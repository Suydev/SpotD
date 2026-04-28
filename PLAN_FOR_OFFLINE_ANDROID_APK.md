# Plan: Convert SpotDL to Fully Offline Android APK

## Current State Analysis
The existing Android app is a WebView wrapper that connects to an externally hosted Flask server. To make it completely offline, we need to:

1. **Embed the Flask server** within the Android APK
2. **Run Python on Android** using Chaquopy or similar
3. **Bundle all Python dependencies** with the APK
4. **Configure WebView to connect to localhost** instead of external URL
5. **Handle Android-specific considerations** (permissions, lifecycle, etc.)

## Step-by-Step Implementation Plan

### Phase 1: Prepare Chaquopy Integration

#### 1.1 Modify build.gradle.kts to add Chaquopy plugin
```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.chaquo.python") version "12.0.0" add false
}
```

#### 1.2 Configure Python in android{}
```kotlin
android {
    // ... existing config ...
    
    sourceSets {
        main {
            python.srcDir "src/main/python"
        }
    }
}
```

#### 1.3 Add Chaquopy dependencies
```kotlin
dependencies {
    // ... existing dependencies ...
    implementation("com.chaquo.python:python:12.0.0")
}
```

### Phase 2: Restructure Project for Python Integration

#### 2.1 Create Python source directory
```
android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/              # Existing Kotlin code
│   │   │   ├── res/               # Existing resources
│   │   │   └── python/            # NEW: Python code
│   │   │       ├── spotdl_server/ # Copy of src/ from main project
│   │   │       └── __init__.py
```

#### 2.2 Copy Flask application to Android Python folder
```
android/app/src/main/python/spotdl_server/
├── web_app.py                 # Main Flask app (modified)
├── requirements.txt           # Python dependencies
└── (other necessary files)
```

### Phase 3: Modify Flask App for Android

#### 3.1 Create Android-specific Flask modifications
- Change host binding from `0.0.0.0` to `127.0.0.1` (localhost only)
- Adjust file paths to use Android-specific directories
- Modify cleanup worker to be Android-lifecycle aware
- Adjust logging for Android environment

#### 3.2 Key Modifications to web_app.py:
```python
# Android-specific path handling
import android.content.Context  # From Chaquopy
from android.content import Context

def get_android_context():
    # Get Android Context from Chaquopy
    return Python.getInstance().getApplicationContext()

def get_data_dir():
    ctx = get_android_context()
    return ctx.getDir("spotdl_data", Context.MODE_PRIVATE)

def get_downloads_dir():
    ctx = get_android_context()
    return ctx.getExternalFilesDir(Environment.DIRECTORY_MUSIC) + "/SpotDL"
```

#### 3.3 Adjust server startup for Android lifecycle
```python
# Instead of app.run(), we'll start/stop with Android lifecycle
class FlaskServer:
    def __init__(self):
        self.server = None
        self.thread = None
    
    def start(self):
        # Start Flask in background thread
        self.thread = Thread(target=self._run_server)
        self.thread.daemon = True
        self.thread.start()
    
    def _run_server(self):
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
    
    def stop(self):
        # Implement graceful shutdown
        pass
```

### Phase 4: Modify Android Kotlin Code

#### 4.1 Update MainActivity.kt to manage Flask server lifecycle
```kotlin
class MainActivity : AppCompatActivity() {
    private var flaskServer: FlaskServer? = null
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // ... existing setup ...
        
        // Start Flask server when activity starts
        flaskServer = FlaskServer()
        flaskServer.start()
        
        // Load local server instead of external URL
        web.loadUrl("http://127.0.0.1:5000")
    }
    
    override fun onDestroy() {
        super.onDestroy()
        // Stop Flask server when activity ends
        flaskServer?.stop()
    }
}
```

#### 4.2 Request necessary permissions
Add to AndroidManifest.xml:
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
<uses-permission android:name="android.permission.WAKE_LOCK"/>
<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
<uses-permission android:name="android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"/>
<uses-permission android:name="android.permission.READ_MEDIA_AUDIO"/>
<uses-permission android:name="android.permission.READ_MEDIA_VIDEO"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
    android:maxSdkVersion="28"/>
```

### Phase 5: Build and Test

#### 5.1 Local build commands
```bash
cd android
./gradlew assembleDebug
```

#### 5.2 Testing checklist
- [ ] App launches without errors
- [ ] Flask server starts successfully (check logs)
- [ ] WebView loads localhost:5000
- [ ] Search functionality works
- [ ] Download initiation works
- [ ] Files save to correct Android directories (/Music/SpotDL/)
- [ ] Notifications work for completed downloads
- [ ] App handles backgrounding properly
- [ ] Battery optimization exemptions work

## Files That Need Modification

### 1. android/app/build.gradle.kts
- Add Chaquopy plugin and configuration
- Add Python dependencies
- Configure Python source sets

### 2. android/app/src/main/AndroidManifest.xml
- Add required permissions
- Configure backup rules if needed
- Set android:usesCleartextTraffic="true" for localhost (if targeting < Android 9)

### 3. android/app/src/main/java/com/suydev/spotdl/MainActivity.kt
- Add Flask server lifecycle management
- Modify URL loading to point to localhost
- Add permission handling

### 4. New Python files in android/app/src/main/python/
- Copy of modified web_app.py
- requirements.txt
- Any helper modules

### 5. Optional: assets/ folder for pre-bundled data
- Default icons
- Pre-configured settings

## Dependencies to Bundle
From requirements.txt:
- flask
- flask-sqlalchemy (may need alternatives for Android)
- spotipy (may need modification for Android)
- qrcode[pil]
- yt-dlp
- python-dotenv
- mutagen
- tqdm
- colorama
- psutil
- pillow
- requests
- gunicorn (may not need if using Flask dev server)

## Potential Challenges and Solutions

### Challenge 1: Native Dependencies
Some packages like `psutil`, `pillow`, `mutagen` have native components.
**Solution**: Chaquopy handles many common packages, but we may need to:
- Use Chaquopy's pip to build from source
- Find Android-compatible alternatives
- Bundle pre-built .so files if necessary

### Challenge 2: File System Access
Android has scoped storage restrictions.
**Solution**: 
- Use Context.getExternalFilesDir() for app-specific storage
- Request MANAGE_EXTERNAL_STORAGE for Android 11+ if needed for broader access
- Use Storage Access Framework for user-selected directories

### Challenge 3: Background Processing
Android restricts background services.
**Solution**:
- Use WorkManager for periodic cleanup
- Use Foreground Service for active downloads (with notification)
- Use AlarmManager for timed tasks if needed
- Properly handle app lifecycle events

### Challenge 4: yt-dlp on Android
yt-dlp might need special handling.
**Solution**:
- Test if pure Python yt-dlp works via Chaquopy
- Consider bundling a pre-built version
- Fallback to simpler YouTube extraction if needed

## Estimated Effort
- Phase 1-2 (Setup): 2-3 hours
- Phase 3 (Flask modification): 4-6 hours
- Phase 4 (Android integration): 3-4 hours
- Phase 5 (Testing/debugging): 4-6 hours
- **Total**: ~15-20 hours

## Success Criteria
1. APK installs successfully on Android device
2. App launches and shows SpotDL UI
3. All core features work offline:
   - Search Spotify content
   - Initiate downloads
   - Track download progress
   - Save files to device
   - Play downloaded content
4. No external server connection required
5. Reasonable APK size (< 100MB ideal)
6. Good battery performance