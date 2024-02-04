@echo off
color a
netsh advfirewall firewall add rule name="fuck-jiyu" dir=out action=block program="c:\programfiles(x86)\Mythware\极域课堂管理系统软件v6.0 2019豪华版\StudentMain.exe" enable=yes
taskkill /f /im studentmain.exe
cd %ProgramFiles(x86)%\
cd "Mythware\极域课堂管理系统软件v6.0 2019豪华版\"
del /s /q shutdown.exe
start StudentMain.exe
echo made by sunminghao!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
timeout /t -1