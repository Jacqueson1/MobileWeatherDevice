@echo off
cd /d "C:\Users\HP\WeatherDevice\MobileWeatherDevice"
echo ---- %date% %time% >> data\collector.log
".venv\Scripts\python.exe" -m collector.run_daily >> data\collector.log 2>&1