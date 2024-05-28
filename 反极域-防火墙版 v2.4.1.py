import ctypes
import sys
import subprocess
import os
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import json

if sys.version_info[0] == 3:
    import winreg as winreg
else:
    import _winreg as winreg

CMD = r"C:\Windows\System32\cmd.exe"
FOD_HELPER = r'C:\Windows\System32\fodhelper.exe'
REG_PATH = 'Software\Classes\ms-settings\shell\open\command'
DELEGATE_EXEC_REG_KEY = 'DelegateExecute'


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def create_reg_key(key, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
    except WindowsError:
        raise


def bypass_uac(cmd):
    try:
        create_reg_key(DELEGATE_EXEC_REG_KEY, '')
        create_reg_key(None, cmd)
    except WindowsError:
        raise


CONFIG_FILE = "config.json"
VERSION = "2.4.1"


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            if "jiyu_path" in config:
                config["jiyu_path"] = config["jiyu_path"].replace("/", "\\")
            return config
    return {}


def save_config(config):
    print("Saving config:", config)  # debug
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)


def open_config_file():
    os.startfile(CONFIG_FILE)
    print("Config file opened")


def select_jiyu_path():
    path = filedialog.askopenfilename(title="选择极域主程序", filetypes=[("可执行文件", "*.exe")])
    if path:
        config = load_config()
        config["jiyu_path"] = path
        save_config(config)
        print("Selected jiyu path:", path)  # debug
        return path
    return None


def get_jiyu_path():
    config = load_config()
    if "jiyu_path" in config and os.path.exists(config["jiyu_path"]):
        jiyu_path = config["jiyu_path"]
        print("Loaded jiyu path:", jiyu_path)  # debug
        return jiyu_path
    else:
        path = select_jiyu_path()
        if path:
            return path
        else:
            messagebox.showerror("Error", "未选择极域主程序，无法继续。")
            sys.exit()


def run_command(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return "", str(e)


def taskkill_process():
    os.system("taskkill /f /im StudentMain.exe")


def on_button_click(option, jiyu_path, detail_text):
    jiyu_dir = os.path.dirname(jiyu_path)
    program_path = os.path.join(jiyu_dir, "StudentMain.exe")
    netsh_command = f'netsh advfirewall firewall add rule name="fuck-jiyu" dir=out action=block program="{program_path}" enable=yes'
    netsh_command_delete = 'netsh advfirewall firewall delete rule name="fuck-jiyu"'
    restart_jiyu = f'cd /d "%ProgramFiles(x86)%\\Mythware\\极域课堂管理系统软件v6.0 2019豪华版\\" && start StudentMain.exe'
    delete_shutdown_project = f'cd /d "%ProgramFiles(x86)%\\Mythware\\极域课堂管理系统软件v6.0 2019豪华版\\" && del /f /q shutdown.exe'

    stdout, stderr = "", ""
    if option == 1:
        stdout, stderr = run_command(netsh_command)
        if stderr:
            messagebox.showerror("Error", f"执行命令时出错: {stderr}")
        else:
            taskkill_process()
            stdout, stderr = run_command(restart_jiyu)
            messagebox.showinfo("Success", "防火墙已开启，作者孙明昊!")
    elif option == 0:
        stdout, stderr = run_command(netsh_command_delete)
        if stderr:
            messagebox.showerror("Error", f"执行命令时出错: {stderr}")
        else:
            taskkill_process()
            stdout, stderr = run_command(restart_jiyu)
            messagebox.showinfo("Success", "防火墙已关闭，作者孙明昊!")
    elif option == 2:
        taskkill_process()
        stdout, stderr = run_command(delete_shutdown_project)
        if stderr:
            messagebox.showerror("Error", f"执行命令时出错: {stderr}")
        else:
            stdout, stderr = run_command(restart_jiyu)
            messagebox.showinfo("Success", "已删除文件, 作者孙明昊!")
    elif option == 3:
        stdout, stderr = run_command(netsh_command)
        if stderr:
            messagebox.showerror("Error", f"执行命令时出错: {stderr}")
        else:
            taskkill_process()
            stdout, stderr = run_command(delete_shutdown_project)
            if stderr:
                messagebox.showerror("Error", f"执行命令时出错: {stderr}")
            else:
                stdout, stderr = run_command(restart_jiyu)
                messagebox.showinfo("Success", "防火墙已开启并删除文件, 作者孙明昊!")
    if detail_text and detail_text.winfo_exists():
        detail_text.delete('1.0', tk.END)
        detail_text.insert(tk.END, f"stdout:\n{stdout}\nstderr:\n{stderr}")


def change_jiyu_path():
    new_path = select_jiyu_path()
    if new_path:
        messagebox.showinfo("Success", f"极域主程序路径已更改为: {new_path}")


def create_gui(jiyu_path):
    root = tk.Tk()
    root.title("极域控制")
    root.geometry("400x500")
    top_var = tk.IntVar()
    detail_var = tk.IntVar()

    def toggle_top():
        root.attributes('-topmost', top_var.get())

    def toggle_details():
        if detail_var.get():
            detail_text.pack(pady=5)
            show_details_info(detail_text)
        else:
            detail_text.pack_forget()

    def show_details_info(detail_text):
        config = load_config()
        config_info = "\n".join([f"{key}: {value}" for key, value in config.items()])
        details = f"参数:\n窗口置顶: {top_var.get()}\n显示详细信息: {detail_var.get()}\n\nConfig 文件内容:\n{config_info}\n\n版本信息:\n版本: {VERSION}"
        detail_text.delete('1.0', tk.END)
        detail_text.insert(tk.END, details)

    label = tk.Label(root, text="请选择一个选项:")
    label.pack(pady=10)

    button1 = tk.Button(root, text="开启反极域防火墙", command=lambda: on_button_click(1, jiyu_path, detail_text))
    button1.pack(pady=5)

    button2 = tk.Button(root, text="关闭反极域防火墙", command=lambda: on_button_click(0, jiyu_path, detail_text))
    button2.pack(pady=5)

    button3 = tk.Button(root, text="删除远程关机文件(永久不可恢复!)", command=lambda: on_button_click(2, jiyu_path, detail_text))
    button3.pack(pady=5)

    button4 = tk.Button(root, text="开启防火墙并删除关机文件", command=lambda: on_button_click(3, jiyu_path, detail_text))
    button4.pack(pady=5)

    open_config_button = tk.Button(root, text="打开配置文件", command=open_config_file)
    open_config_button.pack(pady=5)

    change_path_button = tk.Button(root, text="更改极域主程序路径", command=change_jiyu_path)
    change_path_button.pack(pady=5)

    top_checkbox = tk.Checkbutton(root, text="窗口置顶", variable=top_var, command=toggle_top)
    top_checkbox.pack(pady=5)

    detail_checkbox = tk.Checkbutton(root, text="显示详细信息", variable=detail_var, command=toggle_details)
    detail_checkbox.pack(pady=5)

    detail_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
    detail_text.pack(pady=5)
    detail_text.pack_forget()  # Hide initially

    version_label = tk.Label(root, text=f"版本: {VERSION}")
    version_label.pack(pady=5)

    root.mainloop()


def execute():
    if not is_admin():
        print('[!] The script is NOT running with administrative privileges')
        print('[+] Trying to bypass the UAC')
        try:
            current_exe = sys.argv[0]
            cmd = '{} /k "{}"'.format(CMD, current_exe)
            bypass_uac(cmd)
            os.system(FOD_HELPER)
            sys.exit(0)
        except WindowsError:
            sys.exit(1)
    else:
        print('[+] The script is running with administrative privileges!')
        current_directory = os.getcwd()
        print("Current working directory:", current_directory)
        jiyu_path = get_jiyu_path()
        create_gui(jiyu_path)


if __name__ == '__main__':
    execute()
