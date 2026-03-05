import SwiftUI
import Photos

struct PhotoDetailView: View {
    let initialIndex: Int

    @EnvironmentObject var viewModel: PhotoLibraryViewModel
    @Environment(\.dismiss) private var dismiss

    @State private var currentIndex: Int
    @State private var showOverlay = true
    @State private var image: UIImage?
    @State private var isLoadingFullRes = false
    @State private var zoomScale: CGFloat = 1.0
    @State private var showDeleteConfirmation = false

    init(initialIndex: Int) {
        self.initialIndex = initialIndex
        _currentIndex = State(initialValue: initialIndex)
    }

    var currentAsset: PHAsset? {
        viewModel.asset(at: currentIndex)
    }

    var isMarkedForDeletion: Bool {
        guard let asset = currentAsset else { return false }
        return viewModel.isMarkedForDeletion(asset)
    }

    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()

            TabView(selection: $currentIndex) {
                ForEach(0..<viewModel.totalCount, id: \.self) { index in
                    if let asset = viewModel.asset(at: index) {
                        ZoomableImageView(asset: asset)
                            .tag(index)
                    }
                }
            }
            .tabViewStyle(.page(indexDisplayMode: .never))
            .ignoresSafeArea()

            if showOverlay {
                overlayControls
                    .transition(.opacity)
            }
        }
        .navigationBarHidden(true)
        .statusBarHidden(!showOverlay)
        .onTapGesture {
            withAnimation(.easeInOut(duration: 0.2)) {
                showOverlay.toggle()
            }
        }
        .onChange(of: currentIndex) { _, newIndex in
            viewModel.updateCacheWindow(centerIndex: newIndex, windowSize: 10)
        }
    }

    // MARK: - Overlay Controls

    private var overlayControls: some View {
        VStack {
            // Top bar
            HStack {
                Button(action: { dismiss() }) {
                    Image(systemName: "chevron.left")
                        .font(.title3.bold())
                        .foregroundColor(.white)
                        .padding(10)
                        .background(Color.black.opacity(0.4))
                        .clipShape(Circle())
                }

                Spacer()

                if let asset = currentAsset, let date = asset.creationDate {
                    Text(date, style: .date)
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.9))
                }

                Spacer()

                // Share button
                if let asset = currentAsset {
                    ShareLink(item: Image(uiImage: image ?? UIImage()),
                              preview: SharePreview("Photo", image: Image(uiImage: image ?? UIImage()))) {
                        Image(systemName: "square.and.arrow.up")
                            .font(.title3)
                            .foregroundColor(.white)
                            .padding(10)
                            .background(Color.black.opacity(0.4))
                            .clipShape(Circle())
                    }
                    .disabled(image == nil)
                    .opacity(image == nil ? 0.5 : 1)
                    _ = asset // suppress warning
                }
            }
            .padding(.horizontal)
            .padding(.top, 56) // account for status bar

            Spacer()

            // Bottom bar
            HStack {
                if let asset = currentAsset {
                    VStack(alignment: .leading, spacing: 2) {
                        if let date = asset.creationDate {
                            Text(date, style: .time)
                                .font(.caption)
                                .foregroundColor(.white.opacity(0.8))
                        }
                        Text("\(asset.pixelWidth) × \(asset.pixelHeight)")
                            .font(.caption2)
                            .foregroundColor(.white.opacity(0.6))
                    }
                }

                Spacer()

                // Delete / undelete button
                if let asset = currentAsset {
                    Button(action: { toggleDeletion(asset: asset) }) {
                        Image(systemName: isMarkedForDeletion ? "trash.slash.fill" : "trash.fill")
                            .font(.title3)
                            .foregroundColor(isMarkedForDeletion ? .orange : .red)
                            .padding(10)
                            .background(Color.black.opacity(0.4))
                            .clipShape(Circle())
                    }
                }
            }
            .padding(.horizontal)
            .padding(.bottom, 40)
        }
        .background(
            LinearGradient(
                colors: [Color.black.opacity(0.6), Color.clear, Color.clear, Color.black.opacity(0.5)],
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()
            .allowsHitTesting(false)
        )
    }

    // MARK: - Actions

    private func toggleDeletion(asset: PHAsset) {
        withAnimation(.easeInOut(duration: 0.2)) {
            if isMarkedForDeletion {
                viewModel.unmarkForDeletion(asset)
            } else {
                viewModel.markForDeletion(asset)
                UIImpactFeedbackGenerator(style: .medium).impactOccurred()
            }
        }
    }
}

// MARK: - ZoomableImageView

/// Displays a full-resolution photo with pinch-to-zoom support.
struct ZoomableImageView: View {
    let asset: PHAsset

    @EnvironmentObject var viewModel: PhotoLibraryViewModel
    @State private var image: UIImage?
    @State private var requestID: PHImageRequestID?
    @State private var zoomScale: CGFloat = 1.0
    @State private var lastZoomScale: CGFloat = 1.0
    @State private var offset: CGSize = .zero
    @State private var lastOffset: CGSize = .zero

    var body: some View {
        GeometryReader { geo in
            ZStack {
                Color.black

                if let img = image {
                    Image(uiImage: img)
                        .resizable()
                        .scaledToFit()
                        .scaleEffect(zoomScale)
                        .offset(offset)
                        .gesture(magnifyGesture)
                        .gesture(dragGesture)
                        .onTapGesture(count: 2) { toggleZoom(in: geo) }
                } else {
                    ProgressView()
                        .tint(.white)
                }
            }
            .frame(width: geo.size.width, height: geo.size.height)
        }
        .onAppear { loadImage() }
        .onDisappear { cancelLoad() }
    }

    private var magnifyGesture: some Gesture {
        MagnificationGesture()
            .onChanged { scale in
                zoomScale = lastZoomScale * scale
            }
            .onEnded { scale in
                lastZoomScale = max(1.0, min(5.0, zoomScale))
                withAnimation(.spring()) {
                    zoomScale = lastZoomScale
                    if zoomScale == 1.0 { offset = .zero; lastOffset = .zero }
                }
            }
    }

    private var dragGesture: some Gesture {
        DragGesture()
            .onChanged { value in
                guard zoomScale > 1.0 else { return }
                offset = CGSize(
                    width: lastOffset.width + value.translation.width,
                    height: lastOffset.height + value.translation.height
                )
            }
            .onEnded { _ in
                lastOffset = offset
            }
    }

    private func toggleZoom(in geo: GeometryProxy) {
        withAnimation(.spring()) {
            if zoomScale > 1.0 {
                zoomScale = 1.0
                lastZoomScale = 1.0
                offset = .zero
                lastOffset = .zero
            } else {
                zoomScale = 2.5
                lastZoomScale = 2.5
            }
        }
    }

    private func loadImage() {
        // Load a quick thumbnail first
        let thumbnailID = viewModel.requestImageSync(
            for: asset,
            targetSize: CGSize(width: 400, height: 400),
            deliveryMode: .fastFormat
        ) { img, _ in
            if let img, self.image == nil {
                DispatchQueue.main.async { self.image = img }
            }
        }
        requestID = thumbnailID

        // Then load full resolution
        let fullID = viewModel.requestImageSync(
            for: asset,
            targetSize: PHImageManagerMaximumSize,
            deliveryMode: .highQualityFormat
        ) { img, info in
            let isCancelled = (info?[PHImageCancelledKey] as? Bool) ?? false
            if !isCancelled, let img {
                DispatchQueue.main.async { self.image = img }
            }
        }
        requestID = fullID
    }

    private func cancelLoad() {
        if let id = requestID {
            viewModel.cancelImageRequest(id)
            requestID = nil
        }
        // Reset zoom when leaving the view
        zoomScale = 1.0
        lastZoomScale = 1.0
        offset = .zero
        lastOffset = .zero
    }
}
