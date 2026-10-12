# Standard Library
from sys import exit as sys_exit
from subprocess import (
    DEVNULL,
    check_output,
    CalledProcessError,
    run as run_sub_process,
    Popen
)
from argparse import ArgumentParser
from time import sleep
import os
import signal
import tkinter as tk
import threading
import subprocess

# GUI tool
try:
    from pyautogui import (
        keyDown,
        press,
        keyUp,
        locateOnScreen,
        ImageNotFoundException
    )
except ModuleNotFoundError:
    print(
        "ERROR: pyautogui package not found.\n\n"
        "Ensure your conda env is installed and activated.\n"
        "See `conda_env_setup.md` in `docs/` for help."
    )
    sys_exit(1)


# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT           = os.path.expanduser("~/carla-energy-consumption")
PATH_TO_HELPER_SCRIPTS = os.path.join(PROJECT_ROOT, "demo_helper_scripts")
PATH_TO_UI_IMAGE       = os.path.join(PROJECT_ROOT, "docs/figures/carlaUE4-playbtn.png")
WINDOW_NAME            = "CarlaUE4 - Unreal Editor"
SERVER_EXECUTABLE      = "/home/directlab/carla/Unreal/CarlaUE4/Saved/StagedBuilds/LinuxNoEditor/CarlaUE4.sh"

IMAGE_CONFIDENCE                      = 0.5
EXPECTED_TIME_UNTIL_WINDOW_APPEARANCE = 30
RETRY_WINDOW                          = 5
WAIT_BEFORE_CLIENT_START              = 20
MAP_LOAD_TIMEOUT                      = 180.0


# ── Vehicle ID map ─────────────────────────────────────────────────────────────
VEHICLE_IDS = {
    "kenworth": "vehicle.kenworth.t680e",
    "ogdenbus": "vehicle.ogden.ebus",
    "tesla":    "vehicle.tesla.model3",
}

# ── Charger file per map ───────────────────────────────────────────────────────
CHARGER_FILES = {
    "Town10HD_Opt": "Town10_intersection_chargers",
    "Town10HD":     "Town10_intersection_chargers",
    "Town01_Opt":   "Town01_intersection_chargers",
    "Town02_Opt":   "Town02_intersection_chargers",
    "Town03_Opt":   "Town03_intersection_chargers",
    "Town04_Opt":   "Town04_intersection_chargers",
    "Town05_Opt":   "Town05_intersection_chargers",
    "Town06_Opt":   "Town06_intersection_chargers",
    "Town07_Opt":   "Town07_intersection_chargers",
}

# ── Options ────────────────────────────────────────────────────────────────────
VEHICLES = [
    ("kenworth", "Kenworth T680E Truck"),
    ("ogdenbus", "Ogden Electric Bus"),
    ("tesla",    "Tesla Model 3"),
]

MAPS = [
    ("Town10HD_Opt", "Town 10  — Large detailed city (default, no reload needed)"),
    ("Town03_Opt",   "Town 03  — Medium city with highway & tunnel"),
    ("Town04_Opt",   "Town 04  — Figure-8 highway loop"),
    ("Town05_Opt",   "Town 05  — Grid city, multiple lanes"),
    ("Town06_Opt",   "Town 06  — Long straight highways"),
    ("Town01_Opt",   "Town 01  — Small simple town"),
    ("Town02_Opt",   "Town 02  — Small town, different layout"),
    ("Town07_Opt",   "Town 07  — Rural, narrow roads"),
]

CONTROL_MODES = [
    ("manual",      "Manual Control       — Drive with steering wheel (G920)"),
    ("auto",        "Automated Demo       — Pygame window, vehicle drives itself"),
    ("server_only", "Server Only          — Boot Unreal, no driving program"),
]

# ── Progress window ────────────────────────────────────────────────────────────
class ProgressWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CARLA Boot Progress")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        BG   = "#1a1a2e"
        CYAN = "#00d4ff"
        GREY = "#888888"

        self.root.configure(bg=BG)

        tk.Label(self.root, text="CARLA", font=("Courier New", 18, "bold"), fg=CYAN, bg=BG).pack(pady=(15, 0))
        tk.Label(self.root, text="Boot Progress", font=("Courier New", 10), fg=GREY, bg=BG).pack(pady=(0, 10))
        tk.Frame(self.root, bg="#0f3460", height=2).pack(fill="x", padx=20)

        self.steps_frame = tk.Frame(self.root, bg=BG, padx=20, pady=10)
        self.steps_frame.pack(fill="x")

        self.steps = [
            "Cleaning up ports",
            "Starting CARLA server",
            "Waiting for CARLA build to boot",
            "Waiting for simulation to settle",
            "Starting driving program",
        ]

        self.step_labels = []
        for step in self.steps:
            row = tk.Frame(self.steps_frame, bg=BG)
            row.pack(fill="x", pady=3)
            indicator = tk.Label(row, text="○", font=("Courier New", 12), fg=GREY, bg=BG, width=2)
            indicator.pack(side="left")
            label = tk.Label(row, text=step, font=("Courier New", 11), fg=GREY, bg=BG, anchor="w")
            label.pack(side="left", fill="x")
            self.step_labels.append((indicator, label))

        self.status_var = tk.StringVar(value="Starting up...")
        tk.Label(self.root, textvariable=self.status_var, font=("Courier New", 9), fg=GREY, bg=BG).pack(pady=(5, 15))

        self.current_step = -1
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"+{sw - self.root.winfo_width() - 40}+40")
        self._keep_running = True
        self._update()

    def _update(self):
        if self._keep_running:
            self.root.update()
            self.root.after(100, self._update)

    def advance(self, status_text=""):
        self.current_step += 1
        if self.current_step > 0:
            prev_i, prev_l = self.step_labels[self.current_step - 1]
            prev_i.config(text="✓", fg="#00d4ff")
            prev_l.config(fg="#e8e8e8")
        if self.current_step < len(self.step_labels):
            curr_i, curr_l = self.step_labels[self.current_step]
            curr_i.config(text="►", fg="#ffcc00")
            curr_l.config(fg="#ffcc00")
        if status_text:
            self.status_var.set(status_text)
        self.root.update()

    def complete(self):
        for indicator, label in self.step_labels:
            indicator.config(text="✓", fg="#00d4ff")
            label.config(fg="#e8e8e8")
        self.status_var.set("All done! Simulation running.")
        self.root.update()
        sleep(2)
        self.close()

    def set_status(self, text):
        self.status_var.set(text)
        self.root.update()

    def close(self):
        self._keep_running = False
        try:
            self.root.destroy()
        except Exception:
            pass


# ── Port cleanup ───────────────────────────────────────────────────────────────
def cleanup_ports(progress=None):
    if progress:
        progress.set_status("Killing old CARLA processes...")

    for process in [
        "CarlaUE4-Linux", "CarlaUE4.sh", "UE4Editor",
        "manual_control", "multitracking.py",
        "automatic_control.py", "auto_tracking.py",
    ]:
        run_sub_process(["pkill", "-f", process], capture_output=True)

    sleep(2)

    for process in ["CarlaUE4-Linux", "UE4Editor"]:
        run_sub_process(["pkill", "-9", "-f", process], capture_output=True)

    for port in [2000, 2001, 2002]:
        result = run_sub_process(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        pids = result.stdout.strip()
        if pids:
            if progress:
                progress.set_status(f"Freeing port {port}...")
            for pid in pids.split("\n"):
                try:
                    os.kill(int(pid), signal.SIGKILL)
                except (ProcessLookupError, ValueError):
                    pass

    sleep(2)
    if progress:
        progress.set_status("Ports cleared.")


# ── Map loader ─────────────────────────────────────────────────────────────────

# Launch the server directly into the specific map as a listen/dedicated server
#subprocess.Popen([server_executable, f"{target_map}?listen", "-log"])

# def load_map(map_name, progress=None):
#     if map_name in TOWN10_MAPS: // THIS VARIABLE HAS BEEN DELETED
#         if progress:
#             progress.set_status("Town 10 — skipping reload to preserve custom assets.")
#         return True
#     try:
#         import carla
#         if progress:
#             progress.set_status(f"Connecting to load {map_name}...")
#         client = carla.Client('localhost', 2000)
#         client.set_timeout(MAP_LOAD_TIMEOUT)
#         if progress:
#             progress.set_status(f"Loading {map_name} — may take a while first time...")
#         subprocess.Popen([server_executable, f"{map_name}?listen", "-log"])
#         if progress:
#             progress.set_status(f"{map_name} loaded!")
#         return True
#     except Exception as e:
#         if progress:
#             progress.set_status(f"Map load warning: {e}")
#         return False

# ── Focus pygame window ────────────────────────────────────────────────────────
def focus_pygame_window():
    sleep(4)
    try:
        result = run_sub_process(
            ["xdotool", "search", "--onlyvisible", "--name", "CARLA"],
            capture_output=True, text=True
        )
        handles = result.stdout.strip().split("\n")
        if handles and handles[0]:
            run_sub_process(["xdotool", "windowraise", handles[0]], capture_output=True)
            run_sub_process(["xdotool", "windowfocus", handles[0]], capture_output=True)
    except Exception:
        print("Error loading the pygame window")
        pass


# ── Run simulation ─────────────────────────────────────────────────────────────
def run_simulation(command_args, cwd=None):
    run_sub_process(args=command_args, cwd=cwd)


# ── GUI selection window ───────────────────────────────────────────────────────
def show_selection_window():
    result = {"vehicle": None, "map": None, "mode": None, "cancelled": False}

    root = tk.Tk()
    root.title("CARLA Demo Launcher")
    root.resizable(False, False)

    BG             = "#1a1a2e"
    CARD           = "#16213e"
    ACCENT         = "#0f3460"
    CYAN           = "#00d4ff"
    WHITE          = "#e8e8e8"
    GREY           = "#888888"
    BTN_BG         = "#0f3460"
    BTN_HOV        = "#1a4a80"
    BTN_LAUNCH     = "#00897b"
    BTN_LAUNCH_HOV = "#00bfa5"

    root.configure(bg=BG)

    def make_section(parent, title):
        frame = tk.Frame(parent, bg=CARD, padx=20, pady=15)
        frame.pack(fill="x", padx=30, pady=(10, 0))
        tk.Label(frame, text=title, font=("Courier New", 10, "bold"), fg=CYAN, bg=CARD).pack(anchor="w", pady=(0, 10))
        return frame

    def make_radio(parent, text, variable, value):
        tk.Radiobutton(
            parent, text=text, variable=variable, value=value,
            font=("Courier New", 11), fg=WHITE, bg=CARD,
            activebackground=CARD, activeforeground=CYAN,
            selectcolor=ACCENT, bd=0, highlightthickness=0, cursor="hand2",
        ).pack(anchor="w", pady=2)

    header = tk.Frame(root, bg=BG, pady=20)
    header.pack(fill="x", padx=30)
    tk.Label(header, text="CARLA", font=("Courier New", 32, "bold"), fg=CYAN, bg=BG).pack()
    tk.Label(header, text="Energy Consumption Demo Launcher", font=("Courier New", 11), fg=GREY, bg=BG).pack()
    tk.Frame(root, bg=ACCENT, height=2).pack(fill="x", padx=30)

    vf = make_section(root, "SELECT VEHICLE")
    vehicle_var = tk.StringVar(value=VEHICLES[0][0])
    for vid, vlabel in VEHICLES:
        make_radio(vf, vlabel, vehicle_var, vid)

    mf = make_section(root, "SELECT MAP  (Opt = optimized, better FPS)")
    map_var = tk.StringVar(value=MAPS[0][0])
    for mid, mlabel in MAPS:
        make_radio(mf, mlabel, map_var, mid)

    cf = make_section(root, "SELECT LAUNCH MODE")
    mode_var = tk.StringVar(value=CONTROL_MODES[0][0])
    for cid, clabel in CONTROL_MODES:
        make_radio(cf, clabel, mode_var, cid)

    tk.Label(cf, text="  * Vehicle/map ignored in Server Only mode",
             font=("Courier New", 9), fg=GREY, bg=CARD).pack(anchor="w", pady=(5, 0))

    btn_frame = tk.Frame(root, bg=BG, pady=20)
    btn_frame.pack(fill="x", padx=30)

    def on_launch():
        result["vehicle"]   = vehicle_var.get()
        result["map"]       = map_var.get()
        result["mode"]      = mode_var.get()
        result["cancelled"] = False
        root.destroy()

    def on_cancel():
        result["cancelled"] = True
        root.destroy()

    def make_button(parent, text, command, color, hover_color):
        btn = tk.Button(
            parent, text=text, command=command,
            font=("Courier New", 12, "bold"),
            fg=WHITE, bg=color,
            activeforeground=WHITE, activebackground=hover_color,
            relief="flat", cursor="hand2", padx=20, pady=8, bd=0
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    make_button(btn_frame, "Cancel",   on_cancel,  BTN_BG,     BTN_HOV).pack(side="left")
    make_button(btn_frame, "Launch →", on_launch,  BTN_LAUNCH, BTN_LAUNCH_HOV).pack(side="right")

    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")
    root.mainloop()

    print(repr(result["vehicle"]))
    print(repr(result["map"]))


    if result["cancelled"]:
        print("Cancelled.")
        sys_exit(0)

    return result["vehicle"], result["map"], result["mode"]


# ── CLI args ───────────────────────────────────────────────────────────────────
parser = ArgumentParser(description="CARLA Demo Launcher")
parser.add_argument('-a', action='store_true', help='Run automated demo.')
parser.add_argument('-v', type=str, default=None, help='Vehicle csv name.')
parser.add_argument('-d', action='store_true', help='Debug mode.')
parser.add_argument('--no-prompt', action='store_true', help='Skip GUI.')
args_dict = vars(parser.parse_args())

server_only  = False
selected_map = None
auto_mode    = False
vehicle_key  = None

# ── Show selection GUI ─────────────────────────────────────────────────────────
if not args_dict.get('no_prompt'):
    vehicle_key, selected_map, mode = show_selection_window()
    args_dict['v'] = vehicle_key
    if mode == "auto":
        auto_mode = True
    elif mode == "server_only":
        server_only = True

# ── Open progress window ───────────────────────────────────────────────────────
progress = ProgressWindow()

# ── Step 1: Port cleanup ───────────────────────────────────────────────────────
progress.advance("NOT Cleaning up old processes and ports...")
cleanup_ports(progress)

# ── Step 2: Start CARLA server ─────────────────────────────────────────────────
progress.advance("Launching CARLA server...")
server_log = open(os.path.expanduser("~/server_debug.log"), "w")
#Popen(
#    ["bash", "server-build.sh"],
#    cwd=PATH_TO_HELPER_SCRIPTS,
#    stdout=server_log,
#    stderr=server_log
#)
process = subprocess.Popen(
    [SERVER_EXECUTABLE, f"{selected_map}?listen", "-log"],
    cwd=PATH_TO_HELPER_SCRIPTS,
    stdout=server_log,
    stderr=server_log
)
#subprocess.Popen([SERVER_EXECUTABLE, f"{map_name}?listen", "-log"])

if server_only:
    progress.set_status("Server Only — Carla build loading.")
    for _ in range(len(progress.steps) - 1):
        progress.advance()
    progress.complete()
    sys_exit(0)

# ── Step 3: Wait for packaged build to boot ───────────────────────────────────
progress.advance("Waiting for CARLA server to boot...")
sleep(EXPECTED_TIME_UNTIL_WINDOW_APPEARANCE)  # keep this, packaged builds still take time to load

# ── Step 4: Press Play ────────────────────────────────────────────────────────
progress.set_status("Skipped step original 4")

# ── Step 5: Load map (skip for Town10) ───────────────────────────────────────
#progress.advance(f"Loading map: {selected_map}...")
#if selected_map:
#    if selected_map in TOWN10_MAPS: // THIS VARIABLE HAS BEEN DELETED
#        progress.set_status("Town 10 — skipping reload to preserve custom assets.")
#        sleep(5)
#    else:
#        sleep(10)
#        load_map(selected_map, progress)
#        sleep(5)

#progress.set_status("Skipping map load")
# ── Step 6: Wait to settle ────────────────────────────────────────────────────
progress.advance("Waiting for simulation to settle...")
for i in range(WAIT_BEFORE_CLIENT_START, 0, -5):
    progress.set_status(f"Starting in {i} seconds...")
    sleep(5)

# ── Step 7: Start driving program ─────────────────────────────────────────────
progress.advance("Starting driving program...")
progress.complete()

threading.Thread(target=focus_pygame_window, daemon=True).start()

if auto_mode:
    vehicle_id = VEHICLE_IDS.get(vehicle_key, "vehicle.tesla.model3")
    command_args = ["python", "automatic_control.py", "--filter", vehicle_id]
    run_simulation(command_args, cwd=PROJECT_ROOT)
else:
    charger_file = CHARGER_FILES.get(selected_map, "Town10_intersection_chargers")
    command_args = ["bash", "client.sh", "-v", vehicle_key, "-c", charger_file]
    if args_dict.get('d'):
        command_args.append("-d")
    run_simulation(command_args, cwd=PATH_TO_HELPER_SCRIPTS)
