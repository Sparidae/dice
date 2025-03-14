# dice_cli.py
import argparse
import json
import random
import os
import sys
import time
from pathlib import Path

# Windows ANSI颜色支持初始化
if os.name == 'nt':
    from ctypes import windll, byref
    from ctypes.wintypes import DWORD

    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    STD_OUTPUT_HANDLE = -11

    hOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    dwMode = DWORD()
    windll.kernel32.GetConsoleMode(hOut, byref(dwMode))
    dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    windll.kernel32.SetConsoleMode(hOut, dwMode)

class Colors:
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

DATA_FILE = Path.home() / ".dice_data.json"

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(items):
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f, indent=2)

def add_item(new_item):
    items = load_data()
    if new_item not in items:
        items.append(new_item)
        save_data(items)
        print(f"🎉 {Colors.GREEN}{Colors.BOLD}Added: {new_item}{Colors.RESET}")
    else:
        print(f"🤔 {Colors.YELLOW}Item already exists!{Colors.RESET}")

def pick_animation():
    frames = [
        f"{Colors.DIM}🌀  Spinning...",
        f"{Colors.RESET}✨  Choosing...",
        f"{Colors.BOLD}🔥  Almost there..."
    ]
    for _ in range(3):
        for frame in frames:
            sys.stdout.write('\r' + frame)
            sys.stdout.flush()
            time.sleep(0.2)

def pick_item():
    items = load_data()
    if not items:
        print(f"{Colors.RED}No items found! Add some first.{Colors.RESET}")
        return
    
    pick_animation()
    selected = random.choice(items)
    print(f"\n\n{Colors.MAGENTA}{Colors.BOLD}🎲 Your destiny is:")
    print(f"{Colors.WHITE}{Colors.BOLD}>> {selected} <<{Colors.RESET}")
    print(f"\n{Colors.GREEN}🚀 Go have fun!{Colors.RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="DICE - Decision Maker for Interesting Choices",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add命令
    add_parser = subparsers.add_parser("add", help="Add new choice")
    add_parser.add_argument("item", type=str, help="Item to add")

    # Pick命令
    subparsers.add_parser("pick", help="Pick random item")

    args = parser.parse_args()

    if args.command == "add":
        if not args.item:
            print(f"{Colors.RED}Error: Must specify an item to add{Colors.RESET}")
            sys.exit(1)
        add_item(args.item.strip())
    elif args.command == "pick":
        pick_item()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
