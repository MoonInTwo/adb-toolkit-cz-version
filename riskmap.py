SAFE = ["instagram", "tiktok", "facebook", "netflix"]

DANGEROUS = [
    "systemui",
    "launcher",
    "gms",
    "google",
    "android.system"
]

def get_risk(app):
    app = app.lower()

    if any(x in app for x in DANGEROUS):
        return "🔴 DANGEROUS"

    if any(x in app for x in SAFE):
        return "🟢 SAFE"

    return "🟡 NORMAL"