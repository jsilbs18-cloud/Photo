import SwiftUI
import Photos

struct PermissionView: View {
    @EnvironmentObject var viewModel: PhotoLibraryViewModel

    var body: some View {
        VStack(spacing: 32) {
            Spacer()

            Image(systemName: "photo.on.rectangle.angled")
                .font(.system(size: 80))
                .foregroundColor(.blue)

            VStack(spacing: 12) {
                Text("Photo Manager")
                    .font(.largeTitle.bold())

                Text("Quickly review and clean up your photo library.\nPhotos you delete go to Recently Deleted and can be recovered for 30 days.")
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal)
            }

            Spacer()

            VStack(spacing: 16) {
                if viewModel.authorizationStatus == .denied || viewModel.authorizationStatus == .restricted {
                    DeniedAccessView()
                } else if viewModel.authorizationStatus == .limited {
                    LimitedAccessView()
                } else {
                    Button(action: { viewModel.requestAuthorization() }) {
                        Label("Grant Photo Access", systemImage: "photo.badge.checkmark")
                            .font(.headline)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(14)
                    }
                    .padding(.horizontal)
                }
            }
            .padding(.bottom, 40)
        }
    }
}

private struct DeniedAccessView: View {
    var body: some View {
        VStack(spacing: 16) {
            Text("Photo access was denied.")
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)

            Button(action: openSettings) {
                Label("Open Settings", systemImage: "gear")
                    .font(.headline)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(14)
            }
            .padding(.horizontal)
        }
    }

    private func openSettings() {
        guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
        UIApplication.shared.open(url)
    }
}

private struct LimitedAccessView: View {
    var body: some View {
        VStack(spacing: 12) {
            Text("You've granted limited photo access. For best results, allow access to all photos.")
                .font(.footnote)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal)

            Button(action: openSettings) {
                Label("Change Access in Settings", systemImage: "gear")
                    .font(.subheadline)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.orange.opacity(0.15))
                    .foregroundColor(.orange)
                    .cornerRadius(14)
            }
            .padding(.horizontal)
        }
    }

    private func openSettings() {
        guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
        UIApplication.shared.open(url)
    }
}
