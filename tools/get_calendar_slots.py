import subprocess
import json
import os
from datetime import datetime, timedelta

def run_gws_json(command):
    env = os.environ.copy()
    env.pop("GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE", None)
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, env=env)
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except:
        return None

def get_slots():
    # Looking for slots over the next 3 business days
    now = datetime.now()
    slots = []

    # We fetch events for the next 7 days to cover weekends/holidays
    time_min = now.isoformat() + "Z"
    time_max = (now + timedelta(days=7)).isoformat() + "Z"

    cmd = f'gws calendar events list --params "{{\\"calendarId\\":\\"primary\\",\\"timeMin\\":\\"{time_min}\\",\\"timeMax\\":\\"{time_max}\\",\\"singleEvents\\":true,\\"orderBy\\":\\"startTime\\"}}"'
    data = run_gws_json(cmd)

    busy_intervals = []
    if data and "items" in data:
        for event in data["items"]:
            start_info = event.get("start", {})
            end_info = event.get("end", {})

            # Handle both dateTime and all-day date events
            start_str = start_info.get("dateTime") or start_info.get("date")
            end_str = end_info.get("dateTime") or end_info.get("date")

            if start_str and end_str:
                # Clean strings for fromisoformat: 2026-05-02T09:00:00+05:30 -> 2026-05-02T09:00:00+05:30
                # fromisoformat handles +HH:MM in Python 3.7+
                busy_intervals.append((datetime.fromisoformat(start_str.replace('Z', '+00:00')),
                                      datetime.fromisoformat(end_str.replace('Z', '+00:00'))))

    # Scan next 5 days
    for i in range(1, 6):
        day = now + timedelta(days=i)
        if day.weekday() >= 5: continue

        day_str = day.strftime("%Y-%m-%d")
        # Ensure timezone awareness to match Google API
        tz_offset = datetime.now().astimezone().strftime('%z')
        window_start = datetime.fromisoformat(f"{day_str}T09:00:00{tz_offset}")
        window_end = datetime.fromisoformat(f"{day_str}T18:00:00{tz_offset}")

        current_check = window_start
        while current_check + timedelta(minutes=30) <= window_end:
            slot_start = current_check
            slot_end = current_check + timedelta(minutes=30)

            is_free = True
            for b_start, b_end in busy_intervals:
                # Buffer: slot must be 15m away from any event
                # [slot_start --- slot_end] [15m buffer] [b_start --- b_end]
                if not (slot_end + timedelta(minutes=15) <= b_start or slot_start - timedelta(minutes=15) >= b_end):
                    is_free = False
                    break

            if is_free:
                slots.append(slot_start.strftime("%A, %b %d at %I:%M %p"))
                if len(slots) >= 5: break

            current_check += timedelta(minutes=30) # Check every 30m for a 1h window
        if len(slots) >= 5: break

    with open(".tmp/available_slots.json", "w") as f:
        json.dump(slots, f)
    print(f"Found {len(slots)} available 1-hour slots.")

if __name__ == "__main__":
    get_slots()
