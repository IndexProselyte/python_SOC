from pathlib import Path;import winreg as wrg; import os

registry = wrg.ConnectRegistry(f"{os.environ['COMPUTERNAME']}", wrg.HKEY_LOCAL_MACHINE)

p = Path("client_main.py").resolve()

soft = wrg.OpenKeyEx(registry, r"Software\Microsoft\Windows\CurrentVersion\Run",0, wrg.KEY_ALL_ACCESS | wrg.KEY_WOW64_64KEY);

wrg.SetValueEx(soft, "sex", 0, wrg.REG_SZ, f"{p}")

if soft: 
    wrg.CloseKey(soft)