print("[task] Checking modules [||||||||||]")
try:
    print("--Tkinter--")
    from tkinter import TkVersion
    print("[info] Running Tkinter version: {version:.2f}".format(version=TkVersion))
    print("[info] Module need not be installed.")
except ModuleNotFoundError:
    from os import system
    print("[info] Installing tkinter.")
    system("python -m pip install tkinter")
try:
    print("--pywin32--")
    from win32com.client import Dispatch
    print("[info] Module need not be installed.")
except ModuleNotFoundError:
    from os import system
    print("[info] Win32com not found. Installing library.")
    system("python -m pip install pywin32")
    from win32com.client import Dispatch
    print("[warn] You might need to restart the installer")
try:
    print("--winshell--")
    from winshell import startup, start_menu, desktop
    print("[info] Module need not be installed.")
except ModuleNotFoundError:
    from os import system
    print("[info] winshell not found. Installing library.")
    system("python -m pip install winshell")
    from winshell import startup, start_menu, desktop
    print("[warn] You might need to restart the installer")

print("--------")
print("[task] Importing modules/functions [||||||||||]")

def make_shortcut(path, target, work_dir, description, icon):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = work_dir
    shortcut.Description = description
    shortcut.IconLocation = icon
    shortcut.save()

from tkinter import Tk,filedialog
from os import getenv, system
from zipfile import ZipFile

print("[info] Task complete. Modules/functions have been imported")
print("--------")
print("[task] Locating paths [||||||||||]")
print("[task] Asking user for app directory.")

app = Tk()
app.attributes("-alpha", 0.0)
app.geometry("0x0")

install_to = filedialog.askdirectory(initialdir=getenv("appdata")).replace("/","\\")+"\\sKhedule"
app.destroy()
print("[info] Task Complete")
startup_dir = startup()
start_menu = start_menu()
desktop_dir = desktop()

print("--------")
print("[info] Located app directory as {inst:s}".format(inst=install_to))
print("[info] Located startup directory as {stp:s}".format(stp=startup_dir))
print("[info] Located start menu directory as {stp:s}".format(stp=start_menu))
print("[info] Located desktop directory as {stp:s}".format(stp=desktop_dir))

if input("\n\n--------\n[system] Is this correct? Do you want to proceed (y/n):\n\n").upper() == "N":
    print("[system] User aborted process. Exiting...")
    raise SystemExit
else:
    print("[system] Continuing process.")
print("--------")
print("[info] Extracting files.")
try:
    ZipFile("data.zip", 'r').extractall(install_to)
except PermissionError:
    input("[error] Missing Permissions. Make sure the directory has no files. If you are over writing an old version of sKhedule you can kill the process using the taskkill command.\ntaskkill /IM python.exe /F")
    raise SystemExit
print("[info] Files extracted. No Errors.")
print("--------")
print("[info] Creating shortcuts.")
make_shortcut(desktop_dir+"\\sKhedule.lnk", install_to+"\\open.py", install_to, "sKhedule, the alarm app", install_to+"\\assets\\alarm.ico")
make_shortcut(start_menu+"\\sKhedule.lnk", install_to+"\\open.py", install_to, "sKhedule, the alarm app", install_to+"\\assets\\alarm.ico")
make_shortcut(startup_dir+"\\sKhedule.lnk", install_to+"\\server.exe", install_to, "sKhedule, the alarm app", install_to+"\\assets\\alarm.ico")
print("[info] Shortcuts Created.")
print("[info] Setting up app.")
system("cd / && "+install_to[0:2]+" && cd "+install_to+" && python main.py -setup")
print("[info] Starting app.")
system("cd / && "+install_to[0:2]+" && cd "+install_to+" && start server.exe")
input("--------")