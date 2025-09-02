import requests
import time
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

def fetch_conversation_names(access_token):
    url = "https://graph.facebook.com/v20.0/me/conversations"
    params = {
        "fields": "id,name,participants",
        "limit": 5,   # सिर्फ top 5 दिखाने के लिए
        "access_token": access_token
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        table = Table(title="💬 Messenger Conversations", style="bold cyan")
        table.add_column("Conversation ID", style="green", no_wrap=True)
        table.add_column("Name", style="yellow")
        table.add_column("Members", style="magenta")

        console.print("\n✨ Fetching your conversations...\n", style="bold blue")

        # Animation effect
        for convo in track(data.get("data", []), description="Loading Conversations..."):
            time.sleep(0.5)  # थोड़ा delay stylish effect के लिए
            convo_id = convo["id"]
            convo_name = convo.get("name", "No Name (Direct Chat)")
            members = [p["name"] for p in convo["participants"]["data"]]
            table.add_row(convo_id, convo_name, ", ".join(members))

        console.print(table)
    else:
        console.print("❌ Error:", response.json(), style="bold red")

if __name__ == "__main__":
    token = input("👉 Enter your Facebook Access Token: ").strip()
    fetch_conversation_names(token)
