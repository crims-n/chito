import argparse
import json
import subprocess
import shutil
import os
import configparser
import time
from pathlib import Path

img_extensions = (".jpg", ".jpeg", ".png", ".webp")

base_dir = Path(__file__).resolve().parent

themes_dir = base_dir / "themes/" 

current_path = base_dir / "current.json"

config_file = base_dir / "config.cfg"

config = configparser.ConfigParser()

config.read(config_file)
wallhandler = config["settings"]["wallhandler"]

def get_paths(selected_theme):
    
    scheme_path = themes_dir / selected_theme / f"{selected_theme}.json"

    theme_files = os.listdir(themes_dir / selected_theme)

    for file in theme_files:
        if file.endswith(img_extensions):
            selected_wallpaper = file
            break

    wall_path = themes_dir / selected_theme / selected_wallpaper
    
    return scheme_path, wall_path

def set_themes():

    if wallhandler == "awww":
        subprocess.run([
            "awww",
            "img",
            "-t",
            "wipe",
            "--transition-fps",
            "60",
            f"{wall_path}"
        ])
    elif wallhandler == "hyprpaper":
        subprocess.run([
            "hyprctl",
            "hyprpaper",
            "wallpaper",
            f",{wall_path}"
    ])

    shutil.copyfile(scheme_path, current_path)

    subprocess.run([
        "qs",
        "ipc",
        "call",
        "shell",
        "reload",
    ])




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

subparsers.add_parser(
    "apply",
    help="Applies current theme. Intended to be used for autostart."
)

args = parser.parse_args()

if args.command == "list":
    themes_list = os.listdir(themes_dir)
    print("Available themes:", " ".join(themes_list))

if args.command == "set":
    selected_theme = args.theme
    scheme_path, wall_path = get_paths(selected_theme)
    
    config.read(config_file)
    config.set("current", "theme", selected_theme)

    with open(config_file, "w") as f:
        config.write(f)
        
    set_themes()


if args.command == "apply":
    config.read(config_file)
    selected_theme = config["current"]["theme"]
    scheme_path, wall_path = get_paths(selected_theme)

    if wallhandler == "awww":
        subprocess.Popen("awww-daemon")
    elif wallhandler == "hyprpaper":
        subprocess.run("hyprpaper")
    else:
        print(f"Invalid/unsupported wallpaper handler. ({wallhandler})")

    set_themes()



