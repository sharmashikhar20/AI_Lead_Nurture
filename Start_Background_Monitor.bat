@echo off
cd /d "C:\Users\Shikhar\Desktop\Claude Projects\Google CLI"
echo AI Agent Monitor is running in the background...
start /min pythonw tools/monitor_leads.py
exit
