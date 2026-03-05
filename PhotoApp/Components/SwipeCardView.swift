import SwiftUI
import Photos

struct SwipeCardView: View {
    let asset: PHAsset
    let dragOffset: CGSize
    let isFrontCard: Bool

    @EnvironmentObject var viewModel: PhotoLibraryViewModel
    @State private var image: UIImage?
    @State private var requestID: PHImageRequestID?

    private var deleteOpacity: Double {
        let t = -dragOffset.width / 80
        return max(0, min(1, t))
    }

    private var keepOpacity: Double {
        let t = dragOffset.width / 80
        return max(0, min(1, t))
    }

    var body: some View {
        ZStack {
            // Background placeholder
            RoundedRectangle(cornerRadius: 16)
                .fill(Color(.systemGray5))

            // Photo
            if let img = image {
                Image(uiImage: img)
                    .resizable()
                    .scaledToFill()
                    .clipShape(RoundedRectangle(cornerRadius: 16))
            } else {
                ProgressView()
            }

            // Gradient overlay at bottom for metadata
            VStack {
                Spacer()
                metadataBar
            }

            // DELETE label (appears when dragging left)
            if isFrontCard {
                VStack {
                    HStack {
                        Spacer()
                        deleteLabel
                            .opacity(deleteOpacity)
                        Spacer().frame(width: 24)
                    }
                    Spacer()
                }
                .padding(.top, 40)

                // KEEP label (appears when dragging right)
                VStack {
                    HStack {
                        Spacer().frame(width: 24)
                        keepLabel
                            .opacity(keepOpacity)
                        Spacer()
                    }
                    Spacer()
                }
                .padding(.top, 40)
            }
        }
        .onAppear { loadImage() }
        .onDisappear { cancelLoad() }
    }

    // MARK: - Labels

    private var deleteLabel: some View {
        Text("DELETE")
            .font(.title2.bold())
            .foregroundColor(.white)
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(Color.red.opacity(0.85))
            .cornerRadius(8)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.red, lineWidth: 2)
            )
            .rotationEffect(.degrees(-15))
    }

    private var keepLabel: some View {
        Text("KEEP")
            .font(.title2.bold())
            .foregroundColor(.white)
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(Color.green.opacity(0.85))
            .cornerRadius(8)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.green, lineWidth: 2)
            )
            .rotationEffect(.degrees(15))
    }

    // MARK: - Metadata Bar

    private var metadataBar: some View {
        HStack {
            VStack(alignment: .leading, spacing: 2) {
                if let date = asset.creationDate {
                    Text(date, style: .date)
                        .font(.caption.bold())
                        .foregroundColor(.white)
                }
                Text("\(asset.pixelWidth) × \(asset.pixelHeight)")
                    .font(.caption2)
                    .foregroundColor(.white.opacity(0.8))
            }
            Spacer()
        }
        .padding(12)
        .background(
            LinearGradient(
                colors: [Color.clear, Color.black.opacity(0.55)],
                startPoint: .top,
                endPoint: .bottom
            )
            .clipShape(
                UnevenRoundedRectangle(topLeadingRadius: 0,
                                       bottomLeadingRadius: 16,
                                       bottomTrailingRadius: 16,
                                       topTrailingRadius: 0)
            )
        )
    }

    // MARK: - Image Loading

    private func loadImage() {
        guard image == nil else { return }
        let scale = UIScreen.main.scale
        let bounds = UIScreen.main.bounds
        let size = CGSize(width: bounds.width * scale * 0.9, height: bounds.height * scale * 0.8)

        let id = viewModel.requestImageSync(for: asset,
                                            targetSize: size,
                                            deliveryMode: .opportunistic) { img, _ in
            if let img {
                DispatchQueue.main.async { self.image = img }
            }
        }
        requestID = id
    }

    private func cancelLoad() {
        if let id = requestID {
            viewModel.cancelImageRequest(id)
            requestID = nil
        }
    }
}
