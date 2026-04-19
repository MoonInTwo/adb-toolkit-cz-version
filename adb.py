import subprocess
import os
from datetime import datetime

ADB_PATH = r"C:\Program Files (x86)\Minimal ADB and Fastboot\adb.exe"

def run(cmd):
    full = f'"{ADB_PATH}" {cmd}'
    return subprocess.run(full, shell=True, capture_output=True, text=True).stdout

# ---------- BASIC ----------
def get_devices():
    return run("devices")

def get_apps():
    out = run("shell pm list packages")
    return [x.replace("package:", "").strip() for x in out.splitlines()]

def get_disabled_apps():
    out = run("shell pm list packages -d")
    return [x.replace("package:", "").strip() for x in out.splitlines()]

# ---------- APP CONTROL ----------
def disable_app(pkg):
    run(f"shell pm disable-user --user 0 {pkg}")

def uninstall_app(pkg):
    run(f"shell pm uninstall --user 0 {pkg}")

def enable_app(pkg):
    run(f"shell pm enable {pkg}")

# ---------- CACHE ----------
def clear_all_cache():
    log = []

    run("shell pm trim-caches 999G")
    log.append("✔ System cache cleaned")

    apps = get_apps()
    for app in apps:
        run(f"shell pm clear {app}")

    log.append("✔ App data/cache reset")

    return "\n".join(log)

# ---------- REPAIR ----------
def repair():
    run("shell pm trim-caches 999G")
    run("shell am kill-all")
    run("shell settings put global window_animation_scale 0")
    run("shell settings put global transition_animation_scale 0")
    run("shell settings put global animator_duration_scale 0")
    return "✔ Repair done"

# ---------- DASHBOARD ----------
def get_storage():
    return run("shell df /data")

def get_ram():
    return run("shell cat /proc/meminfo")

# ---------- DIAGNOSE ----------
def smart_diagnose():
    report = []

    storage = get_storage()
    if "90%" in storage or "95%" in storage:
        report.append("⚠️ Storage almost full")

    report.append("💡 Tip: use debloat + repair")

    return "\n".join(report)

# ---------- DEBLOAT ----------
SAFE_DEBLOAT = [
    "com.facebook.appmanager",
    "com.facebook.services",
    "com.netflix.partner.activation",
    "com.android.bips"
]

def safe_debloat():
    for app in SAFE_DEBLOAT:
        run(f"shell pm disable-user --user 0 {app}")
    return "✔ Debloat done"

# ---------- BACKUP ----------
def full_backup():
    folder = os.path.join(os.getcwd(), "backup_" + datetime.now().strftime("%Y%m%d_%H%M"))
    os.makedirs(folder, exist_ok=True)

    log = []

    # APK backup
    apps = get_apps()
    apk_dir = os.path.join(folder, "apks")
    os.makedirs(apk_dir, exist_ok=True)

    for app in apps:
        path = run(f"shell pm path {app}")
        if "package:" in path:
            apk_path = path.strip().replace("package:", "")
            run(f"pull {apk_path} \"{apk_dir}\"")

    log.append("✔ APKs saved")

    # Storage backup
    run(f"pull /sdcard \"{folder}\\storage\"")
    log.append("✔ Storage saved")

    return "\n".join(log)