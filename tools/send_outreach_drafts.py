import subprocess
import json
import os
import base64

def run_gws_json(command):
    env = os.environ.copy()
    env.pop("GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE", None)

    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, env=env)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        return True
    except Exception as e:
        return False

def create_raw_message(to, subject, body):
    message_text = f"To: {to}\r\nSubject: {subject}\r\nContent-Type: text/plain; charset=\"utf-8\"\r\n\r\n{body}"
    return base64.urlsafe_b64encode(message_text.encode("utf-8")).decode("utf-8")

def main():
    if not os.path.exists(".tmp/outreach_drafts.json"):
        print("Outreach drafts data not found.")
        return

    with open(".tmp/outreach_drafts.json", "r") as f:
        drafts = json.load(f)

    print(f"Preparing to create {len(drafts)} drafts in Gmail...")

    for draft in drafts:
        raw = create_raw_message(draft["email"], draft["subject"], draft["body"])

        # Body maps to 'message' which contains 'raw'
        body_json = {
            "message": {
                "raw": raw
            }
        }

        # Correct GWS CLI syntax: service resource resource method
        # Using space separated commands
        cmd = f'gws gmail:v1 users drafts create --params "{{\\"userId\\":\\"me\\"}}" --json "{json.dumps(body_json).replace('"', '\\"')}"'

        print(f"Creating draft for {draft['email']}...")
        if run_gws_json(cmd):
            print(f"Successfully created draft for {draft['name']}.")
        else:
            print(f"Failed to create draft for {draft['name']}.")

if __name__ == "__main__":
    main()
