# vrgb-desktop-app-and-keybind-sequence
made an app with access to variety of button to change color and brightness, sending commands to vrgb

# VRGB Control Panel - Installation Guide

This guide explains how to set up the keyboard shortcut sequence, the graphical interface, and the desktop launcher for the VRGB keyboard backlight tool on Linux Mint.

---

## 1. Prerequisites (Install Dependencies)
Open your terminal and ensure Python 3 and the Tkinter GUI package are installed:
```bash
sudo apt update
sudo apt install python3 python3-tk -y
```

---

## 2. File Placement & Permissions
Make sure your created files are saved in the correct system paths and given execution rights.

### A. The GUI Application (`vrgb_gui.py`)
1. Save the Python script to: `/usr/local/bin/vrgb_gui.py`
2. Make it executable by running:
   ```bash
   sudo chmod +x /usr/local/bin/vrgb_gui.py
   ```

### B. The Shortcut Script (`vrgb_sequence.sh`)
1. Save the sequential loop script to: `/usr/local/bin/vrgb_sequence.sh`
2. Make it executable by running:
   ```bash
   sudo chmod +x /usr/local/bin/vrgb_sequence.sh
   ```

---

## 3. Sudo Privileges Configuration (Crucial)
Since the `vrgb` binary requires root privileges, you must configure `sudo` to allow your scripts to execute it automatically without prompting for a password.

1. Open the secure sudoers editor:
   ```bash
   sudo visudo
   ```
2. Scroll to the very bottom of the file and append the following lines (replace `YOUR_USERNAME` with your actual Linux Mint username):
   ```text
   YOUR_USERNAME ALL=(ALL) NOPASSWD: /usr/bin/vrgb
   YOUR_USERNAME ALL=(ALL) NOPASSWD: /usr/local/bin/vrgb_sequence.sh
   ```
3. Save and close (`Ctrl + O`, `Enter`, then `Ctrl + X`).

---

## 4. Keybinding Setup (Keyboard Shortcut)
To link your physical key/button to the 12-step color loop:

1. Open **System Settings** -> **Keyboard** -> **Shortcuts** tab.
2. Select **Custom Shortcuts** and click **Add custom shortcut**.
3. Fill out the fields:
   * **Name:** VRGB Sequence Loop
   * **Command:** `sudo /usr/local/bin/vrgb_sequence.sh`
4. Click **Apply**, click the unassigned binding slot, and press the physical button you want to map.

---

## 5. Desktop Application Launcher
To make the GUI accessible directly from your Linux Mint Start Menu or Desktop:

1. Create a launcher file in your user local share space:
   ```bash
   nano ~/.local/share/applications/vrgb_control.desktop
   ```
2. Paste the following configuration inside the file:
   ```ini
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=VRGB Control Panel
   Comment=Control keyboard backlights manually or via sequence
   Exec=/usr/local/bin/vrgb_gui.py
   Icon=preferences-desktop-color
   Categories=Utility;
   Terminal=false
   StartupNotify=false
   ```
3. Save and exit (`Ctrl + O`, `Enter`, `Ctrl + X`).
4. Make the desktop entry executable:
   ```bash
   chmod +x ~/.local/share/applications/vrgb_control.desktop
   ```

You will now find **VRGB Control Panel** inside your Start Menu under the "Accessories" or "Utility" category!
