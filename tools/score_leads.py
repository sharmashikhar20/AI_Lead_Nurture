import json
import os

def clean_budget(budget_str):
    try:
        # Remove currency symbols and commas, then convert to int
        cleaned = ''.join(filter(str.isdigit, str(budget_str)))
        return int(cleaned) if cleaned else 0
    except:
        return 0

def score_lead(row, headers):
    # Map headers to indices
    try:
        idx = {h.lower().strip(): i for i, h in enumerate(headers)}
        name = row[idx['name']]
        email = row[idx['email']]
        budget_raw = row[idx['budget']]
        # Use 'field of work' as seen in the JSON
        field = row[idx['field of work']].strip()

        budget = clean_budget(budget_raw)
        # Match priority fields
        is_high_priority_field = any(keyword in field for keyword in ["AI Agent", "Digital Marketing", "Automation"])
        is_high_budget = budget >= 50000

        if is_high_budget and is_high_priority_field:
            score = "Hot 🔥"
            rec = f"Focus on premium {field} package. High conversion probability."
        elif is_high_priority_field and budget < 50000:
            score = "Semi-Hot ⚡"
            rec = f"Interested in {field} but budget is lower. Strategy call needed to upsell."
        elif is_high_budget or is_high_priority_field:
            score = "Warm 🙂"
            rec = f"Send case study on {field}."
        else:
            score = "Cold ❄️"
            rec = "Add to educational newsletter."

        return [score, rec]
    except Exception as e:
        return ["Error", f"Missing data: {str(e)}"]

def main():
    if not os.path.exists(".tmp/raw_leads.json"):
        print("Raw leads file not found.")
        return

    with open(".tmp/raw_leads.json", "r") as f:
        data = json.load(f)

    values = data["values"]
    if len(values) < 2:
        print("No lead data to score (only headers found).")
        return

    headers = values[0]
    leads = values[1:]

    scored_results = []
    # Identify base headers (original form fields)
    base_headers = []
    for h in headers:
        if h.lower().strip() not in ['score', 'recommendation']:
            base_headers.append(h)
        else:
            # Once we hit a score/recommendation column, we assume all following are extras
            break

    scored_results.append(base_headers + ["Score", "Recommendation"])

    for row in leads:
        # Take exactly as many columns as there are base headers
        clean_row = row[:len(base_headers)]
        # Pad row if columns are missing
        while len(clean_row) < len(base_headers):
            clean_row.append("")

        score_info = score_lead(clean_row, base_headers)
        scored_results.append(clean_row + score_info)

    with open(".tmp/scored_leads.json", "w") as f:
        json.dump({"sheet_id": data["sheet_id"], "values": scored_results}, f)

    print(f"Successfully scored {len(leads)} leads.")

if __name__ == "__main__":
    main()
