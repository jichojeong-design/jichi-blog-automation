@echo off
chcp 65001 > nul
title 지치 블로그 매일 아침 9시 무인 자동 포스팅 스케줄러
echo =======================================================
echo    [지치 블로그] 매일 아침 09:00 KST 완전 무인 자동화 실행
echo =======================================================
cd /d "c:\Users\Administrator\Downloads\블로그 자동화"
python daily_scheduler.py
pause
