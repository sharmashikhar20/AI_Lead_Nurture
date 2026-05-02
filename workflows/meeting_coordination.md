# Workflow: Meeting Coordination & Reporting
## Objective
Synchronize the outreach process with your real-time availability and prepare strategy documents for high-value leads.

## Steps
1. **Fetch Availability**: Run `python tools/get_calendar_slots.py`.
   - Scans 10:00 AM - 7:00 PM (Weekdays).
   - Finds 1-hour slots with a 15-minute buffer.
2. **Generate Targeted Outreach**: Run `python tools/generate_outreach.py`.
   - Injects the top 3 free slots into the email drafts.
3. **Create Strategy Docs**: Run `python tools/create_meeting_docs.py`.
   - Automatically creates a personalized Google Doc for every "Hot 🔥" lead.
4. **Push Drafts**: Run `python tools/send_outreach_drafts.py`.

## Logic
- **Hot Leads**: Get specific time proposals + a mention of the pre-prepared Strategy Doc.
- **Buffer**: Ensures you have 15 minutes between meetings.
