@echo off
color a
netsh advfirewall firewall add rule name="fuck-jiyu" dir=out action=block program="c:\programfiles(x86)\Mythware\������ù���ϵͳ���v6.0 2019������\StudentMain.exe" enable=yes
taskkill /f /im studentmain.exe
cd %ProgramFiles(x86)%\
cd "Mythware\������ù���ϵͳ���v6.0 2019������\"
del /s /q shutdown.exe
start StudentMain.exe
echo made by sunminghao!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
timeout /t -1