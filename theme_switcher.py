import argparse
import json
import subprocess
import shutil
import os
from pathlib import Path

img_extensions = (".jpg", ".jpeg", ".png", ".webp")

themes_dir = Path(__file__).resolve().parent / "themes/" 

current_path = Path(__file__).resolve().parent / "current.json"


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest="command") # so each subparse is called a "command"

subparsers.add_parser(
    "list",
    help="Lists your available themes."
)

set_parser = subparsers.add_parser(
    "set",
    help="Sets your theme to one of the available themes. e.g set example"
)
set_parser.add_argument("theme")

args = parser.parse_args()

if args.command == "list":
    print("list initiated")

if args.command == "set":
    selected_theme = args.theme
    scheme_path = themes_dir / selected_theme / f"{selected_theme}.json"

    theme_files = os.listdir(themes_dir / selected_theme)

    for file in theme_files:
        if file.endswith(img_extensions):
            selected_wallpaper = file

    wall_path = themes_dir / selected_theme / selected_wallpaper
    
    subprocess.run([
        "hyprctl",
        "hyprpaper",
        "wallpaper",
        f",{wall_path}"
    ])

    print(f"Wallpaper set to {selected_theme}!")

    shutil.copyfile(scheme_path, current_path)

    subprocess.run([
        "qs",
        "ipc",
        "call",
        "shell",
        "reload",
    ])

    print(f"Colours set to {selected_theme}")
