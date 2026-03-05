import SwiftUI
import Photos

struct GridView: View {
    @EnvironmentObject var viewModel: PhotoLibraryViewModel
    @State private var isSelectionMode = false
    @State private var selectedAssetForDetail: (asset: PHAsset, index: Int)?
    @State private var showDeleteConfirmation = false
    @State private var showError = false

    private let columns = [GridItem(.adaptive(minimum: 100, maximum: 150), spacing: 2)]

    var body: some View {
        NavigationStack {
            ZStack(alignment: .bottom) {
                scrollContent

                if !viewModel.pendingDeletionIDs.isEmpty {
                    deleteBar
                }
            }
            .navigationTitle("Library")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar { toolbarContent }
            .navigationDestination(item: $selectedAssetForDetail, destination: { selection in
                PhotoDetailView(initialIndex: selection.index)
            })
            .alert("Error", isPresented: $showError, presenting: viewModel.lastDeletionError) { _ in
                Button("OK", role: .cancel) {}
            } message: { error in
                Text(error)
            }
            .onChange(of: viewModel.lastDeletionError) { _, newValue in
                showError = newValue != nil
            }
        }
    }

    // MARK: - Scroll Content

    private var scrollContent: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 2) {
                ForEach(0..<viewModel.totalCount, id: \.self) { index in
                    if let asset = viewModel.asset(at: index) {
                        ThumbnailView(asset: asset, index: index, isSelectionMode: isSelectionMode)
                            .onTapGesture { handleTap(asset: asset, index: index) }
                    }
                }
            }
            .padding(.bottom, viewModel.pendingDeletionIDs.isEmpty ? 0 : 80)
        }
    }

    // MARK: - Delete Bar

    private var deleteBar: some View {
        VStack(spacing: 0) {
            Divider()
            HStack {
                Text("\(viewModel.pendingDeletionIDs.count) photo\(viewModel.pendingDeletionIDs.count == 1 ? "" : "s") selected")
                    .foregroundColor(.secondary)
                    .font(.subheadline)
                Spacer()
                Button(role: .destructive) {
                    showDeleteConfirmation = true
                } label: {
                    if viewModel.isPerformingDeletion {
                        ProgressView()
                            .tint(.red)
                    } else {
                        Label("Move to Recently Deleted", systemImage: "trash")
                            .font(.subheadline.bold())
                    }
                }
                .disabled(viewModel.isPerformingDeletion)
                .confirmationDialog(
                    "Move \(viewModel.pendingDeletionIDs.count) photo\(viewModel.pendingDeletionIDs.count == 1 ? "" : "s") to Recently Deleted?",
                    isPresented: $showDeleteConfirmation,
                    titleVisibility: .visible
                ) {
                    Button("Move to Recently Deleted", role: .destructive) {
                        Task { await viewModel.commitDeletions() }
                    }
                    Button("Cancel", role: .cancel) {}
                } message: {
                    Text("You can recover them from Recently Deleted in Photos for up to 30 days.")
                }
            }
            .padding(.horizontal)
            .padding(.vertical, 12)
            .background(.ultraThinMaterial)
        }
        .transition(.move(edge: .bottom).combined(with: .opacity))
        .animation(.spring(), value: viewModel.pendingDeletionIDs.isEmpty)
    }

    // MARK: - Toolbar

    @ToolbarContentBuilder
    private var toolbarContent: some ToolbarContent {
        ToolbarItem(placement: .navigationBarLeading) {
            Text("\(viewModel.totalCount) Photos")
                .font(.caption)
                .foregroundColor(.secondary)
        }

        ToolbarItem(placement: .navigationBarTrailing) {
            Button(isSelectionMode ? "Done" : "Select") {
                withAnimation { isSelectionMode.toggle() }
                if !isSelectionMode {
                    // Deselect all when leaving selection mode
                    // (keep pendingDeletionIDs — user may want to commit later)
                }
            }
        }
    }

    // MARK: - Tap Handling

    private func handleTap(asset: PHAsset, index: Int) {
        if isSelectionMode {
            withAnimation(.easeInOut(duration: 0.15)) {
                if viewModel.isMarkedForDeletion(asset) {
                    viewModel.unmarkForDeletion(asset)
                } else {
                    viewModel.markForDeletion(asset)
                }
            }
        } else {
            selectedAssetForDetail = (asset: asset, index: index)
        }
    }
}

// MARK: - Hashable conformance for navigation destination

extension PHAsset: @retroactive Hashable {
    public func hash(into hasher: inout Hasher) {
        hasher.combine(localIdentifier)
    }
    public static func == (lhs: PHAsset, rhs: PHAsset) -> Bool {
        lhs.localIdentifier == rhs.localIdentifier
    }
}

private struct AssetSelection: Hashable {
    let asset: PHAsset
    let index: Int
}
