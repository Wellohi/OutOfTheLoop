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

# (list) List of modules to crash if found in search path
source.exclude_strs = tests,docs,spec

# (list) List of directory to exclude (let buildozer find them)
source.exclude_dirs = tests, bin

# (str) The version of your application
version = 0.1

# (list) Kivy version to use
kivy.version = 2.1.0

# (list) Your application requirements
# --- MODIFIED: Simplified for the virtual environment ---
# We have already installed the correct versions of cython and jnius.
requirements = python3,kivy

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Supported orientation (one of landscape, sensorLandscape, portrait, sensorPortrait)
orientation = portrait

android.screen_orientation = portrait

# (list) Permissions
# android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (str) The Android arch to build for.
android.archs = arm64-v8a

# --- NEW: This is the definitive fix for the pyenv conflict ---
# This line explicitly tells python-for-android which Python executable to use for the build,
# pointing directly to the one inside our clean virtual environment.
# Make sure your username is correct in this path.
p4a.python_cmd = /home/wellohi/pyproject/outoftheloop/build_env/bin/python3

#
# Buildozer specific
#

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
