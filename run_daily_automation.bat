@echo off
chcp 65001 > nul
cd /d "c:\Users\Administrator\Downloads\블로그 자동화"
"C:\Python314\python.exe" "c:\Users\Administrator\Downloads\블로그 자동화\daily_scheduler.py" --cloud-mode >> "c:\Users\Administrator\Downloads\블로그 자동화\daily_automation.log" 2>&1
