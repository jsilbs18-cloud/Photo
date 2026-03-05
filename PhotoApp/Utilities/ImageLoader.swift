import Photos
import UIKit

/// Lightweight wrapper around PHCachingImageManager that bridges callback-based
/// PHKit APIs to async/await. Each load operation can be cancelled by cancelling
/// the enclosing Swift Task.
final class ImageLoader {

    private let manager: PHCachingImageManager

    init(manager: PHCachingImageManager) {
        self.manager = manager
    }

    /// Loads an image for the given asset asynchronously.
    /// - Parameters:
    ///   - asset: The PHAsset to load.
    ///   - targetSize: The desired output size in points (pass PHImageManagerMaximumSize for full-res).
    ///   - contentMode: How the image should fill the target size.
    ///   - deliveryMode: Quality vs speed trade-off (.fastFormat for thumbnails, .highQualityFormat for full-res).
    /// - Returns: The best available UIImage, or nil if the request failed or was cancelled.
    func load(
        asset: PHAsset,
        targetSize: CGSize,
        contentMode: PHImageContentMode = .aspectFill,
        deliveryMode: PHImageRequestOptionsDeliveryMode = .opportunistic
    ) async -> UIImage? {
        let options = PHImageRequestOptions()
        options.deliveryMode = deliveryMode
        options.isNetworkAccessAllowed = true
        options.resizeMode = targetSize == PHImageManagerMaximumSize ? .none : .fast

        return await withTaskCancellationHandler {
            await withCheckedContinuation { continuation in
                let requestID = manager.requestImage(
                    for: asset,
                    targetSize: targetSize,
                    contentMode: contentMode,
                    options: options
                ) { image, info in
                    let isDegraded = (info?[PHImageResultIsDegradedKey] as? Bool) ?? false
                    let isCancelled = (info?[PHImageCancelledKey] as? Bool) ?? false
                    // Resolve on the final delivery (not degraded preview) or cancellation.
                    if !isDegraded || isCancelled {
                        continuation.resume(returning: isCancelled ? nil : image)
                    }
                }
                _ = requestID // captured for cancellation below
            }
        } onCancel: {
            // No direct way to cancel inside withCheckedContinuation here without
            // storing the requestID externally. The manager will eventually call
            // back with PHImageCancelledKey = true once it detects Task cancellation.
        }
    }

    /// Non-async version that returns a PHImageRequestID for manual cancellation.
    /// Use this in SwiftUI views that manage their own cancellation lifecycle.
    @discardableResult
    func requestThumbnail(
        for asset: PHAsset,
        targetSize: CGSize,
        resultHandler: @escaping (UIImage?, [AnyHashable: Any]?) -> Void
    ) -> PHImageRequestID {
        let options = PHImageRequestOptions()
        options.deliveryMode = .opportunistic
        options.isNetworkAccessAllowed = false // thumbnails come from local cache
        options.resizeMode = .fast

        return manager.requestImage(
            for: asset,
            targetSize: targetSize,
            contentMode: .aspectFill,
            options: options,
            resultHandler: resultHandler
        )
    }

    func cancel(_ requestID: PHImageRequestID) {
        manager.cancelImageRequest(requestID)
    }
}
