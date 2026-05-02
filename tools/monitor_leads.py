import subprocess
import json
import os
import time
from win10toast import ToastNotifier

toaster = ToastNotifier()

def run_step(script):
    try:
        # We use 'python' to ensure it opens in the foreground terminal when triggered by messenger
        subprocess.run(["python", script], check=True)
        return True
    except Exception as e:
        print(f"Error executing {script}: {e}")
        return False

def get_total_leads():
    try:
        subprocess.run(["python", "tools/fetch_leads.py"], check=True, capture_output=True)
        if os.path.exists(".tmp/raw_leads.json"):
            with open(".tmp/raw_leads.json", "r") as f:
                data = json.load(f)
                return len(data.get("values", [])) - 1
    except:
        pass
    return 0

def main():
    print("--------------------------------------------------")
    print("   AI AGENT REVENUE SYSTEM - BACKGROUND MONITOR   ")
    print("--------------------------------------------------")

    last_count = get_total_leads()
    print(f"[*] Initial sync complete. Monitoring '{last_count}' existing leads.")
    print("[*] Polling every 10 minutes. This window can be minimized.")

    while True:
        time.sleep(600)
        current_count = get_total_leads()

        if current_count > last_count:
            new_leads = current_count - last_count

            # 1. Desktop Notification
            toaster.show_toast(
                "🚀 New Lead Received!",
                f"You have {new_leads} new prospect(s). Opening the Master Console now...",
                duration=10,
                threaded=True
            )

            # 2. Trigger the Interactive Console for the user to choose
            # We use 'start' to bring the interactive console to the foreground
            subprocess.run("start python tools/master_console.py", shell=True)

            last_count = current_count
        else:
            # Simple heartbeat log
            t = time.strftime("%H:%M:%S", time.localtime())
            print(f"[{t}] Monitoring: No new activity.")

if __name__ == "__main__":
    main()
