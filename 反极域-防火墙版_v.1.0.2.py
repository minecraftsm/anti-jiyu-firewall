import ctypes
import sys
import subprocess
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

netsh_command = 'netsh advfirewall firewall add rule name="fuck-jiyu" dir=out action=block program="c:\\program files (x86)\\Mythware\\极域课堂管理系统软件v6.0 2019豪华版\\StudentMain.exe" enable=yes'
netsh_command_delete = 'netsh advfirewall firewall delete rule name="fuck-jiyu"'
restart_jiyu = 'cd /d "%ProgramFiles(x86)%\\Mythware\\极域课堂管理系统软件v6.0 2019豪华版\\" && start StudentMain.exe'
delete_shutdown_project = 'cd /d "%ProgramFiles(x86)%\\Mythware\\极域课堂管理系统软件v6.0 2019豪华版\\" && del /f /q shutdown.exe'


if is_admin():
    print("请输入1或0，1为开启反极域防火墙，0为关闭该防火墙，2为删除远程关机文件(永久不可恢复!)，3为开启反极域防火墙并删除远程关机文件(永久不可恢复!):")
    n = int(input())
    if n == 1:
        subprocess.run(netsh_command, check=True, shell=True)
        print("防火墙已开启，作者孙明昊!")
        os.system("taskkill /f /im studentmain.exe")
        try:
            subprocess.run(restart_jiyu, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print("启动程序时出错:", e)
        os.system("timeout /t -1")
    elif n == 0:
        subprocess.run(netsh_command_delete, check=True, shell=True)
        print("防火墙已关闭，作者孙明昊!")
        os.system("taskkill /f /im studentmain.exe")
        try:
            subprocess.run(restart_jiyu, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print("启动程序时出错:", e)
        os.system("timeout /t -1")
    elif n == 2:
        os.system("taskkill /f /im studentmain.exe")
        subprocess.run(delete_shutdown_project, check=True, shell=True)
        print("已删除文件,作者孙明昊!")
        try:
            subprocess.run(restart_jiyu, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print("启动程序时出错:", e)
        os.system("timeout /t -1")
    elif n == 3:
        subprocess.run(netsh_command, check=True, shell=True)
        print("防火墙已开启，作者孙明昊!")
        os.system("taskkill /f /im studentmain.exe")
        subprocess.run(delete_shutdown_project, check=True, shell=True)
        print("已删除文件,作者孙明昊!")
        try:
            subprocess.run(restart_jiyu, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print("启动程序时出错:", e)
        os.system("timeout /t -1")
        
        
        
else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        print("run again...")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
