import requests
import json
import time
import sys
from platform import system
import os
import http.server
import socketserver
import threading
import random

# ASCII art banner for styled output
BANNER = """
\033[1;93m
=============================================
       Fugal Messaging Script
=============================================
\033[0m
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Fugal Server Is Live")

def execute_server():
    PORT = 4000
    try:
        with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
            print(f"\033[1;94m[INFO] Server running at http://localhost:{PORT}\033[0m")
            httpd.serve_forever()
    except Exception as e:
        print(f"\033[1;91m[ERROR] Failed to start server: {e}\033[0m")
        sys.exit(1)

def send_messages():
    # Clear screen and display banner
    def cls():
        if system() == 'Linux':
            os.system('clear')
        elif system() == 'Windows':
            os.system('cls')

    cls()
    print(BANNER)

    # Separator for styled output
    def liness():
        print('\033[0;93m' + '═' * 50 + '\033[0m')

    # Prompt for password
    from getpass import getpass
    print("\033[1;94m[INPUT] Password Setup\033[0m")
    liness()
    password = getpass("Enter password: ")
    entered_password = getpass("Confirm password: ")
    if entered_password != password:
        print('\033[1;91m[-] Incorrect Password! Please try again.\033[0m')
        sys.exit(1)
    print("\033[1;92m[+] Password confirmed.\033[0m")
    liness()

    # Prompt for haters name
    print("\033[1;94m[INPUT] Haters Name\033[0m")
    liness()
    haters_name = input("Enter haters name (e.g., Hater): ").strip()
    if not haters_name:
        print("\033[1;91m[-] Haters name cannot be empty!\033[0m")
        sys.exit(1)
    print(f"\033[1;92m[+] Haters name set to: {haters_name}\033[0m")
    liness()

    # Prompt for conversation IDs
    print("\033[1;94m[INPUT] Conversation IDs\033[0m")
    liness()
    convo_ids_input = input("Enter conversation IDs (comma-separated, e.g., 123456789,987654321): ")
    convo_ids = [cid.strip() for cid in convo_ids_input.split(',') if cid.strip()]
    if not convo_ids:
        print("\033[1;91m[-] No valid conversation IDs provided!\033[0m")
        sys.exit(1)
    print(f"\033[1;92m[+] Conversation IDs: {', '.join(convo_ids)}\033[0m")
    liness()

    # Prompt for speed
    print("\033[1;94m[INPUT] Speed\033[0m")
    liness()
    try:
        speed = int(input("Enter speed (delay in seconds, e.g., 5): "))
        if speed < 0:
            raise ValueError("Speed must be non-negative!")
    except ValueError:
        print("\033[1;91m[-] Invalid speed value provided! Must be a non-negative integer.\033[0m")
        sys.exit(1)
    print(f"\033[1;92m[+] Speed set to: {speed} seconds\033[0m")
    liness()

    # Prompt for message file paths
    print("\033[1;94m[INPUT] Message Files\033[0m")
    liness()
    message_files_input = input("Enter message file paths (comma-separated, e.g., messages1.txt,messages2.txt): ")
    message_files = [file.strip() for file in message_files_input.split(',') if file.strip()]
    if not message_files:
        print("\033[1;91m[-] No valid message file paths provided!\033[0m")
        sys.exit(1)
    print(f"\033[1;92m[+] Message files: {', '.join(message_files)}\033[0m")
    liness()

    # Prompt for token file path
    print("\033[1;94m[INPUT] Token File\033[0m")
    liness()
    token_file = input("Enter token file path (e.g., tokennum.txt): ").strip()
    if not token_file:
        print("\033[1;91m[-] Token file path cannot be empty!\033[0m")
        sys.exit(1)
    print(f"\033[1;92m[+] Token file: {token_file}\033[0m")
    liness()

    # Read tokens from the specified file
    try:
        with open(token_file, 'r') as file:
            tokens = file.readlines()
    except FileNotFoundError:
        print(f"\033[1;91m[-] Token file {token_file} not found!\033[0m")
        sys.exit(1)
    access_tokens = [token.strip() for token in tokens if token.strip()]
    if not access_tokens:
        print(f"\033[1;91m[-] No valid tokens in {token_file}!\033[0m")
        sys.exit(1)
    num_tokens = len(access_tokens)
    print(f"\033[1;92m[+] Loaded {num_tokens} tokens\033[0m")
    liness()

    # Read messages from all message files
    messages = []
    for message_file in message_files:
        try:
            with open(message_file, 'r') as file:
                file_messages = file.readlines()
                messages.extend([msg.strip() for msg in file_messages if msg.strip()])
        except FileNotFoundError:
            print(f"\033[1;91m[-] Message file {message_file} not found! Skipping...\033[0m")
            continue
    if not messages:
        print("\033[1;91m[-] No valid messages found in any message files!\033[0m")
        sys.exit(1)
    print(f"\033[1;92m[+] Loaded {len(messages)} messages\033[0m")
    liness()

    # Set random_messages to True
    random_messages = True

    requests.packages.urllib3.disable_warnings()  # Warning: Insecure; consider enabling SSL

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    num_messages = len(messages)
    max_tokens = min(num_tokens, num_messages)

    print("\033[1;94m[INFO] Starting Messaging Process\033[0m")
    liness()

    def getName(token):
        try:
            data = requests.get(f'https://graph.facebook.com/v17.0/me?access_token={token}').json()
            return data.get('name', 'Error occurred')
        except:
            return "Error occurred"

    while True:
        try:
            # Shuffle messages if random_messages is True
            message_list = random.sample(messages, len(messages)) if random_messages else messages

            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = access_tokens[token_index]
                message = message_list[message_index % len(message_list)]
                convo_id = random.choice(convo_ids)

                url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
                parameters = {'access_token': access_token, 'message': f"{haters_name} {message}"}
                response = requests.post(url, json=parameters, headers=headers)

                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print(f"\033[1;35m[+] Message {message_index + 1}/{num_messages}")
                    print(f"    Convo ID: {convo_id}")
                    print(f"    Token: {token_index + 1}")
                    print(f"    Message: {haters_name} {message}")
                    print(f"\033[1;34m    Time: {current_time}\033[0m")
                    liness()
                else:
                    print(f"\033[1;92m[x] Failed Message {message_index + 1}/{num_messages}")
                    print(f"    Convo ID: {convo_id}")
                    print(f"    Token: {token_index + 1}")
                    print(f"    Message: {haters_name} {message}")
                    print(f"\033[1;34m    Time: {current_time}\033[0m")
                    liness()
                time.sleep(speed)

            print("\033[1;92m[+] All messages sent. Restarting the process...\033[0m")
            liness()
        except Exception as e:
            print(f"\033[1;91m[!] An error occurred: {e}\033[0m")
            liness()

def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()
    send_messages()

if __name__ == '__main__':
    main()