[app]
# (str) Title of your application
title = Local LLM Chat

# (str) Package name
package.name = locallmchat

# (str) Package domain (needed for android/ios packaging)
package.domain = org.jash18

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,certifi,urllib3,charset-normalizer,idna

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# (int) Target Android API
android.api = 31

# (int) Minimum API your APK + Aapt/Aapt2 will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use (deprecated; removed to avoid p4a fetching latest)
# android.sdk = 31

# (str) Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
