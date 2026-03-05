import SwiftUI
import Photos

private let thumbnailTargetSize = CGSize(width: 150, height: 150)

struct ThumbnailView: View {
    let asset: PHAsset
    let index: Int
    var isSelectionMode: Bool = false

    @EnvironmentObject var viewModel: PhotoLibraryViewModel
    @State private var image: UIImage?
    @State private var requestID: PHImageRequestID?

    var isSelected: Bool {
        viewModel.pendingDeletionIDs.contains(asset.localIdentifier)
    }

    var body: some View {
        ZStack(alignment: .topTrailing) {
            imageContent
            if isSelectionMode {
                selectionOverlay
            }
        }
        .contentShape(Rectangle())
        .onAppear { loadImage() }
        .onDisappear { cancelLoad() }
    }

    // MARK: - Subviews

    private var imageContent: some View {
        Group {
            if let img = image {
                Image(uiImage: img)
                    .resizable()
                    .scaledToFill()
            } else {
                Rectangle()
                    .foregroundColor(Color(.systemGray5))
                    .overlay(
                        Image(systemName: "photo")
                            .foregroundColor(Color(.systemGray3))
                    )
            }
        }
        .clipped()
        .aspectRatio(1, contentMode: .fit)
        .overlay(
            // Dim selected photos in selection mode
            isSelectionMode && isSelected
                ? Color.blue.opacity(0.3)
                : Color.clear
        )
    }

    private var selectionOverlay: some View {
        ZStack {
            Circle()
                .fill(isSelected ? Color.blue : Color.white.opacity(0.8))
                .frame(width: 24, height: 24)
                .overlay(
                    Circle().stroke(Color.white, lineWidth: 1.5)
                )
            if isSelected {
                Image(systemName: "checkmark")
                    .font(.system(size: 12, weight: .bold))
                    .foregroundColor(.white)
            }
        }
        .padding(6)
    }

    // MARK: - Image Loading

    private func loadImage() {
        guard image == nil else { return }
        let scale = UIScreen.main.scale
        let size = CGSize(width: thumbnailTargetSize.width * scale,
                          height: thumbnailTargetSize.height * scale)

        let id = viewModel.requestImageSync(for: asset,
                                            targetSize: size,
                                            deliveryMode: .opportunistic) { img, _ in
            if let img {
                DispatchQueue.main.async { self.image = img }
            }
        }
        requestID = id

        // Update the cache window centered on this cell's index.
        viewModel.updateCacheWindow(centerIndex: index, windowSize: 100)
    }

    private func cancelLoad() {
        if let id = requestID {
            viewModel.cancelImageRequest(id)
            requestID = nil
        }
    }
}
