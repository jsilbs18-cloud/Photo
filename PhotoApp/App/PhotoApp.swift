import SwiftUI

@main
struct PhotoApp: App {
    @StateObject private var viewModel = PhotoLibraryViewModel()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(viewModel)
        }
    }
}
