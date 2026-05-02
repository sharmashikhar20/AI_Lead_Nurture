# Workflow: Qualify Leads
## Objective
Fetch new responses from the "Lead Form (Responses)" Google Sheet, score them based on budget and field, and update the sheet with recommendations.

## Prerequisites
- GWS CLI installed and authenticated.
- Google Sheets API enabled.
- Access to the "Lead Form (Responses)" spreadsheet.

## Steps
1. **Fetch Leads**: Run `python tools/fetch_leads.py`. This finds the sheet and saves new entries to `.tmp/raw_leads.json`.
2. **Score Leads**: Run `python tools/score_leads.py`. This categorizes leads into Hot, Warm, or Cold based on budget and interest field.
3. **Update Sheet**: Run `python tools/update_sheet.py`. This writes the scores and recommendations back to the Google Sheet.

## Rules
- **Hot 🔥**: Budget > ₹50,000 AND (Field is "AI Agent Development" OR "Digital Marketing").
- **Warm 🙂**: Budget > ₹50,000 OR (Field is "AI Agent Development" OR "Digital Marketing").
- **Cold ❄️**: All others.

## Edge Cases
- **No new leads**: The tools should exit gracefully if no new rows are found.
- **Missing columns**: Errors if headers do not match: Name, Email, Budget, Field.
