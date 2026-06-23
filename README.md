# Ajeossida
Frida with patches that definitively fix basic detection points on Android and iOS.<br> 
Unfortunately, I discovered that the patches in several custom Frida builds for bypassing detections are incomplete and still detectable.<br>
For example, `frida_agent_main` in memory and the `gum-js-loop` thread name.<br> 
Therefore, I created a Python build script to address these issues.

## 🔄 Auto-Build (This Fork)

This fork includes a **GitHub Actions workflow** that automatically builds ajeossida stealth servers from the latest Frida releases.

- **Weekly auto-build** — checks for the latest Frida version every Sunday
- **Manual trigger** — build any version on demand via `workflow_dispatch`
- **Binary patching** — downloads official Frida binaries and applies stealth patches (fast & reliable)
- **Pre-built releases** — grab patched servers from the [Releases page](../../releases)

### Quick Start
```bash
# Download from releases
gunzip ajeossida-server-17.15.0-android-arm64.gz

# Deploy to device
adb push ajeossida-server-17.15.0-android-arm64 /data/local/tmp/ajeossida-server
adb shell "chmod 755 /data/local/tmp/ajeossida-server"
adb shell "/data/local/tmp/ajeossida-server &"

# Connect
frida -U -f <package> -l <script.js>
```

### Trigger a Build Manually
Go to **Actions → Build Ajeossida → Run workflow** and enter a Frida version (e.g., `17.15.0`) or leave as `latest`.

# Patches
- Android
- [x] No `frida_agent_main` in memory<br>
- [x] No `gum-js-loop, gmain, gdbus, frida-gadget` thread name in `/proc/<pid>/task/<thread_id>/status`<br>
- [x] No `libfrida-agent-raw.so` in linker's so list
- [x] No libc hooking<br>

- iOS
- [x] No `frida_agent_main` in memory<br>
- [x] No `gum-js-loop, gmain, gdbus, pool-frida, pool-spawner` thread name<br>
- [x] No `/usr/lib/frida/` 
- [x] No `exit, abort, task_threads` hooking<br>

# Run
- MacOS<br>
Output: server, gadget (Android, iOS)<br>
`python3 main_macos.py`

- Ubuntu 22.04<br>
Output: server, gagdet (Android)<br>
`python3 main_ubuntu.py`

# MagiskAjeossida
* A magisk module that automatically runs ajeossida-server on boot.  
* To run it in remote mode, use the following command. It will listen on `0.0.0.0:45678`.  
`adb shell "su -c sed -i 's/REMOTE=0/REMOTE=1/' /data/adb/modules/magisk_ajeossida/service.sh"`
* You can attach Frida to a pairipcore protected app using this module.  
However, the app will crash after a few seconds. Bypassing the crash is up to you. (Spawning the app also causes it to crash)

# Contact
- Channel: https://t.me/hackcatml1
- Chat: https://t.me/hackcatmlchat

# References
- [strongR-frida-android](https://github.com/hzzheyang/strongR-frida-android)<br>
- [Florida](https://github.com/Ylarod/Florida)
- [magisk-frida](https://github.com/ViRb3/magisk-frida)