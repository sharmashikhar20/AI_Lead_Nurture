import subprocess
import json
import os
import sys

def run_gws(command):
    # Use default environment
    env = os.environ.copy()

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            env=env
        )
        if result.returncode != 0:
            print(f"Error running gws: {result.stderr}")
            return None
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Exception: {str(e)}")
        return None

def main():
    print("Searching for 'Lead Form (Responses)' sheet...")
    # Search for the sheet
    search_cmd = 'gws drive files list --params "{\\"q\\":\\"name=\'Lead Form (Responses)\' and mimeType=\'application/vnd.google-apps.spreadsheet\'\\",\\"pageSize\\":1}"'
    search_data = run_gws(search_cmd)

    if not search_data or not search_data.get("files"):
        print("Sheet not found.")
        sys.exit(1)

    sheet_id = search_data["files"][0]["id"]
    print(f"Found sheet ID: {sheet_id}")

    # Fetch all values from the first sheet
    # Assuming standard 'Form Responses 1' or first sheet
    fetch_cmd = f'gws sheets:v4 spreadsheets values get --params "{{\\"spreadsheetId\\":\\"{sheet_id}\\",\\"range\\":\\"A:Z\\"}}"'
    sheet_data = run_gws(fetch_cmd)

    if not sheet_data or "values" not in sheet_data:
        print("No data found in sheet.")
        sys.exit(0)

    # Save to tmp
    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/raw_leads.json", "w") as f:
        json.dump({"sheet_id": sheet_id, "values": sheet_data["values"]}, f)

    print(f"Exported {len(sheet_data['values'])} rows to .tmp/raw_leads.json")

if __name__ == "__main__":
    main()
