[app]

# (str) Title of your application
title = SpotDL

# (str) Package name
package.name = spotdl

# (str) Package domain (needed for android/ios packaging)
package.domain = org.suydev

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,flask,yt-dlp,mutagen,requests,pyjnius,android

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash image (string)
#presplash = ./splash.png

# (str) Icon image (string)
#icon = ./icon.png

# (list) Supported orientations
#orientations = portrait,landscape

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a

# (int) Target API (APIS) to use for the current apk
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 24

# (int) Android SDK version to use
android.sdk = 34

# (int) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support.
android.ndk_api = 24

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to resolve symbols for android/libpythonX.Y.so
#   useful for the embedded environments which don't have the generate_symlinks tool.
android.skip_symbols = false

# (str) Python for android (p4a) branch to use, defaults to master
#p4a.branch = master

# (bool) Whether to sign the apk (default is False)
# Note: if you set this to true, you also need to provide the keystore and
#       keystore password via the relevant properties.
android.debug_signing = True

# (str) Set the android app's custom certificate (string)
#   Example: ##.##.##.##:/path/to/my.keystore
#android.custom_cert_path =

# (int) Set the android app's custom certificate's priority (string)
#android.custom_cert_priority =

# (str) Keystore file path.
#android.keystore =

# (str) Keystore password.
#android.keystore_password =

# (str) Keystore alias.
#android.keystore_alias =

# (str) Gradle properties to add to gradle.properties
#   Example: #android.add_generated_gradle_properties = key1=value1,key2=value2
#android.add_generated_gradle_properties =

# (list) Java compilations options for aar generation.
#   Example: #android.jar_annotations = [annotation1,annotation2]
#android.jar_annotations =

# (bool) Set if it should copy preserved libs into the libs folder for aar packaging
#   (set to 0 to disable)
android.copy_libs = 1

# (str) The Android logcat filters to use
android.logcat_filters = *:S

# (bool) Copy libraries instead of making a symlink (False = symlink, True = copy)
android.copy_libs = 1

# (str) Android entrypoint, default is main activity
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is @style/Theme.AppCompat
#android.apptheme = @style/Theme.AppCompat

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK,FOREIGN_SERVICE,POST_NOTIFICATIONS,WRITE_EXTERNAL_STORAGE,READ_MEDIA_AUDIO,READ_MEDIA_VIDEO,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS

# (bool) Target Android SDK, necessary to enable the default window softinput mode
#android.target_android = 34

# (str) Android window manager type, can be activity, application (default: activity)
#android.window_manager = activity

# (bool) Enable Jetpack AndroidX
#android.enable_androidx = True

# (bool) Enable Jetpack AndroidX Jetifier
#android.enable_jetifier = True

# (str) Android extra compile time arguments
#android.compile_args =

# (list) Source files to exclude (let empty to include all the files)
source.exclude_exts =

# (list) List of directory to exclude (let empty to include all the files)
source.exclude_dirs =

# (list) List of exclusions using pattern matching (let empty to include all the files)
source.exclude_patterns =

# (str) Language to use for translations
#lang =

# (enum) Licence
#license =

# (int) Version of your application
version = 1.0

# (int) Minimum required version
#min_ver = 1

# (list) Image files to include
#image =

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash image (string)
#presplash = ./splash.png

# (str) Icon image (string)
#icon = ./icon.png

# (list) Supported orientations
#orientations = portrait,landscape

#
# Python for android (p4a) specific
#

# (str) Python-for-android fork to use, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) Python for android branch to use, defaults to master
#p4a.branch = master

# (bool) If true, then use `--ignore-sandbox-patch` (default is false)
#p4a.ignore_sandbox_patch = False

# (str) Hook script path (optional)
#p4a.hook =

# (str) Hook script args (optional)
#p4a.hook_args =

# (bool) If true, then copy the MATCHING_LIB from the build to the final apk
#   (this only works with the buildozer tool)
#p4a.copy_matching_lib = False

# (str) The Xcode project to use for building ios
#ios.project =

# (str) The XCode target to use for building ios
#ios.target =

# (str) The minimum version of iOS
#ios.min_version = 9.0

# (str) The iOS application argument used to launch the app
#ios.argument =

# (str) The iOS reserved memory size (string)
#ios.reserved_mem =

# (str) The iOS reserve offset (string)
#ios.reserved_offset =

# (str) The iOS build signg string (string)
#ios.signing =

# (str) The iOS export forrmat string (string)
#ios.export_format =

# (str) The iOS bundle identifier (string)
#ios.bundle_id =

# (str) The iOS release date (string)
#ios.release_date =

# (str) The iOS ship weight (string)
#ios.ship_weight =

# (str) The iOScale factor (string)
#ios.scale =

# (str) The iOS developerr string (string)
#ios.developer =

# (str) The iOS distribution string (string)
#ios.distribution =

# (str) The iOS build date (string)
#ios.build_date =

# (str) The iOS build make (string)
#ios.build_make =

# (str) The iOS build model (string)
#ios.build_model =

# (str) The iOS build model (string)
#ios.build_model =

# (str) The iOS build model (string)
#ios.build_model =

# (str) The iOS build model (string)
#ios.build_model =

# (str) The iOS build model (string)
#ios.build_model =

# (str) The iOS build model (string)
#ios.build_model =

# (str) The iOS build model (string)
#ios.build_model =

# (str) The iOS build model (string)
#ios.build_model =

# (str) The iOS build model (string)
#ios.build_model =

# (str) The iOS build model (string)
#ios.build_model =

[source]

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let empty to include all the files)
source.exclude_exts =

# (list) List of directory to exclude (let empty to include all the files)
source.exclude_dirs =

# (list) List of exclusions using pattern matching (let empty to include all the files)
source.exclude_patterns =

[wheel]

# (list) Supported Wheels
# .whl) packages that should be copied to the android apk
#wheel_libs =

# (bool) Enable experimental signed wheels support
#wheel_split = False

[log]

# (log) Define where to put log files
#log_level = 2
#log_dir = logs

# (str) Route for log files
#log_route =

# (str/float) Show level of logging (0: nothing, 1: warnings, 2: info, 3: debug)
log_level = 2

# (str) Route for log files
log_dir = logs

# (str) Route for log files
log_route =

# (bool) Do not append the default android logcat filtering
#logcat_filters = false

# (list) List of p4a versions to try (let empty to always use the latest version)
#p4a_versions =

# (list) List of p4a versions to try (let empty to always use the latest version)
p4a_versions =

# (str) Android logcat filters to use
#logcat_filters = *:S

# (str) Android logcat filters to use
logcat_filters = *:S

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = warning, 3 = debug)
log_level = 2

# (int) Display warning if buildozer.py is run instead of the actual build script
#warn_on_root = 1

# (str) Path to buildozer.py
#path =

# (str) Path to buildozer spec file
#spec_file =

# (str) Path to buildozer.py
#path_to_buildozer = buildozer.py

# (str) Path to buildozer spec file
#spec_file =

# (str) Path to buildozer.py
#path_to_buildozer = buildozer.py