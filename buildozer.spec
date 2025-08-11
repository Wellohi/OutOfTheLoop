[app]

# (str) Title of your application
title = Out of the Loop

# (str) Package name
package.name = outoftheloop

# (str) Package domain (needed for android/ios packaging)
package.domain = org.mygame

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let buildozer find them)
source.include_exts = py,png,jpg,kv,atlas

# (str) The version of your application
version = 0.2

# (list) Your application requirements
# MODIFIED: Simplified to the essentials. The other libraries are handled by the build process.
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) This provides a direct rule for the Android OS.
android.screen_orientation = portrait

# (list) The Android architectures to build for.
android.archs = arm64-v8a

#
# Buildozer specific
#

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
