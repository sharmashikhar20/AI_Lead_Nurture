import subprocess
import json
import os
import sys

def run_gws(command):
    env = os.environ.copy()
    env["GOOGLE_WORKSPACE_CLI_STORAGE"] = "plaintext"
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, env=env)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Exception: {str(e)}")
        return None

def main():
    print("Creating Google Form: 'Lead Enquiry Form'...")

    # 1. Create the Form
    create_params = {
        "info": {
            "title": "Lead Enquiry Form",
            "documentTitle": "Lead Enquiry Form"
        }
    }
    create_cmd = f'gws forms:v1 forms create --params "{json.dumps(create_params).replace('"', '\\"')}"'
    form = run_gws(create_cmd)

    if not form:
        print("Failed to create form.")
        return

    form_id = form["formId"]
    print(f"Form created! ID: {form_id}")

    # 2. Add Questions
    # We use batchUpdate to add all 4 items
    update_params = {
        "requests": [
            {
                "createItem": {
                    "item": {"title": "Name", "questionItem": {"question": {"required": True, "textQuestion": {}}}},
                    "location": {"index": 0}
                }
            },
            {
                "createItem": {
                    "item": {"title": "Email", "questionItem": {"question": {"required": True, "textQuestion": {}}}},
                    "location": {"index": 1}
                }
            },
            {
                "createItem": {
                    "item": {"title": "Budget", "questionItem": {"question": {"required": True, "textQuestion": {}}}},
                    "location": {"index": 2}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Field",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "DROP_DOWN",
                                    "options": [
                                        {"value": "AI Agent Development"},
                                        {"value": "Digital Marketing"},
                                        {"value": "SEO"},
                                        {"value": "Custom Automation"},
                                        {"value": "Other"}
                                    ]
                                }
                            }
                        }
                    },
                    "location": {"index": 3}
                }
            }
        ]
    }

    update_cmd = f'gws forms:v1 forms batchUpdate --params "{{\\"formId\\":\\"{form_id}\\",\\"resource\\":{json.dumps(update_params).replace('"', '\\"')}}}"'

    if run_gws(update_cmd):
        print("Questions added to form.")
    else:
        print("Failed to add questions.")

    # 3. Output links
    print(f"\nYour form is ready!")
    print(f"Editor URL: https://docs.google.com/forms/d/{form_id}/edit")
    print(f"Please open the form and click 'Responses' -> 'Link to Sheets' to create your 'Lead Form (Responses)' sheet.")

if __name__ == "__main__":
    main()
