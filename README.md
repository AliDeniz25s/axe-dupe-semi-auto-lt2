use this shit of a loadstring 
loadstring(game:HttpGet("https://raw.githubusercontent.com/AliDeniz25s/axe-dupe-semi-auto-lt2/refs/heads/main/duper"))()
the mmacro instructions and features 
# Auto E Macro Overlay

A lightweight, customizable Python macro script featuring a floating GUI overlay that automatically spams the **E** key at set intervals. Available for both Linux and Windows.

---

## Features

* **Floating Overlay GUI:** Clean, dark-themed, always-on-top, and draggable control window.
* **Live Countdown Timer:** Visual status tracker showing when the next key press will happen.
* **Simple Hotkeys:**
* **F5:** Toggle Auto E ON/OFF
* **F8:** Exit / Close Application



---

## Linux Installation & Dependencies

The Linux version utilizes Python 3, Tkinter, and `evdev` to simulate hardware-level input. Because of this, it requires root/sudo privileges (the script handles self-elevation automatically).

### Dependency Installation Commands by Distro:

* **Ubuntu / Debian / Linux Mint / Pop!_OS:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk python3-evdev

```


* **Fedora / RHEL / CentOS:**
```bash
sudo dnf install python3 python3-pip python3-tkinter python3-evdev

```


* **Arch Linux / Manjaro:**
```bash
sudo pacman -S python python-pip tk python-evdev

```


* **openSUSE:**
```bash
sudo zypper install python3 python3-pip python3-tk python3-evdev

```



### How to Run on Linux:

1. Save the Linux script as `auto_e.py`.
2. Open a terminal in the script directory and make it executable:
```bash
chmod +x auto_e.py

```


3. Run the script (it will request your sudo password automatically):
```bash
python3 auto_e.py

```


4. Press **F5** to start/stop the macro, and **F8** to exit.

---

## Windows Installation & Dependencies

The Windows version utilizes Python 3, Tkinter, and the `keyboard` library to manage hotkeys and simulate key inputs globally.

### Dependency Installation Commands (Windows):

Open **Command Prompt** or **PowerShell** and run:

```cmd
pip install keyboard

```

*(Note: Tkinter comes pre-installed with standard Windows Python distributions).*

### How to Run on Windows:

1. Save the Windows script file as `auto_e_win.py`.
2. Open Command Prompt or PowerShell in the directory where the file is saved.
3. Run the script:
```cmd
python auto_e_win.py

```


4. Press **F5** to start/stop the macro, and **F8** to exit.

---

## Troubleshooting: What Could Go Wrong & Solutions

### Linux Troubleshooting

* **Error:** `ModuleNotFoundError: No module named 'evdev'` or `'tkinter'`
* **Solution:** Install the respective package using your distribution's package manager commands shown in the Linux section above.


* **Error:** Sudoers dynamic elevation failed / Permission Denied
* **Solution:** Ensure you are running the script from a user account with standard sudo access. The script attempts to elevate itself automatically.


* **Problem:** The terminal says "No such file or directory" or the script won't run when executing the command.
* **Solution:** Ensure the actual name of your saved Python file matches the name written in your command (e.g., `auto_e.py`), and make sure your terminal is navigated to the exact directory where the file is located using `cd /path/to/folder`.


* **Issue:** Key presses do not register inside games or specific applications.
* **Solution:** Ensure your user has write permissions to `/dev/uinput` or load the kernel module using `sudo modprobe uinput`.



### Windows Troubleshooting

* **Error:** `ModuleNotFoundError: No module named 'keyboard'`
* **Solution:** Run `pip install keyboard` in your command prompt. If multiple Python versions are installed, use `python -m pip install keyboard`.


* **Issue:** Hotkeys (`F5`/`F8`) do not trigger or key presses are blocked.
* **Solution:** The `keyboard` module on Windows requires administrator permissions to hook global hotkeys. Right-click your Command Prompt or PowerShell icon and select **"Run as administrator"**, then restart the script.


* **Issue:** Hotkeys conflict with other apps.
* **Solution:** Close background macro utilities or software (like Logitech G Hub, Razer Synapse, or AutoHotkey) that might be intercepting `F5` or `F8`.
