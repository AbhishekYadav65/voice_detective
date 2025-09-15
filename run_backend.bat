@echo off
echo 🚀 Starting Voice Detective Backend...
cd /d %~dp0
uvicorn backend.app:app --reload --port 8000
pause
