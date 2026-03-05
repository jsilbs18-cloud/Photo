import SwiftUI
import Photos

struct ContentView: View {
    @EnvironmentObject var viewModel: PhotoLibraryViewModel

    var body: some View {
        Group {
            switch viewModel.authorizationStatus {
            case .authorized, .limited:
                MainTabView()
            case .notDetermined, .denied, .restricted:
                PermissionView()
            @unknown default:
                PermissionView()
            }
        }
        .animation(.easeInOut, value: viewModel.authorizationStatus)
    }
}

private struct MainTabView: View {
    @EnvironmentObject var viewModel: PhotoLibraryViewModel
    @State private var selectedTab: Tab = .library

    enum Tab { case library, review }

    var body: some View {
        TabView(selection: $selectedTab) {
            GridView()
                .tabItem {
                    Label("Library", systemImage: "photo.on.rectangle")
                }
                .tag(Tab.library)

            SwipeReviewView()
                .tabItem {
                    Label("Review", systemImage: "hand.point.right")
                }
                .badge(viewModel.pendingDeletionIDs.count > 0 ? viewModel.pendingDeletionIDs.count : nil)
                .tag(Tab.review)
        }
        .tint(.blue)
    }
}
