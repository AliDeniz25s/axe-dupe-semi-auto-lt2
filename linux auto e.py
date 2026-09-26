#!/usr/bin/env python3
import os
import sys

# ==========================================
#  Immediate Graphical Sudoers Elevation Check
# ==========================================
if os.getuid() != 0:
    current_env = os.environ.copy()
    sudo_args = [
        "sudo", "-E",
        sys.executable,
        os.path.abspath(sys.argv[0])
    ] + sys.argv[1:]

    try:
        os.execvp("sudo", sudo_args)
    except Exception as e:
        print(f"Sudoers dynamic elevation failed: {e}")
        sys.exit(1)

import tkinter as tk
import threading
import time
import select
from evdev import UInput, ecodes, InputDevice, list_devices

# ==========================================
#      EDIT YOUR CONFIG HERE
# ==========================================
E_INTERVAL = 2.0  # Time in seconds between E presses
# ==========================================
#         Auto E UI Layout
# ==========================================
WX, WY = 1620, 35
WW, WH = 260, 220
GUI_GEOMETRY = f"{WW}x{WH}+{WX}+{WY}"

BG_MAIN        = "#121212"
BG_PANEL       = "#1A1A1A"
COLOR_TEXT     = "#D4C4A8"
ACCENT_GOLD    = "#FFD700"
COLOR_GREYED   = "#555555"
COLOR_BORDER   = "#332C20"
COLOR_RED      = "#FF4A4A"

FONT_TITLE = ("Georgia", 11, "bold")
FONT_TEXT  = ("Georgia", 10)
FONT_TIMER = ("Courier New", 10, "bold")

class AutoE:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto E")
        self.root.geometry(GUI_GEOMETRY)

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=BG_MAIN)

        self.e_active = False
        self.next_execution = 0

        self.ui = UInput()

        self.main_frame = tk.Frame(root, bg=BG_MAIN, highlightthickness=2, highlightbackground=COLOR_BORDER)
        self.main_frame.pack(fill="both", expand=True)

        self.title_lbl = tk.Label(self.main_frame, text="— AUTO E —", font=FONT_TITLE, fg=ACCENT_GOLD, bg=BG_MAIN)
        self.title_lbl.pack(pady=(12, 8))

        self.content_frame = tk.Frame(self.main_frame, bg=BG_PANEL, padx=8, pady=8, highlightthickness=1, highlightbackground="#2A2A2A")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Row 1: F5 Control & Countdown
        self.e_status_lbl = tk.Label(self.content_frame, text="[F5] Auto E: OFF", font=FONT_TEXT, fg=COLOR_TEXT, bg=BG_PANEL)
        self.e_status_lbl.grid(row=0, column=0, sticky="w", pady=8)

        self.e_timer_lbl = tk.Label(self.content_frame, text=f"[{E_INTERVAL}s]", font=FONT_TIMER, fg=COLOR_TEXT, bg=BG_PANEL)
        self.e_timer_lbl.grid(row=0, column=1, sticky="e", padx=(4, 0), pady=8)

        # Row 2: Close Hotkey Indicator
        self.close_key_lbl = tk.Label(self.content_frame, text="[F8] Exit Keybind", font=FONT_TEXT, fg=ACCENT_GOLD, bg=BG_PANEL)
        self.close_key_lbl.grid(row=1, column=0, columnspan=2, sticky="w", pady=8)

        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)

        # Bottom: Close Overlay Button
        self.close_btn = tk.Button(
            self.main_frame,
            text="CLOSE OVERLAY",
            font=FONT_TITLE,
            fg=COLOR_RED,
            bg=BG_PANEL,
            activebackground=BG_MAIN,
            activeforeground="#FF3333",
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
            bd=1,
            command=lambda: os._exit(0)
        )
        self.close_btn.pack(fill="x", padx=10, pady=(0, 12))

        # Window Dragging Logic
        drag_elements = [
            self.main_frame, self.title_lbl, self.content_frame,
            self.e_status_lbl, self.e_timer_lbl, self.close_key_lbl
        ]
        for element in drag_elements:
            element.bind("<ButtonPress-1>", self.start_move)
            element.bind("<ButtonRelease-1>", self.stop_move)
            element.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self._x = event.x_root - self.root.winfo_x()
        self._y = event.y_root - self.root.winfo_y()

    def stop_move(self, event):
        self._x = None
        self._y = None

    def do_move(self, event):
        if self._x is not None and self._y is not None:
            x = event.x_root - self._x
            y = event.y_root - self._y
            self.root.geometry(f"+{x}+{y}")

    def sync_ui(self):
        now = time.time()

        if self.e_active:
            self.e_status_lbl.config(text="[F5] Auto E: ON", fg=ACCENT_GOLD)
            remaining = max(0.0, self.next_execution - now)
            self.e_timer_lbl.config(text=f"[{remaining:.1f}s]", fg=ACCENT_GOLD)
        else:
            self.e_status_lbl.config(text="[F5] Auto E: OFF", fg=COLOR_TEXT)
            self.e_timer_lbl.config(text=f"[{E_INTERVAL}s]", fg=COLOR_TEXT)

        self.root.after(50, self.sync_ui)

    def press_e(self):
        self.ui.write(ecodes.EV_KEY, ecodes.KEY_E, 1)
        self.ui.syn()
        time.sleep(0.05)
        self.ui.write(ecodes.EV_KEY, ecodes.KEY_E, 0)
        self.ui.syn()

    def e_loop(self):
        while self.e_active:
            self.press_e()
            self.next_execution = time.time() + E_INTERVAL

            steps = int(E_INTERVAL / 0.05)
            for _ in range(steps):
                if not self.e_active:
                    break
                time.sleep(0.05)

    def start_listener(self):
        try:
            devs = {InputDevice(p).fd: InputDevice(p) for p in list_devices() if ecodes.EV_KEY in InputDevice(p).capabilities()}
        except Exception as e:
            print(f"Error parsing hardware nodes: {e}")
            return

        while True:
            try:
                r, _, _ = select.select(devs, [], [])
                for fd in r:
                    for event in devs[fd].read():
                        if event.type == ecodes.EV_KEY and event.value == 1:

                            # Close Overlay
                            if event.code == ecodes.KEY_F8:
                                os._exit(0)

                            # Toggle Auto E
                            elif event.code == ecodes.KEY_F5:
                                self.e_active = not self.e_active
                                if self.e_active:
                                    self.next_execution = time.time()
                                    threading.Thread(target=self.e_loop, daemon=True).start()

            except (OSError, KeyError):
                continue
            except Exception:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoE(root)
    app.sync_ui()

    threading.Thread(target=app.start_listener, daemon=True).start()
    root.mainloop()
