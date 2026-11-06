[app]

title = Monu AI Voice Editor
package.name = monuaivoiceeditor
package.domain = org.monuvoicestudio

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,md
source.exclude_dirs = .git,.github,venv,env,build,dist,__pycache__,server

version = 0.1.1

requirements = python3,kivy==2.3.0,requests,plyer

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.minapi = 23
android.api = 33
android.ndk = 25b

# First get a stable 64-bit APK; add 32-bit after the first successful build.
android.archs = arm64-v8a

android.accept_sdk_license = True
p4a.bootstrap = sdl2

# Pin python-for-android to a known release whose Python recipe is 3.11.5.
# This prevents latest p4a from selecting the incompatible Python 3.14 recipe.
p4a.commit = 957a3e5f8c270f7aa648ba185e5a68c1077a798d

log_level = 2

source.exclude_patterns = server/*, .github/*, *.zip

[buildozer]
warn_on_root = 1
