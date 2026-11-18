[app]

# (str) Title of your application
title = Discord DM Deleter

# (str) Package name
package.name = dmdel

# (str) Package domain (needed for android/ios packaging)
package.domain = org.dmdel

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,kv,json,md,png,jpg,ttf

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.10,kivy,kivymd,requests,urllib3,certifi,charset_normalizer,idna

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.3.0

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples
#android.presplash_lottie = "assets/lottie/loading.json"

# (str) Adaptive icon of the application (used if Android API level is 26+)
#android.adaptive_icon.filename = %(source.dir)s/data/icon.png

# (str) Adaptive icon background color
#android.adaptive_icon.background_color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# (list) features (adds uses-feature -tags to manifest)
#android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 23

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 27c

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 23

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid any interaction with the server, or to speed up the build.
#android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# Use that parameter together with android.entrypoint to use custom Java class instead of default PythonActivity
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# Use that parameter to provide a filename from where to load your custom XML code
#android.extra_manifest_xml =

# (str) Extra xml to write directly inside the <manifest><application> tag of AndroidManifest.xml
# Use that parameter to provide a filename from where to load your custom XML code
#android.extra_application_xml =

# (str) Full name including package path of the Java class that implements Python Service
# Use that parameter to use custom Java class instead of default PythonService
#android.service_class_name = org.kivy.android.PythonService

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Android logcat to use
#android.logcat = True

# (str) Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides automatic versionCode computation (used in build.gradle)
#android.version_code = 1

# (str) Custom gradle file to use for the build
#android.gradle_file =

# (bool) Enable AndroidX support (required for Android 10+)
android.enable_androidx = True

# (bool) Add Google Play Services support
#android.play_services = False

# (str) Specifies the name of the custom file to include in the build
#android.add_jar =

# (str) Specifies the name of the custom file to include in the build
#android.add_aar =

# (str) Specifies the name of the custom file to include in the build
#android.add_src =

# (str) Specifies the name of the custom file to include in the build
#android.add_jni =

# (str) Specify the Android Gradle Plugin version to use
#android.gradle_plugin_version = 8.1.0

# (str) Specify the Kotlin version to use
#android.kotlin_version = 1.9.10

# (bool) If True, build AAB (Android App Bundle) instead of APK
#android.build_aab = False

# (str) Additional arguments to pass to gradle
#android.gradle_args =

# (bool) Gradle plugin to enable Jetpack Compose support
#android.enable_jetpack_compose = False

#
# Python for android (p4a) specific
#

# (str) python-for-android URL to use for checkout
#p4a.url = https://github.com/kivy/python-for-android

# (str) python-for-android fork to use in case non-default fork is used
#p4a.fork = kivy

# (str) python-for-android branch to use
#p4a.branch = master

# (str) python-for-android specific commit to use
#p4a.commit =

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your build recipes (if empty, it will look in the default install location)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Filename to the bootstrap to use for p4a
p4a.bootstrap = sdl2

# (str) python-for-android specific extra args
p4a.extra_args = --extra-pip-packages=kivymd

# Control passing the --use-setup-py vs --ignore-setup-py to p4a (in "installRequirements" command)
#p4a.use_setup_py = False

# (str) Extra command line arguments to pass when invoking python-for-android.toolchain
#p4a.extra_args =

#
# iOS specific
#

# (str) Path to the iOS project directory
#ios.path =

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <firstname> <lastname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

# (list) List of provisioning profiles to use for signing
#ios.provision =

# (list) List of provisioning profiles to use for signing the release version
#ios.provision.release =

# [ios] internal path where the application will be installed
#ios.install_path = /var/mobile/Applications/

# (bool) If True, use buildozer to bundle app with Xcode
#ios.use_xcode = True

# (str) Path to the Xcode project directory
#ios.xcode_path =

# (str) Path to the xcodeproj directory
#ios.xcodeproj_path =

# (bool) If True, build iOS with Xcode
#ios.build = True

#
# Buildozer specific
#

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (bool) Display warning if buildozer is run as root (default: False)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List of hooks (when buildozer performs the default actions of "get_recipe_env",
#    "get_dependencies", "build_package", "build_dist")
#    -----------------------------------------------------------------------------
#    A hook is a Python function that takes the buildozer instance as the single argument.
#    Hooks are called at specific points in the build process.

#    For example, to add a custom recipe for a package named 'mypkg':
#
#    def my_recipe_func(buildozer):
#        print("Adding my custom recipe")
#        buildozer.recipes["mypkg"] = os.path.join(buildozer.specs[0].source_dir, "recipes", "mypkg")
#
#    hooks = [my_recipe_func]
#
#    See https://buildozer.readthedocs.io/en/latest/recipes.html#hooks
#    -----------------------------------------------------------------------------

#    -----------------------------------------------------------------------------
#    List of callbacks (when buildozer performs the default actions of "get_recipe_env",
#    "get_dependencies", "build_package", "build_dist")
#    -----------------------------------------------------------------------------
#    A callback is a Python function that takes the buildozer instance as the single argument.
#    Callbacks are called at specific points in the build process.
#    For example, to add a custom recipe for a package named 'mypkg':
#
#    def my_recipe_func(buildozer):
#        print("Adding my custom recipe")
#        buildozer.recipes["mypkg"] = os.path.join(buildozer.specs[0].source_dir, "recipes", "mypkg")
#
#    callbacks = [my_recipe_func]
#
#    See https://buildozer.readthedocs.io/en/latest/recipes.html#callbacks
#    -----------------------------------------------------------------------------

# (str) buildozer binary to use for building (default: buildozer)
# buildozer_bin = buildozer

# (bool) Enable the new buildozer based on p4a toolchain
# new_buildozer = False

# (str) Buildozer repository URL
# buildozer_url = https://github.com/kivy/buildozer

# (str) Buildozer branch to use
# buildozer_branch = master

# (str) Buildozer commit to use
# buildozer_commit =