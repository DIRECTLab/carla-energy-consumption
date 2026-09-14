#!/usr/bin/env python3
"""
Generate ALL types of charger CSV files for all CARLA maps.
Run this with Unreal Editor open and Play pressed.

For each map generates:
  chargers/Town01/
    Town01_spawn_chargers.csv       — chargers at vehicle spawn points
    Town01_all_junction_chargers.csv — all junction chargers combined
    junction_chargers/               — per-junction charger files
    road_chargers/                   — per-road-lane charger files
    Town01_combined_chargers.csv     — ALL charger types merged (used by client.sh)

  input/examples/Town01_intersection_chargers.csv  — symlinked to combined file

Note: optimal_chargers.py requires simulation data — run separately after
collecting driving data with multitracking.py.
"""

import os
import sys
import time
import shutil
import tkinter as tk
from subprocess import run as run_sub, PIPE

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT   = os.path.expanduser("~/carla-energy-consumption")
INPUT_DIR      = os.path.join(PROJECT_ROOT, "input")
EXAMPLES_DIR   = os.path.join(INPUT_DIR, "examples")
CREATION_DIR   = os.path.join(INPUT_DIR, "creation")
CHARGERS_DIR   = os.path.join(EXAMPLES_DIR, "chargers")

# ── Map config ─────────────────────────────────────────────────────────────────
MAPS = [
    "Town01_Opt",
    "Town02_Opt",
    "Town03_Opt",
    "Town04_Opt",
    "Town05_Opt",
    "Town06_Opt",
    "Town07_Opt",
    "Town10HD_Opt",
]

# Charger parameters
CHARGER_LENGTH     = 2.0
CHARGER_WIDTH      = 1.0
CHARGER_POWER      = 100000
CHARGER_EFFICIENCY = 0.95
CHARGER_COUNT      = 50
CHARGER_SEED       = 0
MAP_SETTLE_TIME    = 15

# ── Progress window ────────────────────────────────────────────────────────────
class ProgressWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CARLA Charger Generator")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        BG   = "#1a1a2e"
        CYAN = "#00d4ff"
        GREY = "#888888"

        self.root.configure(bg=BG)

        tk.Label(self.root, text="CARLA Charger Generator",
                 font=("Courier New", 14, "bold"), fg=CYAN, bg=BG).pack(pady=(15, 5))
        tk.Frame(self.root, bg="#0f3460", height=2).pack(fill="x", padx=20)

        self.map_frame = tk.Frame(self.root, bg=BG, padx=20, pady=10)
        self.map_frame.pack(fill="x")

        self.map_labels = []
        for map_name in MAPS:
            row = tk.Frame(self.map_frame, bg=BG)
            row.pack(fill="x", pady=1)
            indicator = tk.Label(row, text="○", font=("Courier New", 11),
                                 fg=GREY, bg=BG, width=2)
            indicator.pack(side="left")
            label = tk.Label(row, text=map_name,
                             font=("Courier New", 10), fg=GREY, bg=BG, anchor="w")
            label.pack(side="left")

            step_frame = tk.Frame(row, bg=BG)
            step_frame.pack(side="right")
            step_labels = []
            for step_name in ["spawn", "junction", "roads", "merge"]:
                sl = tk.Label(step_frame, text=f"[{step_name}]",
                              font=("Courier New", 8), fg=GREY, bg=BG)
                sl.pack(side="left", padx=2)
                step_labels.append(sl)

            self.map_labels.append((indicator, label, step_labels))

        tk.Frame(self.root, bg="#0f3460", height=1).pack(fill="x", padx=20, pady=5)

        self.status_var = tk.StringVar(value="Starting...")
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Courier New", 9), fg=GREY, bg=BG).pack(pady=(0, 15))

        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"+{sw - self.root.winfo_width() - 40}+40")
        self._keep_running = True
        self._update()

    def _update(self):
        if self._keep_running:
            self.root.update()
            self.root.after(100, self._update)

    def mark_map_active(self, index):
        indicator, label, _ = self.map_labels[index]
        indicator.config(text="►", fg="#ffcc00")
        label.config(fg="#ffcc00")
        self.root.update()

    def mark_map_done(self, index):
        indicator, label, _ = self.map_labels[index]
        indicator.config(text="✓", fg="#00d4ff")
        label.config(fg="#e8e8e8")
        self.root.update()

    def mark_map_error(self, index):
        indicator, label, _ = self.map_labels[index]
        indicator.config(text="✗", fg="#ff4444")
        label.config(fg="#ff4444")
        self.root.update()

    def mark_step(self, map_index, step_index, status):
        _, _, step_labels = self.map_labels[map_index]
        colors = {
            "done":   "#00d4ff",
            "error":  "#ff4444",
            "active": "#ffcc00",
            "skip":   "#555555"
        }
        step_labels[step_index].config(fg=colors.get(status, "#888888"))
        self.root.update()

    def set_status(self, text):
        self.status_var.set(text)
        self.root.update()

    def complete(self):
        self.set_status("All maps complete!")
        time.sleep(3)
        self.close()

    def close(self):
        self._keep_running = False
        try:
            self.root.destroy()
        except Exception:
            pass


# ── Helper: run script capturing stdout to file ────────────────────────────────
def run_to_file(cmd, output_path):
    result = run_sub(cmd, stdout=PIPE, stderr=PIPE, text=True, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        return False, result.stderr.strip()
    output = result.stdout.strip()
    if not output or "front_left" not in output:
        return False, f"No charger data. stderr: {result.stderr[:100]}"
    with open(output_path, 'w') as f:
        f.write(output + "\n")
    return True, None


def run_to_folder(cmd, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    result = run_sub(cmd, stdout=PIPE, stderr=PIPE, text=True, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        return False, result.stderr.strip()
    return True, None


# ── Merge all CSVs into one combined file ──────────────────────────────────────
def merge_charger_files(files_to_merge, output_path):
    """
    Merges multiple charger CSV files into one combined file.
    Keeps header from first file, appends data rows from all files.
    """
    header = None
    all_rows = []

    for filepath in files_to_merge:
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r') as f:
            lines = f.readlines()
        if not lines:
            continue
        if header is None:
            header = lines[0]
        # Add data rows (skip header)
        all_rows.extend(lines[1:])

    if header is None or not all_rows:
        return False, "No data to merge"

    with open(output_path, 'w') as f:
        f.write(header)
        f.writelines(all_rows)

    return True, None


def merge_folder_csvs(folder, output_path):
    """Merge all CSV files in a folder into one file."""
    if not os.path.exists(folder):
        return False, "Folder does not exist"
    csv_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.csv')]
    if not csv_files:
        return False, "No CSV files in folder"
    return merge_charger_files(csv_files, output_path)


# ── Charger generators ─────────────────────────────────────────────────────────
def gen_spawn_chargers(map_name, out_path, progress, map_idx):
    progress.mark_step(map_idx, 0, "active")
    progress.set_status(f"Generating spawn chargers for {map_name}...")

    cmd = [
        sys.executable,
        os.path.join(CREATION_DIR, "charger_options.py"),
        str(CHARGER_LENGTH), str(CHARGER_WIDTH),
        "-m", map_name,
        "--power", str(CHARGER_POWER),
        "--efficiency", str(CHARGER_EFFICIENCY),
        "-n", str(CHARGER_COUNT),
        "--seed", str(CHARGER_SEED),
    ]

    success, err = run_to_file(cmd, out_path)
    if success:
        lines = sum(1 for _ in open(out_path)) - 1
        print(f"    spawn: {lines} chargers")
        progress.mark_step(map_idx, 0, "done")
    else:
        print(f"    spawn ERROR: {err}")
        progress.mark_step(map_idx, 0, "error")
    return success


def gen_junction_chargers(map_name, out_folder, out_all_path, progress, map_idx):
    progress.mark_step(map_idx, 1, "active")
    progress.set_status(f"Generating junction chargers for {map_name}...")

    cmd = [
        sys.executable,
        os.path.join(CREATION_DIR, "junction_chargers_all.py"),
        str(CHARGER_LENGTH), str(CHARGER_WIDTH),
        out_folder,
        "--power", str(CHARGER_POWER),
        "--efficiency", str(CHARGER_EFFICIENCY),
        "-m", map_name,
    ]

    success, err = run_to_folder(cmd, out_folder)
    if success:
        all_junctions_src = os.path.join(PROJECT_ROOT, "all_junctions.csv")
        if os.path.exists(all_junctions_src):
            shutil.move(all_junctions_src, out_all_path)
            lines = sum(1 for _ in open(out_all_path)) - 1
            print(f"    junction: {lines} chargers")
        progress.mark_step(map_idx, 1, "done")
    else:
        print(f"    junction ERROR: {err}")
        progress.mark_step(map_idx, 1, "error")
    return success


def gen_road_chargers(map_name, out_folder, progress, map_idx):
    progress.mark_step(map_idx, 2, "active")
    progress.set_status(f"Generating road chargers for {map_name}...")

    cmd = [
        sys.executable,
        os.path.join(CREATION_DIR, "chargers_all_roads.py"),
        str(CHARGER_LENGTH), str(CHARGER_WIDTH),
        out_folder,
        "--power", str(CHARGER_POWER),
        "--efficiency", str(CHARGER_EFFICIENCY),
        "-m", map_name,
    ]

    success, err = run_to_folder(cmd, out_folder)
    if success:
        road_files = len([f for f in os.listdir(out_folder) if f.endswith('.csv')])
        print(f"    roads: {road_files} files")
        progress.mark_step(map_idx, 2, "done")
    else:
        print(f"    roads ERROR: {err}")
        progress.mark_step(map_idx, 2, "error")
    return success


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("CARLA Complete Charger Generator")
    print("=" * 50)

    try:
        import carla
        print("CARLA Python API: OK")
    except ImportError:
        print("ERROR: CARLA Python API not found! Activate carlaclient-env.")
        sys.exit(1)

    os.makedirs(CHARGERS_DIR, exist_ok=True)
    os.makedirs(EXAMPLES_DIR, exist_ok=True)

    progress = ProgressWindow()

    for i, map_name in enumerate(MAPS):
        map_short = map_name.replace("_Opt", "")
        print(f"\n[{i+1}/{len(MAPS)}] Processing {map_name}...")

        progress.mark_map_active(i)
        progress.set_status(f"Processing {map_name}...")

        map_dir = os.path.join(CHARGERS_DIR, map_short)
        os.makedirs(map_dir, exist_ok=True)

        # Track which files were successfully generated for merging
        files_to_merge = []

        # ── 1. Spawn chargers ──────────────────────────────────────────────────
        spawn_path = os.path.join(map_dir, f"{map_short}_spawn_chargers.csv")
        if gen_spawn_chargers(map_name, spawn_path, progress, i):
            files_to_merge.append(spawn_path)

        # ── 2. Junction chargers ───────────────────────────────────────────────
        junction_folder = os.path.join(map_dir, "junction_chargers")
        junction_all_path = os.path.join(map_dir, f"{map_short}_all_junction_chargers.csv")
        if gen_junction_chargers(map_name, junction_folder, junction_all_path, progress, i):
            if os.path.exists(junction_all_path):
                files_to_merge.append(junction_all_path)

        # ── 3. Road chargers ───────────────────────────────────────────────────
        road_folder = os.path.join(map_dir, "road_chargers")
        road_merged_path = os.path.join(map_dir, f"{map_short}_all_road_chargers.csv")
        if gen_road_chargers(map_name, road_folder, progress, i):
            # Merge all road files into one
            merge_folder_csvs(road_folder, road_merged_path)
            if os.path.exists(road_merged_path):
                files_to_merge.append(road_merged_path)

        # ── 4. Merge all into combined file ────────────────────────────────────
        progress.mark_step(i, 3, "active")
        progress.set_status(f"Merging all chargers for {map_name}...")

        combined_path = os.path.join(map_dir, f"{map_short}_combined_chargers.csv")
        success, err = merge_charger_files(files_to_merge, combined_path)

        if success:
            total_lines = sum(1 for _ in open(combined_path)) - 1
            print(f"    combined: {total_lines} total chargers")
            progress.mark_step(i, 3, "done")

            # Copy combined file to examples folder as the main charger file
            # This is what client.sh -c will reference
            examples_path = os.path.join(EXAMPLES_DIR, f"{map_short}_intersection_chargers.csv")
            shutil.copy(combined_path, examples_path)
            print(f"    Saved to examples: {map_short}_intersection_chargers.csv")
        else:
            print(f"    merge ERROR: {err}")
            progress.mark_step(i, 3, "error")
            # Fall back to just the spawn chargers
            if os.path.exists(spawn_path):
                examples_path = os.path.join(EXAMPLES_DIR, f"{map_short}_intersection_chargers.csv")
                shutil.copy(spawn_path, examples_path)
                print(f"    Fallback: copied spawn chargers to examples")

        progress.mark_map_done(i)

        # Wait between maps
        if i < len(MAPS) - 1:
            for remaining in range(MAP_SETTLE_TIME, 0, -5):
                progress.set_status(f"Waiting {remaining}s before next map...")
                time.sleep(5)

    # Summary
    print("\n── Summary ──")
    for map_name in MAPS:
        map_short = map_name.replace("_Opt", "")
        combined = os.path.join(CHARGERS_DIR, map_short, f"{map_short}_combined_chargers.csv")
        examples = os.path.join(EXAMPLES_DIR, f"{map_short}_intersection_chargers.csv")
        combined_lines = (sum(1 for _ in open(combined)) - 1) if os.path.exists(combined) else 0
        print(f"  {map_short}: {combined_lines} combined chargers → {'✓' if os.path.exists(examples) else '✗'} examples")

    print(f"\nCharger files: {CHARGERS_DIR}")
    print(f"Client files:  {EXAMPLES_DIR}")
    print("\nNote: Run optimal_chargers.py separately after collecting simulation data.")

    progress.complete()


if __name__ == '__main__':
    main()
