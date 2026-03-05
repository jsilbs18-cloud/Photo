import Foundation
import Photos
import UIKit

private let reviewIndexKey = "com.photomanager.reviewIndex"
private let thumbnailSize = CGSize(width: 150, height: 150)

@MainActor
final class PhotoLibraryViewModel: NSObject, ObservableObject {

    // MARK: - Published State

    @Published var authorizationStatus: PHAuthorizationStatus = .notDetermined
    @Published var totalCount: Int = 0
    @Published var currentReviewIndex: Int = 0
    @Published var pendingDeletionIDs: Set<String> = []
    @Published var isPerformingDeletion: Bool = false
    @Published var lastDeletionError: String?

    // MARK: - Private

    private var fetchResult: PHFetchResult<PHAsset> = .init()
    private let cachingManager = PHCachingImageManager()
    private var cachedIndexRange: Range<Int> = 0..<0

    // MARK: - Init

    override init() {
        super.init()
        let saved = UserDefaults.standard.integer(forKey: reviewIndexKey)
        currentReviewIndex = saved
        authorizationStatus = PHPhotoLibrary.authorizationStatus(for: .readWrite)
        if authorizationStatus == .authorized || authorizationStatus == .limited {
            loadLibrary()
            PHPhotoLibrary.shared().register(self)
        }
    }

    deinit {
        PHPhotoLibrary.shared().unregisterChangeObserver(self)
        cachingManager.stopCachingImagesForAllAssets()
    }

    // MARK: - Authorization

    func requestAuthorization() {
        Task {
            let status = await PHPhotoLibrary.requestAuthorization(for: .readWrite)
            authorizationStatus = status
            if status == .authorized || status == .limited {
                loadLibrary()
                PHPhotoLibrary.shared().register(self)
            }
        }
    }

    // MARK: - Library Loading

    private func loadLibrary() {
        let options = PHFetchOptions()
        options.sortDescriptors = [NSSortDescriptor(key: "creationDate", ascending: false)]
        options.includeHiddenAssets = false
        fetchResult = PHAsset.fetchAssets(with: .image, options: options)
        totalCount = fetchResult.count
        // Clamp review index in case photos were deleted externally
        if currentReviewIndex >= totalCount {
            currentReviewIndex = max(0, totalCount - 1)
            persistReviewIndex()
        }
    }

    // MARK: - Asset Access

    func asset(at index: Int) -> PHAsset? {
        guard index >= 0, index < fetchResult.count else { return nil }
        return fetchResult.object(at: index)
    }

    // MARK: - Cache Window Management

    /// Call this whenever the visible center index changes.
    /// windowSize is the total number of assets to pre-cache (split equally before/after center).
    func updateCacheWindow(centerIndex: Int, windowSize: Int) {
        let half = windowSize / 2
        let lower = max(0, centerIndex - half)
        let upper = min(fetchResult.count, centerIndex + half)
        let newRange = lower..<upper

        guard newRange != cachedIndexRange else { return }

        let toStop = assetsInRange(cachedIndexRange).filter { !newRange.contains(cachedIndexRange.lowerBound) }
        let toStart = assetsInRange(newRange)

        let stopAssets = indexRangeAssets(cachedIndexRange.filter { !newRange.contains($0) })
        let startAssets = indexRangeAssets(newRange.filter { !cachedIndexRange.contains($0) })

        if !stopAssets.isEmpty {
            cachingManager.stopCachingImages(for: stopAssets,
                                             targetSize: thumbnailSize,
                                             contentMode: .aspectFill,
                                             options: nil)
        }
        if !startAssets.isEmpty {
            cachingManager.startCachingImages(for: startAssets,
                                              targetSize: thumbnailSize,
                                              contentMode: .aspectFill,
                                              options: nil)
        }

        cachedIndexRange = newRange
        _ = toStop // suppress warning
        _ = toStart
    }

    private func indexRangeAssets(_ indices: [Int]) -> [PHAsset] {
        indices.compactMap { asset(at: $0) }
    }

    private func assetsInRange(_ range: Range<Int>) -> [PHAsset] {
        range.compactMap { asset(at: $0) }
    }

    // MARK: - Image Loading

    func loadImage(for asset: PHAsset,
                   targetSize: CGSize,
                   deliveryMode: PHImageRequestOptionsDeliveryMode) async -> UIImage? {
        let options = PHImageRequestOptions()
        options.deliveryMode = deliveryMode
        options.isNetworkAccessAllowed = true
        options.resizeMode = targetSize == PHImageManagerMaximumSize ? .none : .fast

        return await withCheckedContinuation { continuation in
            cachingManager.requestImage(
                for: asset,
                targetSize: targetSize,
                contentMode: .aspectFill,
                options: options
            ) { image, info in
                // Only resolve once with the best available image.
                // PHKit may call back multiple times (degraded, then full).
                let isDegraded = (info?[PHImageResultIsDegradedKey] as? Bool) ?? false
                if !isDegraded || image != nil {
                    continuation.resume(returning: image)
                }
            }
        }
    }

    func cancelImageRequest(_ requestID: PHImageRequestID) {
        cachingManager.cancelImageRequest(requestID)
    }

    func requestImageSync(for asset: PHAsset,
                          targetSize: CGSize,
                          deliveryMode: PHImageRequestOptionsDeliveryMode,
                          resultHandler: @escaping (UIImage?, [AnyHashable: Any]?) -> Void) -> PHImageRequestID {
        let options = PHImageRequestOptions()
        options.deliveryMode = deliveryMode
        options.isNetworkAccessAllowed = true
        options.resizeMode = targetSize == PHImageManagerMaximumSize ? .none : .fast

        return cachingManager.requestImage(
            for: asset,
            targetSize: targetSize,
            contentMode: .aspectFill,
            options: options,
            resultHandler: resultHandler
        )
    }

    // MARK: - Mark / Unmark for Deletion

    func markForDeletion(_ asset: PHAsset) {
        pendingDeletionIDs.insert(asset.localIdentifier)
    }

    func unmarkForDeletion(_ asset: PHAsset) {
        pendingDeletionIDs.remove(asset.localIdentifier)
    }

    func isMarkedForDeletion(_ asset: PHAsset) -> Bool {
        pendingDeletionIDs.contains(asset.localIdentifier)
    }

    // MARK: - Commit Deletions
    // Moves marked photos to iOS Recently Deleted (recoverable for 30 days).
    // PHAssetChangeRequest.deleteAssets() is NOT a permanent delete.
    func commitDeletions() async {
        guard !pendingDeletionIDs.isEmpty else { return }
        isPerformingDeletion = true
        lastDeletionError = nil

        // Collect the PHAsset objects for each pending ID.
        let options = PHFetchOptions()
        let predicate = NSPredicate(format: "localIdentifier IN %@", Array(pendingDeletionIDs))
        options.predicate = predicate
        let assetsToDelete = PHAsset.fetchAssets(with: options)

        do {
            try await PHPhotoLibrary.shared().performChanges {
                PHAssetChangeRequest.deleteAssets(assetsToDelete)
            }
            pendingDeletionIDs.removeAll()
            // fetchResult will be updated via photoLibraryDidChange
        } catch {
            lastDeletionError = error.localizedDescription
        }

        isPerformingDeletion = false
    }

    // MARK: - Review Index Persistence

    func advanceReviewIndex() {
        if currentReviewIndex < totalCount - 1 {
            currentReviewIndex += 1
            persistReviewIndex()
        }
    }

    func decrementReviewIndex() {
        if currentReviewIndex > 0 {
            currentReviewIndex -= 1
            persistReviewIndex()
        }
    }

    private func persistReviewIndex() {
        UserDefaults.standard.set(currentReviewIndex, forKey: reviewIndexKey)
    }
}

// MARK: - PHPhotoLibraryChangeObserver

extension PhotoLibraryViewModel: PHPhotoLibraryChangeObserver {
    nonisolated func photoLibraryDidChange(_ changeInstance: PHChange) {
        Task { @MainActor in
            guard let changes = changeInstance.changeDetails(for: self.fetchResult) else { return }
            self.cachingManager.stopCachingImagesForAllAssets()
            self.cachedIndexRange = 0..<0
            self.fetchResult = changes.fetchResultAfterChanges
            self.totalCount = self.fetchResult.count
            if self.currentReviewIndex >= self.totalCount {
                self.currentReviewIndex = max(0, self.totalCount - 1)
                self.persistReviewIndex()
            }
        }
    }
}
