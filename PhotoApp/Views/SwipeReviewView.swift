import SwiftUI
import Photos

struct SwipeReviewView: View {
    @EnvironmentObject var viewModel: PhotoLibraryViewModel

    @State private var dragOffset: CGSize = .zero
    @State private var cardRotation: Double = 0
    @State private var reviewHistory: [Int] = [] // indices of reviewed photos (for undo)
    @State private var showCommitSheet = false
    @State private var showError = false

    private let swipeThreshold: CGFloat = 100
    private let maxHistorySize = 20

    // MARK: - Feedback

    private let impactHeavy = UIImpactFeedbackGenerator(style: .heavy)
    private let impactLight = UIImpactFeedbackGenerator(style: .light)

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                progressBar
                    .padding(.horizontal)
                    .padding(.top, 8)

                cardStack
                    .padding(.horizontal, 16)
                    .padding(.vertical, 12)

                actionButtons
                    .padding(.horizontal)
                    .padding(.bottom, 8)
            }
            .navigationTitle("Review")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar { toolbarContent }
            .alert("Error", isPresented: $showError, presenting: viewModel.lastDeletionError) { _ in
                Button("OK", role: .cancel) {}
            } message: { error in
                Text(error)
            }
            .onChange(of: viewModel.lastDeletionError) { _, newValue in
                showError = newValue != nil
            }
            .onChange(of: viewModel.currentReviewIndex) { _, newIndex in
                viewModel.updateCacheWindow(centerIndex: newIndex, windowSize: 10)
            }
        }
    }

    // MARK: - Progress Bar

    private var progressBar: some View {
        VStack(alignment: .leading, spacing: 4) {
            ProgressView(value: Double(viewModel.currentReviewIndex),
                         total: Double(max(1, viewModel.totalCount)))
                .tint(.blue)
                .animation(.linear, value: viewModel.currentReviewIndex)

            HStack {
                Text("\(viewModel.currentReviewIndex) of \(viewModel.totalCount)")
                    .font(.caption)
                    .foregroundColor(.secondary)
                Spacer()
                if !viewModel.pendingDeletionIDs.isEmpty {
                    Text("\(viewModel.pendingDeletionIDs.count) marked for deletion")
                        .font(.caption)
                        .foregroundColor(.red)
                }
            }
        }
    }

    // MARK: - Card Stack

    private var cardStack: some View {
        ZStack {
            // Show up to 3 cards in the stack (current + 2 preview)
            ForEach((0..<3).reversed(), id: \.self) { offset in
                let cardIndex = viewModel.currentReviewIndex + offset
                if let asset = viewModel.asset(at: cardIndex) {
                    SwipeCardView(
                        asset: asset,
                        dragOffset: offset == 0 ? dragOffset : .zero,
                        isFrontCard: offset == 0
                    )
                    .scaleEffect(cardScale(for: offset))
                    .offset(y: cardYOffset(for: offset))
                    .offset(x: offset == 0 ? dragOffset.width : 0,
                            y: offset == 0 ? dragOffset.height * 0.3 : 0)
                    .rotationEffect(.degrees(offset == 0 ? cardRotation : 0))
                    .zIndex(Double(3 - offset))
                    .gesture(offset == 0 ? swipeGesture : nil)
                    .animation(.spring(response: 0.35, dampingFraction: 0.7),
                               value: dragOffset)
                }
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private func cardScale(for offset: Int) -> CGFloat {
        switch offset {
        case 0: return 1.0
        case 1: return 0.95
        default: return 0.90
        }
    }

    private func cardYOffset(for offset: Int) -> CGFloat {
        switch offset {
        case 0: return 0
        case 1: return 12
        default: return 24
        }
    }

    // MARK: - Swipe Gesture

    private var swipeGesture: some Gesture {
        DragGesture()
            .onChanged { value in
                dragOffset = value.translation
                cardRotation = Double(value.translation.width / 20)
            }
            .onEnded { value in
                if value.translation.width < -swipeThreshold {
                    markAndAdvance()
                } else if value.translation.width > swipeThreshold {
                    keepAndAdvance()
                } else {
                    resetCardPosition()
                }
            }
    }

    // MARK: - Actions

    private func markAndAdvance() {
        guard let asset = viewModel.asset(at: viewModel.currentReviewIndex) else { return }
        impactHeavy.impactOccurred()
        viewModel.markForDeletion(asset)
        advanceWithAnimation(direction: .left)
    }

    private func keepAndAdvance() {
        impactLight.impactOccurred()
        advanceWithAnimation(direction: .right)
    }

    private enum SwipeDirection { case left, right }

    private func advanceWithAnimation(direction: SwipeDirection) {
        let xOffset: CGFloat = direction == .left ? -500 : 500
        withAnimation(.easeOut(duration: 0.25)) {
            dragOffset = CGSize(width: xOffset, height: 0)
            cardRotation = direction == .left ? -30 : 30
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) {
            reviewHistory.append(viewModel.currentReviewIndex)
            if reviewHistory.count > maxHistorySize { reviewHistory.removeFirst() }
            viewModel.advanceReviewIndex()
            dragOffset = .zero
            cardRotation = 0
        }
    }

    private func resetCardPosition() {
        withAnimation(.spring(response: 0.4, dampingFraction: 0.7)) {
            dragOffset = .zero
            cardRotation = 0
        }
    }

    // MARK: - Undo

    private func undoLast() {
        guard let lastIndex = reviewHistory.popLast() else { return }
        // If the photo at lastIndex was marked, unmark it
        if let asset = viewModel.asset(at: lastIndex) {
            viewModel.unmarkForDeletion(asset)
        }
        viewModel.currentReviewIndex = lastIndex
        impactLight.impactOccurred()
    }

    // MARK: - Action Buttons

    private var actionButtons: some View {
        VStack(spacing: 12) {
            HStack(spacing: 24) {
                // Delete button
                Button(action: markAndAdvance) {
                    VStack(spacing: 4) {
                        Image(systemName: "trash.circle.fill")
                            .font(.system(size: 52))
                            .foregroundColor(.red)
                        Text("Delete")
                            .font(.caption)
                            .foregroundColor(.red)
                    }
                }
                .disabled(viewModel.asset(at: viewModel.currentReviewIndex) == nil)

                // Undo button
                Button(action: undoLast) {
                    VStack(spacing: 4) {
                        Image(systemName: "arrow.uturn.left.circle.fill")
                            .font(.system(size: 36))
                            .foregroundColor(.orange)
                        Text("Undo")
                            .font(.caption)
                            .foregroundColor(.orange)
                    }
                }
                .disabled(reviewHistory.isEmpty)

                // Keep button
                Button(action: keepAndAdvance) {
                    VStack(spacing: 4) {
                        Image(systemName: "checkmark.circle.fill")
                            .font(.system(size: 52))
                            .foregroundColor(.green)
                        Text("Keep")
                            .font(.caption)
                            .foregroundColor(.green)
                    }
                }
                .disabled(viewModel.asset(at: viewModel.currentReviewIndex) == nil)
            }

            if !viewModel.pendingDeletionIDs.isEmpty {
                Button {
                    showCommitSheet = true
                } label: {
                    HStack {
                        Image(systemName: "trash")
                        Text("Move \(viewModel.pendingDeletionIDs.count) Photo\(viewModel.pendingDeletionIDs.count == 1 ? "" : "s") to Recently Deleted")
                            .font(.subheadline.bold())
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 12)
                    .background(Color.red)
                    .foregroundColor(.white)
                    .cornerRadius(12)
                }
                .disabled(viewModel.isPerformingDeletion)
                .confirmationDialog(
                    "Move \(viewModel.pendingDeletionIDs.count) photo\(viewModel.pendingDeletionIDs.count == 1 ? "" : "s") to Recently Deleted?",
                    isPresented: $showCommitSheet,
                    titleVisibility: .visible
                ) {
                    Button("Move to Recently Deleted", role: .destructive) {
                        Task { await viewModel.commitDeletions() }
                    }
                    Button("Cancel", role: .cancel) {}
                } message: {
                    Text("Photos will be recoverable from the Recently Deleted album in Photos for 30 days.")
                }
            }

            if viewModel.currentReviewIndex >= viewModel.totalCount && viewModel.totalCount > 0 {
                completionView
            }
        }
    }

    private var completionView: some View {
        VStack(spacing: 8) {
            Image(systemName: "checkmark.seal.fill")
                .font(.largeTitle)
                .foregroundColor(.green)
            Text("All photos reviewed!")
                .font(.headline)
            Text("You can restart the review or commit your deletions.")
                .font(.caption)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
            Button("Start Over") {
                viewModel.currentReviewIndex = 0
            }
            .buttonStyle(.bordered)
        }
        .padding()
        .background(Color(.systemGroupedBackground))
        .cornerRadius(16)
    }

    // MARK: - Toolbar

    @ToolbarContentBuilder
    private var toolbarContent: some ToolbarContent {
        ToolbarItem(placement: .navigationBarTrailing) {
            if viewModel.isPerformingDeletion {
                ProgressView()
            }
        }
    }
}
