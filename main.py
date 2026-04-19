import tkinter as tk
from tkinter import messagebox
from adb import *
from riskmap import get_risk

root = tk.Tk()
root.title("ADB Toolkit PRO")
root.geometry("1000x600")
root.configure(bg="#1e1e1e")

BG = "#1e1e1e"
FG = "#ffffff"
BTN = "#2d2d2d"

# ---------- TOP ----------
top = tk.Frame(root, bg=BG)
top.pack(fill="x")

search_var = tk.StringVar()

tk.Entry(top, textvariable=search_var, bg="#333", fg="white").pack(side="left", padx=5)

tk.Button(top, text="Search", bg=BTN, fg=FG, command=lambda: load_apps()).pack(side="left")
tk.Button(top, text="Check", bg=BTN, fg=FG, command=lambda: status.set(get_devices())).pack(side="left")
tk.Button(top, text="Repair", bg=BTN, fg=FG, command=lambda: status.set(repair())).pack(side="left")
tk.Button(top, text="Diagnose", bg=BTN, fg=FG, command=lambda: status.set(smart_diagnose())).pack(side="left")
tk.Button(top, text="Dashboard", bg=BTN, fg=FG, command=lambda: status.set(get_storage()+get_ram())).pack(side="left")
tk.Button(top, text="Debloat", bg=BTN, fg=FG, command=lambda: status.set(safe_debloat())).pack(side="left")
tk.Button(top, text="🧹 Clear ALL", bg=BTN, fg=FG, command=lambda: status.set(clear_all_cache())).pack(side="left")
tk.Button(top, text="💾 Backup", bg=BTN, fg=FG, command=lambda: status.set(full_backup())).pack(side="left")

# ---------- SCROLL ----------
container = tk.Frame(root, bg=BG)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container, bg=BG)
scrollbar = tk.Scrollbar(container, command=canvas.yview)
frame = tk.Frame(canvas, bg=BG)

frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0,0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ---------- STATUS ----------
status = tk.StringVar()
tk.Label(root, textvariable=status, fg="gray", bg=BG).pack()

BLOCKED = ["com.android.systemui"]

def confirm(app):
    risk = get_risk(app)

    if app in BLOCKED:
        messagebox.showerror("BLOCKED", "System app – ne!")
        return False

    if "🔴" in risk:
        return messagebox.askyesno("DANGER", f"{app}\nSystem app!\nPokračovat?")

    return True

def action(func, app, text):
    if not confirm(app):
        return
    func(app)
    status.set(f"{text}: {app}")

def load_apps():
    for w in frame.winfo_children():
        w.destroy()

    apps = get_apps()
    disabled = get_disabled_apps()
    q = search_var.get().lower()

    for app in apps:
        if q and q not in app.lower():
            continue

        row = tk.Frame(frame, bg=BG)
        row.pack(fill="x")

        risk = get_risk(app)

        if app in disabled:
            state = "⛔ DISABLED"
        else:
            state = "✔ ENABLED"

        tk.Label(row, text=f"{risk} {state} {app}", bg=BG, fg=FG).pack(side="left")

        tk.Button(row, text="Disable", bg=BTN, fg=FG,
                  command=lambda a=app: action(disable_app, a, "Disabled")).pack(side="right")

        tk.Button(row, text="Uninstall", bg=BTN, fg=FG,
                  command=lambda a=app: action(uninstall_app, a, "Uninstalled")).pack(side="right")

        tk.Button(row, text="Enable", bg=BTN, fg=FG,
                  command=lambda a=app: action(enable_app, a, "Enabled")).pack(side="right")

root.mainloop()