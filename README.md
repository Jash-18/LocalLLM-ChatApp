# Local LLM Chat App

A ChatGPT-like Android application built with Python (Kivy/KivyMD) that connects to your local LM Studio server.

## Features

- 🤖 ChatGPT-like interface
- 🏠 Connects to local LM Studio server
- 📱 Native Android app experience
- ⚙️ Configurable server settings
- 💾 Conversation history
- 🌙 Dark theme interface
- 📝 Material Design components

## Prerequisites

1. **LM Studio**: Install and run LM Studio on your computer
2. **Model**: Download any compatible LLM model in LM Studio
3. **Server**: Enable the local server in LM Studio (usually runs on port 1234)

## Setup Instructions

### Method 1: Download APK (Easiest)

1. Go to the [Releases](https://github.com/Jash-18/LocalLLM-ChatApp/releases) section
2. Download the latest APK file
3. Install on your Android device
4. Configure the server URL in settings

### Method 2: Build from Source

#### Prerequisites for Building
- Python 3.8+
- Buildozer
- Android SDK/NDK (automatically handled by Buildozer)

#### Build Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Jash-18/LocalLLM-ChatApp.git
   cd LocalLLM-ChatApp
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Buildozer**:
   ```bash
   pip install buildozer
   ```

4. **Initialize Buildozer** (first time only):
   ```bash
   buildozer android debug
   ```

5. **Build the APK**:
   ```bash
   buildozer android debug
   ```

6. **Find your APK**:
   The APK will be in `bin/` folder as `locallmchat-1.0-debug.apk`

## Configuration

### LM Studio Setup

1. **Start LM Studio**
2. **Load a model** (e.g., Llama 2, Mistral, etc.)
3. **Start the server**:
   - Go to the "Server" tab in LM Studio
   - Click "Start Server"
   - Note the server URL (usually `http://localhost:1234`)

### App Configuration

1. **Open the app**
2. **Tap the settings icon** (gear icon in the top bar)
3. **Configure**:
   - **Server URL**: Your LM Studio server URL
     - If on same device: `http://localhost:1234`
     - If on different device: `http://YOUR_COMPUTER_IP:1234`
   - **Model Name**: The model name from LM Studio
4. **Save settings**

### Finding Your Computer's IP Address

To connect from your phone to your computer:

**Windows**:
```cmd
ipconfig
```
Look for "IPv4 Address"

**Linux/Mac**:
```bash
ifconfig
```
Look for "inet" address

**Example**: If your computer's IP is `192.168.1.100`, use `http://192.168.1.100:1234`

## Usage

1. **Start LM Studio** on your computer and load a model
2. **Start the server** in LM Studio
3. **Open the app** on your Android device
4. **Configure the server URL** in settings
5. **Start chatting!**

## Troubleshooting

### Connection Issues

- **"Connection Error"**: 
  - Check if LM Studio server is running
  - Verify the server URL in settings
  - Ensure your phone and computer are on the same network
  - Check firewall settings on your computer

- **"Timeout Error"**:
  - The model might be slow to respond
  - Try a smaller/faster model
  - Check your network connection

### Building Issues

- **Buildozer fails**:
  ```bash
  buildozer android clean
  buildozer android debug
  ```

- **Missing dependencies**:
  ```bash
  pip install --upgrade buildozer
  ```

## Features in Detail

### Chat Interface
- Clean, modern Material Design interface
- Scrollable conversation history
- User messages appear on the right (blue)
- AI responses appear on the left (gray)
- Auto-scroll to latest messages

### Settings
- Configurable server URL
- Configurable model name
- Settings persist between app sessions

### Error Handling
- Connection error messages
- Timeout handling
- Server error reporting

## File Structure

```
LocalLLM-ChatApp/
├── main.py              # Main application code
├── buildozer.spec       # Buildozer configuration
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── bin/                # Generated APK files (after building)
```

## Technical Details

- **Framework**: Kivy + KivyMD
- **Language**: Python 3
- **Build Tool**: Buildozer
- **API**: OpenAI-compatible REST API
- **Min Android**: API 21 (Android 5.0)
- **Target Android**: API 33 (Android 13)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Provide details about your setup and error messages

## Changelog

### Version 1.0
- Initial release
- Basic chat functionality
- LM Studio integration
- Settings configuration
- Material Design interface