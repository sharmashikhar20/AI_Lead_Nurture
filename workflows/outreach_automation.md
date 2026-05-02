# Workflow: Outreach Automation
## Objective
Generate personalized email responses and save them as Gmail drafts for leads qualified in the scoring system.

## Prerequisites
- Phase 1 (Lead Scoring) completed successfully.
- Gmail API enabled in Google Cloud Console.
- GWS CLI authenticated and using local keyring.

## Steps
1. **Initialize Phase 1**: Ensure `python tools/fetch_leads.py` and `python tools/score_leads.py` have been run.
2. **Generate Copy**: Run `python tools/generate_outreach.py`.
   - This calculates **Conversion Probability**.
   - This generates **Personalized Email Body** based on Hot/Warm/Cold scores.
3. **Push to Gmail**: Run `python tools/send_outreach_drafts.py`.
   - This creates Drafts in your Gmail account (Drafts folder).
4. **Final Review**: Open your [Gmail Drafts](https://mail.google.com/mail/u/0/#drafts), review the content, and hit send!

## Logic & Personalization
- **Probability**: High budgets (>₹1L) get a +10% boost.
- **Tone**: Professional yet friendly, tailored to the specific business field (AI, Marketing, etc.).
- **Signature**: Shikhar Sharma (Your AI Companion).

## Troubleshooting
- **Error: RFC 2822**: Occurs if the email format is invalid. The tool handles base64 encoding automatically.
- **No Drafts Visible**: Ensure you are logged into GWS CLI with the same account as your Gmail.
