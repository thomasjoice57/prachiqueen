import requests
import time
import sys
import os
import random
import threading
from platform import system
from getpass import getpass
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

# ------------------- COLORS & BANNER -------------------
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"

BANNER = f"""
{Colors.YELLOW}{Colors.BOLD}
/$$$$$$$$ /$$   /$$  /$$$$$$   /$$$$$$  /$$      
| $$_____/| $$  | $$ /$$__  $$ /$$__  $$| $$      
| $$      | $$  | $$| $$  \__/| $$  \ $$| $$      
| $$$$$   | $$  | $$| $$ /$$$$| $$$$$$$$| $$      
| $$__/   | $$  | $$| $$|_  $$| $$__  $$| $$      
| $$      | $$  | $$| $$  \ $$| $$  | $$| $$      
| $$      |  $$$$$$/|  $$$$$$/| $$  | $$| $$$$$$$$
|__/       \______/  \______/ |__/  |__/|________/
                                                  
🌟 Multi-Tool Script: POST / MESSENGER / TOKEN TO UID 🌟
{Colors.RESET}
"""

def separator():
    print(f"{Colors.YELLOW}{'═'*60}{Colors.RESET}")

def clear_screen():
    os.system('cls' if system() == 'Windows' else 'clear')

# ------------------- TOKEN TO UID TOOL -------------------
def token_to_uid():
    clear_screen()
    console.print(BANNER)
    console.print("\n[bold cyan]💬 TOKEN TO UID TOOL[/bold cyan]")
    separator()
    token = input("👉 Enter your Facebook Access Token: ").strip()
    url = "https://graph.facebook.com/v20.0/me/conversations"
    params = {
        "fields": "id,name,participants",
        "limit": 5,
        "access_token": token
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            table = Table(title="💬 Messenger Conversations", style="bold cyan")
            table.add_column("Conversation ID", style="green", no_wrap=True)
            table.add_column("Name", style="yellow")
            table.add_column("Members", style="magenta")

            console.print("\n✨ Fetching your conversations...\n", style="bold blue")
            for convo in track(data.get("data", []), description="Loading Conversations..."):
                time.sleep(0.5)
                convo_id = convo["id"]
                convo_name = convo.get("name", "No Name (Direct Chat)")
                members = [p["name"] for p in convo["participants"]["data"]]
                table.add_row(convo_id, convo_name, ", ".join(members))
            console.print(table)
        else:
            console.print("❌ Error: " + str(response.json()), style="bold red")
    except Exception as e:
        console.print(f"❌ Error occurred: {e}", style="bold red")
    input("\nPress Enter to return to main menu...")

# ------------------- POST TOOL -------------------
def post_tool():
    clear_screen()
    console.print(BANNER)
    console.print("\n[bold cyan]🚀 POST TOOL[/bold cyan]")
    separator()

    # Password
    password = getpass("Enter password: ")
    confirm_password = getpass("Confirm password: ")
    if password != confirm_password:
        console.print("❌ Passwords do not match!", style="bold red")
        return
    console.print("✅ Password confirmed.", style="bold green")
    separator()

    # Post IDs
    post_ids_input = input("Enter post IDs (comma-separated): ")
    post_ids = [p.strip() for p in post_ids_input.split(',') if p.strip()]
    if not post_ids:
        console.print("❌ No valid post IDs!", style="bold red")
        return

    # Speed
    try:
        speed = int(input("Enter delay between posts (seconds): "))
        if speed < 0:
            raise ValueError
    except ValueError:
        console.print("❌ Invalid speed!", style="bold red")
        return

    # Comment files
    comment_files_input = input("Enter comment file paths (comma-separated): ")
    comment_files = [f.strip() for f in comment_files_input.split(',') if f.strip()]
    comments = []
    for f in comment_files:
        try:
            with open(f, 'r') as file:
                comments.extend([line.strip() for line in file.readlines() if line.strip()])
        except:
            console.print(f"⚠️ Comment file {f} not found, skipping.", style="bold yellow")
    if not comments:
        console.print("❌ No comments loaded!", style="bold red")
        return

    # Token file
    token_file = input("Enter token file path: ").strip()
    try:
        with open(token_file, 'r') as f:
            tokens = [t.strip() for t in f.readlines() if t.strip()]
    except:
        console.print(f"❌ Token file {token_file} not found!", style="bold red")
        return
    if not tokens:
        console.print("❌ No tokens loaded!", style="bold red")
        return

    # Headers
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    console.print("\n🚀 Starting posting process...\n", style="bold purple")
    while True:
        for idx, comment in enumerate(comments):
            post_id = random.choice(post_ids)
            token = random.choice(tokens)
            url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
            params = {"access_token": token, "message": comment}
            try:
                response = requests.post(url, json=params, headers=headers)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if response.ok:
                    console.print(f"✅ [{now}] Posted comment: {comment}", style="bold green")
                else:
                    console.print(f"❌ [{now}] Failed to post comment: {comment}", style="bold red")
            except Exception as e:
                console.print(f"❌ Error: {e}", style="bold red")
            time.sleep(speed)

# ------------------- MESSENGER TOOL -------------------
def messenger_tool():
    clear_screen()
    console.print(BANNER)
    console.print("\n[bold cyan]💌 MESSENGER TOOL[/bold cyan]")
    separator()

    # Password
    password = getpass("Enter password: ")
    confirm_password = getpass("Confirm password: ")
    if password != confirm_password:
        console.print("❌ Passwords do not match!", style="bold red")
        return
    console.print("✅ Password confirmed.", style="bold green")
    separator()

    # Haters name
    haters_name = input("Enter name prefix for messages: ").strip()
    if not haters_name:
        console.print("❌ Name cannot be empty!", style="bold red")
        return

    # Convo IDs
    convo_ids_input = input("Enter conversation IDs (comma-separated): ")
    convo_ids = [c.strip() for c in convo_ids_input.split(',') if c.strip()]
    if not convo_ids:
        console.print("❌ No valid conversation IDs!", style="bold red")
        return

    # Speed
    try:
        speed = int(input("Enter delay between messages (seconds): "))
        if speed < 0:
            raise ValueError
    except ValueError:
        console.print("❌ Invalid speed!", style="bold red")
        return

    # Message files
    message_files_input = input("Enter message file paths (comma-separated): ")
    messages = []
    for f in [f.strip() for f in message_files_input.split(',') if f.strip()]:
        try:
            with open(f, 'r') as file:
                messages.extend([line.strip() for line in file.readlines() if line.strip()])
        except:
            console.print(f"⚠️ File {f} not found, skipping.", style="bold yellow")
    if not messages:
        console.print("❌ No messages loaded!", style="bold red")
        return

    # Token file
    token_file = input("Enter token file path: ").strip()
    try:
        with open(token_file, 'r') as f:
            tokens = [t.strip() for t in f.readlines() if t.strip()]
    except:
        console.print(f"❌ Token file {token_file} not found!", style="bold red")
        return
    if not tokens:
        console.print("❌ No tokens loaded!", style="bold red")
        return

    console.print("\n🚀 Starting messaging process...\n", style="bold purple")
    while True:
        for idx, message in enumerate(messages):
            token = random.choice(tokens)
            convo_id = random.choice(convo_ids)
            url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
            params = {"access_token": token, "message": f"{haters_name} {message}"}
            try:
                response = requests.post(url, json=params)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if response.ok:
                    console.print(f"✅ [{now}] Sent message: {message}", style="bold green")
                else:
                    console.print(f"❌ [{now}] Failed to send: {message}", style="bold red")
            except Exception as e:
                console.print(f"❌ Error: {e}", style="bold red")
            time.sleep(speed)

# ------------------- MAIN MENU -------------------
def main_menu():
    while True:
        clear_screen()
        console.print(BANNER)
        console.print("\n[bold cyan]Select a Tool:[/bold cyan]")
        console.print("[1] 🚀 POST TOOL")
        console.print("[2] 💌 MESSENGER TOOL")
        console.print("[3] 💬 TOKEN TO UID TOOL")
        console.print("[0] ❌ Exit")
        choice = input("\nEnter choice: ").strip()
        if choice == "1":
            post_tool()
        elif choice == "2":
            messenger_tool()
        elif choice == "3":
            token_to_uid()
        elif choice == "0":
            console.print("👋 Exiting... Goodbye!", style="bold yellow")
            sys.exit(0)
        else:
            console.print("❌ Invalid choice! Try again.", style="bold red")
            time.sleep(1)

# ------------------- RUN -------------------
if __name__ == "__main__":
    main_menu()
