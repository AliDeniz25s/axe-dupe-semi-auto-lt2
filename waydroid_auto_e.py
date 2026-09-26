import os
import time

E_INTERVAL = 2.0

print("--- Waydroid Native Auto E ---")
print("Switch to Roblox now! The loop will start in 60 seconds.")
time.sleep(60)

print("Auto E is now ACTIVE. Go back to your PC host.")
print("To stop, switch back to Termux and press Ctrl+C.")

try:
    while True:
        os.system("su -c 'input keyevent 33'")
        time.sleep(E_INTERVAL)
except KeyboardInterrupt:
    print("\nAuto E Stopped.")
