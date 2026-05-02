import subprocess
import json
import os

def run_gws(command):
    env = os.environ.copy()
    env.pop("GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE", None)
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, env=env)
        return json.loads(result.stdout) if result.returncode == 0 else None
    except:
        return None

def create_doc(name, email, budget, field):
    title = f"Strategy Session - {name}"
    # Create the doc
    create_cmd = f'gws docs:v1 documents create --json "{{\\"title\\":\\"{title}\\"}}"'
    doc = run_gws(create_cmd)

    if not doc: return None

    doc_id = doc["documentId"]

    # Add content
    content = f"CLIENT STRATEGY BRIEF\n\nName: {name}\nEmail: {email}\nBudget: {budget}\nField: {field}\n\n## Pain Points\n- [TBD]\n\n## Proposed Strategy\n- [TBD]\n\n## Next Steps\n- [TBD]"

    update_params = {"documentId": doc_id}
    requests = {"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}

    update_cmd = f'gws docs:v1 documents batchUpdate --params "{json.dumps(update_params).replace('"', '\\"')}" --json "{json.dumps(requests).replace('"', '\\"')}"'
    run_gws(update_cmd)

    return f"https://docs.google.com/document/d/{doc_id}/edit"

def main():
    if not os.path.exists(".tmp/outreach_drafts.json"):
        print("Outreach data not found.")
        return

    with open(".tmp/outreach_drafts.json", "r") as f:
        leads = json.load(f)

    print("Creating Strategy Docs for Hot leads...")
    for lead in leads:
        # We need to know the score. Let's check scored_leads.json for the score attribute
        # Or better, generate_outreach could pass it. For now, we look for 'Hot' indicators in subject/body
        if "massive opportunity" in lead["body"] or "Hot" in lead.get("score", ""):
            url = create_doc(lead["name"], lead["email"], lead.get("budget", "N/A"), lead.get("field", "N/A"))
            if url:
                print(f"Doc created for {lead['name']}: {url}")

if __name__ == "__main__":
    main()
