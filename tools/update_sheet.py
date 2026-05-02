import subprocess
import json
import os
import sys

def run_gws_json(command):
    env = os.environ.copy()
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, env=env)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        return json.loads(result.stdout)
    except:
        return None

def main():
    if not os.path.exists(".tmp/scored_leads.json"):
        print("Scored leads file not found.")
        return

    with open(".tmp/scored_leads.json", "r") as f:
        data = json.load(f)

    sheet_id = data["sheet_id"]
    all_values = data["values"] # This is the full table [headers + data]

    # 1. Separate the AI data from the form data
    # We only want to update columns F and G (Score and Recommendation)
    # the 'all_values' table from score_leads.py has [original_cols + Score + Recommendation]
    ai_only_values = []
    for row in all_values:
        # We take the last two items (Score and Recommendation)
        ai_only_values.append([row[-2], row[-1]])

    # 2. Get the actual sheet name
    metadata_cmd = f'gws sheets:v4 spreadsheets get --params "{{\\"spreadsheetId\\":\\"{sheet_id}\\"}}"'
    metadata = run_gws_json(metadata_cmd)
    sheet_name = metadata["sheets"][0]["properties"]["title"] if metadata else "Sheet1"

    print(f"Updating AI columns in '{sheet_name}'...")

    # 3. Update only columns F and G
    # Column F is the 6th column, G is the 7th. Range is F1:G
    params = {
        "spreadsheetId": sheet_id,
        "range": f"'{sheet_name}'!F1:G",
        "valueInputOption": "USER_ENTERED"
    }
    body = {
        "values": ai_only_values
    }

    update_cmd = f'gws sheets:v4 spreadsheets values update --params "{json.dumps(params).replace('"', '\\"')}" --json "{json.dumps(body).replace('"', '\\"')}"'

    env = os.environ.copy()
    res = subprocess.run(update_cmd, capture_output=True, text=True, shell=True, env=env)

    if res.returncode == 0:
        print("AI Columns (Score & Recommendation) updated 100% successfully.")
    else:
        print(f"Failed to update columns: {res.stderr}")

if __name__ == "__main__":
    main()
