#!/usr/bin/env python3
"""
Remerge charger files using ONLY spawn + junction chargers.
Removes road chargers (every lane meter) which are unrealistic.
Deletes old merged files and creates new cleaner merged files.
"""

import os
import shutil

PROJECT_ROOT = os.path.expanduser("~/carla-energy-consumption")
EXAMPLES_DIR = os.path.join(PROJECT_ROOT, "input", "examples")
CHARGERS_DIR = os.path.join(EXAMPLES_DIR, "chargers")

MAPS = {
    "Town01":   "Town01",
    "Town02":   "Town02",
    "Town03":   "Town03",
    "Town04":   "Town04",
    "Town05":   "Town05",
    "Town06":   "Town06",
    "Town07":   "Town07",
    "Town10HD": "Town10HD",
}

OLD_FILES = [
    "Town01_intersection_chargers.csv",
    "Town02_intersection_chargers.csv",
    "Town03_intersection_chargers.csv",
    "Town04_intersection_chargers.csv",
    "Town05_intersection_chargers.csv",
    "Town06_intersection_chargers.csv",
    "Town07_intersection_chargers.csv",
    "Town10_intersection_chargers.csv",
    "Town10HD_intersection_chargers.csv",
]


def merge_csv_files(files, output_path):
    header = None
    all_rows = []
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"    Skipping missing: {os.path.basename(filepath)}")
            continue
        with open(filepath, 'r') as f:
            lines = [l for l in f.readlines() if l.strip()]
        if not lines:
            continue
        if header is None:
            header = lines[0]
        all_rows.extend(lines[1:])
    if not header or not all_rows:
        return 0, "No data to merge"
    with open(output_path, 'w') as f:
        f.write(header)
        f.writelines(all_rows)
    return len(all_rows), None


def main():
    print("CARLA Charger Remerger — Spawn + Junction Only")
    print("=" * 50)

    # Step 1 — Delete old merged files from examples
    print("\nStep 1 — Deleting old merged files from input/examples/...")
    for filename in OLD_FILES:
        path = os.path.join(EXAMPLES_DIR, filename)
        if os.path.exists(path):
            os.remove(path)
            print(f"  Deleted: {filename}")
        else:
            print(f"  Not found (skipping): {filename}")

    # Step 2 — Delete old combined files inside chargers folders
    print("\nStep 2 — Deleting old combined files in chargers/...")
    for map_short, folder_name in MAPS.items():
        combined = os.path.join(CHARGERS_DIR, folder_name, f"{folder_name}_combined_chargers.csv")
        if os.path.exists(combined):
            os.remove(combined)
            print(f"  Deleted: chargers/{folder_name}/{folder_name}_combined_chargers.csv")

    # Step 3 — Remerge spawn + junction only
    print("\nStep 3 — Merging spawn + junction chargers only...")
    results = {}

    for map_short, folder_name in MAPS.items():
        map_dir = os.path.join(CHARGERS_DIR, folder_name)
        if not os.path.exists(map_dir):
            print(f"\n  {map_short}: folder not found — skipping")
            results[map_short] = 0
            continue

        print(f"\n  {map_short}:")
        files_to_merge = []

        # Spawn chargers
        spawn_path = os.path.join(map_dir, f"{folder_name}_spawn_chargers.csv")
        if os.path.exists(spawn_path):
            lines = sum(1 for _ in open(spawn_path)) - 1
            files_to_merge.append(spawn_path)
            print(f"    + spawn_chargers.csv ({lines} chargers)")
        else:
            print(f"    - spawn_chargers.csv NOT FOUND")

        # Junction chargers
        junction_all = os.path.join(map_dir, f"{folder_name}_all_junction_chargers.csv")
        if os.path.exists(junction_all):
            lines = sum(1 for _ in open(junction_all)) - 1
            files_to_merge.append(junction_all)
            print(f"    + all_junction_chargers.csv ({lines} chargers)")
        else:
            print(f"    - all_junction_chargers.csv NOT FOUND")

        print(f"    - road_chargers SKIPPED (unrealistic)")

        if not files_to_merge:
            print(f"    No files — skipping")
            results[map_short] = 0
            continue

        # Merge
        combined_path = os.path.join(map_dir, f"{folder_name}_combined_chargers.csv")
        total, err = merge_csv_files(files_to_merge, combined_path)

        if err:
            print(f"    ERROR: {err}")
            results[map_short] = 0
            continue

        print(f"    = {total} total chargers")
        results[map_short] = total

        # Copy to examples folder
        if map_short == "Town10HD":
            target_names = [
                "Town10HD_intersection_chargers.csv",
                "Town10_intersection_chargers.csv",
            ]
        else:
            target_names = [f"{map_short}_intersection_chargers.csv"]

        for name in target_names:
            shutil.copy(combined_path, os.path.join(EXAMPLES_DIR, name))
            print(f"    Saved: input/examples/{name}")

    # Summary
    print("\n── Summary ──")
    total_all = 0
    for map_short, count in results.items():
        print(f"  {'✓' if count > 0 else '✗'} {map_short}: {count} chargers")
        total_all += count
    print(f"\n  Total: {total_all} chargers across all maps")
    print(f"\nDone!")


if __name__ == '__main__':
    main()
