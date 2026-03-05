# Photo Manager

A native iOS app for quickly reviewing and cleaning up large photo libraries. Built for iPhone with SwiftUI and PhotoKit.

## Features

- **Grid Browser** — Scroll through your entire library in a fast, lazy-loading grid
- **Swipe Review** — Tinder-style card swiper: swipe left to mark for deletion, right to keep
- **Safe Deletion** — Photos are moved to iOS "Recently Deleted" (not permanently deleted)
- **30-Day Recovery** — Recover any photo from the Recently Deleted album in Photos.app within 30 days
- **Progress Saved** — Your review position is saved across app sessions
- **Undo** — Undo your last 20 swipe decisions during a session
- **Multi-Select** — Select multiple photos in the grid and delete them in one batch
- **Full-Screen Viewer** — Pinch-to-zoom, swipe between photos, one-tap delete

---

## Requirements

- macOS with **Xcode 15** or later
- iOS 16 deployment target
- A **physical iPhone** (Photos library access is limited in the Simulator)
- An Apple Developer account (free account works for personal device testing)

---

## Setup in Xcode

### Step 1: Create a new Xcode project

1. Open Xcode and choose **File → New → Project**
2. Select the **iOS → App** template and click Next
3. Configure:
   - **Product Name**: `PhotoManager` (or any name you prefer)
   - **Interface**: SwiftUI
   - **Language**: Swift
   - **Minimum Deployments**: iOS 16.0
4. Choose a location and click **Create**

### Step 2: Add the source files

1. In Finder, navigate to the cloned repo folder
2. In Xcode's Project Navigator (left sidebar), select the `PhotoManager` group (the folder with the app name)
3. Drag all the Swift files from the repo into Xcode, organized by folder:
   - `PhotoApp/App/` → `PhotoApp.swift`, `ContentView.swift`
   - `PhotoApp/ViewModel/` → `PhotoLibraryViewModel.swift`
   - `PhotoApp/Views/` → all view files
   - `PhotoApp/Components/` → `ThumbnailView.swift`, `SwipeCardView.swift`
   - `PhotoApp/Utilities/` → `ImageLoader.swift`
4. When prompted, ensure **"Add to target: PhotoManager"** is checked
5. Delete the auto-generated `ContentView.swift` that Xcode created (keep the one from the repo)

> **Tip**: You can create Groups in Xcode (right-click → New Group) to match the folder structure, which makes the project easier to navigate.

### Step 3: Configure Info.plist

Xcode 13+ uses a different Info.plist approach. Either:

**Option A** (easiest): Open the project's **Info** tab (click the project root → target → Info), and add these keys manually:
- `Privacy - Photo Library Usage Description` → `Photo Manager needs access to your photo library to browse and organize your photos.`
- `Privacy - Photo Library Additions Usage Description` → `Photo Manager needs access to save photos to your library.`

**Option B**: Replace the auto-generated `Info.plist` with the one from `PhotoApp/Resources/Info.plist` in this repo. In Xcode, select the existing `Info.plist` in the navigator and use **File → Replace** (or delete and re-add).

### Step 4: Set up signing

1. Select the project root in the Navigator
2. Select the **PhotoManager** target → **Signing & Capabilities**
3. Check **Automatically manage signing**
4. Select your Apple ID team from the dropdown
5. Change the **Bundle Identifier** to something unique, e.g. `com.yourname.photomanager`

### Step 5: Build and run

1. Connect your iPhone via USB
2. Trust the developer certificate on your iPhone if prompted (Settings → General → VPN & Device Management)
3. Select your iPhone from the device picker at the top of Xcode
4. Press **⌘R** to build and run

On first launch, the app will ask for permission to access your Photos library. Tap **Allow Full Access** for the best experience.

---

## How to Use

### Grid View (Library tab)

- Scroll through all your photos in a grid
- Tap **Select** (top right) to enter selection mode
- Tap photos to select/deselect them (blue checkmark appears)
- Tap **Move to Recently Deleted** at the bottom to delete selected photos
- Tap any photo to view it full-screen

### Swipe Review (Review tab)

- Swipe **left** or tap the **red trash button** to mark a photo for deletion
- Swipe **right** or tap the **green checkmark** to keep a photo and move to the next
- Tap **Undo** (orange arrow) to undo your last decision
- When you've marked photos, tap **"Move [N] Photos to Recently Deleted"** to commit
- Your position is automatically saved — close the app and pick up where you left off

### Full-Screen Viewer

- Tap any photo in the grid to open it full-screen
- **Pinch** to zoom in/out
- **Double-tap** to toggle 2.5× zoom
- **Swipe left/right** to navigate to adjacent photos
- Tap the **red trash icon** (bottom right) to mark the current photo for deletion
- Tap the **orange trash/slash icon** to unmark a photo you previously marked

---

## About "Recently Deleted"

When you delete photos in this app, they are moved to the iOS **Recently Deleted** album — **not permanently erased**. This is the same behavior as deleting photos directly in Apple Photos.

To recover a photo:
1. Open **Photos.app**
2. Tap **Albums** at the bottom
3. Scroll down to **Utilities → Recently Deleted**
4. Tap a photo → **Recover**

Photos in Recently Deleted are **automatically and permanently deleted after 30 days**.

---

## File Structure

```
PhotoApp/
├── App/
│   ├── PhotoApp.swift          # @main entry point
│   └── ContentView.swift       # Root router (permission vs. main UI)
├── ViewModel/
│   └── PhotoLibraryViewModel.swift  # Core: PHFetchResult, caching, deletion
├── Views/
│   ├── PermissionView.swift    # Authorization flow
│   ├── GridView.swift          # LazyVGrid photo browser
│   ├── SwipeReviewView.swift   # Card swiper for rapid review
│   └── PhotoDetailView.swift   # Full-screen photo viewer with zoom
├── Components/
│   ├── ThumbnailView.swift     # Reusable grid cell with lazy loading
│   └── SwipeCardView.swift     # Visual card for swipe interface
├── Utilities/
│   └── ImageLoader.swift       # async/await wrapper for PHCachingImageManager
└── Resources/
    └── Info.plist              # Photo permission descriptions
```

---

## Privacy

This app runs entirely on-device. No photos, metadata, or usage data ever leave your iPhone. The app only accesses your photo library locally through Apple's PhotoKit framework.
