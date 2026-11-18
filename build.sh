#!/bin/bash
# Build script for Discord DM Deleter Android APK
# Run this on Linux (or WSL on Windows, or a Linux VM on Mac)

set -e  # Exit on error

echo "========================================"
echo "Discord DM Deleter - Android APK Builder"
echo "========================================"
echo

# Check if we're on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  This script must run on Linux!"
    echo "   Options:"
    echo "   1. Use WSL2 on Windows"
    echo "   2. Use a Linux VM (VirtualBox, VMware, etc.)"
    echo "   3. Use GitHub Actions (see .github/workflows/build.yml)"
    echo "   4. Use a cloud CI/CD service"
    exit 1
fi

# Check for buildozer
if ! command -v buildozer &> /dev/null; then
    echo "📦 Installing buildozer..."
    pip install --user buildozer
    export PATH="$PATH:$HOME/.local/bin"
fi

# Check for Java
if ! command -v java &> /dev/null; then
    echo "☕ Installing OpenJDK 17..."
    sudo apt update && sudo apt install -y openjdk-17-jdk
fi

# Check for Android SDK/NDK dependencies
echo "🔧 Checking build dependencies..."
sudo apt update && sudo apt install -y \
    git zip unzip openjdk-17-jdk python3-pip autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev automake \
    libgmp-dev libmpc-dev libmpfr-dev libltdl-dev

# Navigate to project directory
cd "$(dirname "$0")"

# Clean previous builds (optional)
read -p "Clean previous build artifacts? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning previous builds..."
    buildozer android clean
fi

# Build the APK
echo "🏗️  Building APK (this may take 10-30 minutes on first run)..."
buildozer android debug

# Check if build succeeded
if [ -f "bin/"*.apk ]; then
    APK_PATH=$(ls -t bin/*.apk | head -1)
    echo
    echo "✅ Build successful!"
    echo "📱 APK location: $APK_PATH"
    echo "📏 APK size: $(du -h "$APK_PATH" | cut -f1)"
    echo
    echo "To install on device:"
    echo "  adb install -r $APK_PATH"
    echo
    echo "To copy to phone:"
    echo "  scp $APK_PATH user@phone:/sdcard/Download/"
else
    echo
    echo "❌ Build failed! Check the output above for errors."
    exit 1
fi