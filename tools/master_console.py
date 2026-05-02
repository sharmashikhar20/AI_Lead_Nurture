import os
import subprocess
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_phase_1_2():
    print("\n--- Executing Phase 1 & 2 (Scoring & Gmail Drafts) ---")
    scripts = ["tools/score_leads.py", "tools/generate_outreach.py", "tools/update_sheet.py", "tools/send_outreach_drafts.py"]
    for s in scripts:
        subprocess.run(["python", s])
    print("\n✅ Phase 1 & 2 Complete.")

def run_phase_1_3():
    print("\n--- Executing Full Phase 1-3 (Scoring, Calendar, Docs & Gmail) ---")
    scripts = ["tools/score_leads.py", "tools/get_calendar_slots.py", "tools/generate_outreach.py", "tools/update_sheet.py", "tools/create_meeting_docs.py", "tools/send_outreach_drafts.py"]
    for s in scripts:
        subprocess.run(["python", s])
    print("\n✅ Full system cycle complete.")

def main():
    clear()
    print("====================================================")
    print("            AI AGENT: MASTER CONTROLLER             ")
    print("====================================================")
    print("\nNew leads have been detected in your Google Sheet.")
    print("How would you like to process them?")
    print("\n[1] Phase 1-2: Score Leads & Create Gmail Drafts")
    print("[2] Phase 1-3: Full Automated Cycle (Includes Strategy Docs)")
    print("[3] Exit")
    print("\n" + "="*52)

    choice = input("\nEnter your choice (1, 2, or 3): ")

    if choice == "1":
        run_phase_1_2()
    elif choice == "2":
        run_phase_1_3()
    elif choice == "3":
        sys.exit()
    else:
        print("Invalid choice.")

    input("\nPress Enter to close this console...")

if __name__ == "__main__":
    main()
