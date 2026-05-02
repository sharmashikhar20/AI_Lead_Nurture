@echo off
cd /d "C:\Users\Shikhar\Desktop\Claude Projects\Google CLI"
echo Starting AI Agent Revenue System...
python tools/fetch_leads.py
python tools/score_leads.py
python tools/get_calendar_slots.py
python tools/generate_outreach.py
python tools/update_sheet.py
python tools/send_outreach_drafts.py
echo.
echo Automation Complete! Check your Sheet and Gmail Drafts.
pause
