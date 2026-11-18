# Discord DM Deleter

A tool to bulk-delete your own Discord direct messages. Built with Kivy/KivyMD for cross-platform support (Desktop & Android).

## ⚠️ Important Disclaimer

**Use at your own risk.** This tool uses your Discord user token (not a bot token) to delete messages via the Discord API. 
- Discord's Terms of Service prohibit user token automation
- Deleting messages is **permanent and irreversible**
- Rate limits are strictly enforced (1.5s delay between deletions)
- Your account could be flagged or banned

## Features

- 🔐 **Secure login** with Discord user token
- 📱 **Cross-platform**: Desktop (Windows/Mac/Linux) and Android
- 🔍 **Search & filter** messages by content
- ✅ **Select all/deselect all** your messages
- 🗑️ **Bulk delete** with confirmation
- 📊 **Load more/Load all** pagination
- 🌙 **Dark theme** optimized for mobile

## Desktop Installation

```bash
# Clone and navigate
cd dmdeleter

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

## Android APK Build

### Option 1: GitHub Actions (Recommended - No local setup needed)

1. Fork this repository
2. Go to **Actions** tab → **Build Android APK** → **Run workflow**
3. Wait for build to complete (~10-30 mins)
4. Download the APK from **Artifacts** or **Releases** (if you push a tag like `v1.0.0`)

### Option 2: Local Linux Build

**Requirements:** Linux (Ubuntu/Debian/WSL2), not macOS or Windows directly

```bash
cd dmdeleter
chmod +x build.sh
./build.sh
```

The script will:
- Install buildozer and dependencies
- Build the APK (first run downloads Android SDK/NDK ~2GB)
- Output APK to `bin/dmdel-1.0.0-arm64-v8a-debug.apk`

### Option 3: Docker Build

```bash
cd dmdeleter
docker run --rm -v $(pwd):/app -w /app kivy/buildozer android debug
```

## Getting Your Discord Token

1. Open **discord.com** in Chrome/Edge
2. Press **F12** → **Network** tab
3. Send any message in any DM
4. Click the **messages** request (or `channels/@me/messages`)
5. **Headers** → **Request Headers** → **authorization**
6. Copy the token value (starts with `MTA...` or similar)

**⚠️ Never share your token!** Anyone with it has full account access.

## Usage

1. **Login**: Paste your token and tap "Login"
2. **Select conversation**: Tap a DM from the sidebar
3. **Filter**: Search messages, toggle "Only my messages"
4. **Load**: Tap "Load More" or "Load All" to fetch history
5. **Select**: Check messages to delete (only your messages can be checked)
6. **Delete**: Tap "Delete Selected" → Confirm → Wait for completion

## Project Structure

```
dmdeleter/
├── main.py              # Kivy/KivyMD app entry point
├── buildozer.spec       # Buildozer configuration
├── requirements.txt     # Python dependencies
├── build.sh             # Local build script
├── .github/workflows/   # CI/CD for automated builds
└── README.md            # This file
```

## Technical Details

- **Framework**: Kivy 2.3 + KivyMD 1.2 (Material Design)
- **API**: Discord API v9 (users/@me/channels, channels/{id}/messages)
- **Threading**: Background threads for API calls, UI updates via Clock
- **Storage**: No local storage - token kept in memory only
- **Permissions**: INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid token" | Token expired or copied incorrectly. Get fresh token. |
| Rate limited (429) | Wait longer between deletions. Increase DELAY constant. |
| Build fails on Mac/Windows | Use GitHub Actions or WSL2/Linux VM |
| APK won't install | Enable "Unknown sources" in Android settings |
| Messages not loading | Check network, some DMs may be inaccessible |

## License

MIT License - Use responsibly.

---

**Remember**: This tool is for personal use only. Automating user accounts violates Discord ToS. Consider using Discord's built-in "Delete Message" feature for individual messages instead.