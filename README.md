# AI Lead Nurture Agent 🚀

A fully automated AI Agent system built with the **WAT Framework** (Workflows, Agents, Tools) to capture, qualify, and nurture leads using Google Workspace.

## 🧠 Core Features
- **Phase 1: Lead Capture & Scoring**: Automatically fetches leads from Google Forms/Sheets and scores them (Hot, Semi-Hot, Warm, Cold) based on budget and business field.
- **Phase 2: Smart Outreach**: Generates personalized, professional Gmail drafts with upselling logic and field-specific value propositions.
- **Phase 3: Scheduling & Reporting**: Integrates with Google Calendar and automatically creates Strategy Session documents for high-value leads.
- **Phase 4: Automation**: Silent background monitor with desktop notifications and an interactive Master Console for one-click processing.

## 🛠️ Architecture (WAT Framework)
- **Workflows/**: Markdown SOPs defining the business logic and standard operating procedures.
- **Tools/**: Deterministic Python scripts that execute API calls via the Google Workspace CLI.
- **Monitor**: A background poller that watches for new leads and notifies the user via desktop toast.

## 🚀 Setup
1. Install the Google Workspace CLI: `npm install -g @googleworkspace/cli`
2. Authenticate: `gws auth login`
3. Run `Start_Background_Monitor.bat` to begin automation.

---
*Built with ❤️ for AI Agent Development and Digital Marketing growth.*
