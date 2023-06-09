import tkinter as tk
import threading
from pynput.mouse import Listener as MouseListener, Button
from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode
import pyautogui
from collections import deque
import numpy as np
import os

action_log = []
key_buffer = deque(maxlen=5)
stop_listening = False
start_time = end_time = None
stop_hotkey = {Key.ctrl, Key.alt, KeyCode.from_char('z')}
current_keys = set()
last_screenshot = None

KEY_NAME_MAPPING = {
    'alt': {
        'linux': '<alt>',
        'windows': '<alt>',
        'mac': '<option>'
    },
    # Add other special keys as needed...
}

def on_click(x, y, button, pressed):
    global start_time, end_time, last_screenshot
    if button == Button.left and pressed:
        screenshot = pyautogui.screenshot()
        if last_screenshot is not None and np.array_equal(np.array(screenshot), np.array(last_screenshot)):
            screenshot_path = "reuse_previous_screenshot"
        else:
            screenshot_path = f"{time.time()}_screenshot.png"
            screenshot.save(screenshot_path)
            last_screenshot = screenshot
        if key_buffer:
            action_log.append((start_time, end_time, list(key_buffer)))
            key_buffer.clear()
            start_time = end_time = None
        xdotool_command = f"xdotool mousemove {x} {y} click 1"
        powershell_command = f"Add-Type -TypeDefinition 'public class Cursor {{ [System.Runtime.InteropServices.DllImport(\"user32.dll\")] public static extern bool SetCursorPos(int x, int y); }}' ; [Cursor]::SetCursorPos({x}, {y}) ; (New-Object -ComObject wscript.shell).SendKeys('{{LEFTCLICK}}')"
        applescript_command = f"osascript -e 'tell application \"System Events\" to click at {x} {y}'"
        action_log.append((time.time(), time.time(), [xdotool_command, powershell_command, applescript_command, "OCR_PLACEHOLDER", "GPT_SUMMARY_PLACEHOLDER"]))

def on_press(key):
    global start_time, end_time
    current_keys.add(key)
    if key_buffer and time.time() - end_time > 2.0:
        action_log.append((start_time, end_time, list(key_buffer)))
        key_buffer.clear()
    if not key_buffer:
        start_time = time.time()
    if isinstance(key, Key):
        key_buffer.append(KEY_NAME_MAPPING.get(key.name, {}).get(platform.system().lower(), f'<{key.name}>'))
    else:
        key_buffer.append(str(key.char))
    end_time = time.time()
    if current_keys == stop_hotkey:
        global stop_listening
        stop_listening = True

def on_release(key):
    current_keys.discard(key)

def listen_to_input():
    with MouseListener(on_click=on_click) as mouse_listener, KeyboardListener(on_press=on_press, on_release=on_release) as keyboard_listener:
        while not stop_listening:
            pass

def start_listening():
    threading.Thread(target=listen_to_input).start()

def stop_listening_gui():
    global stop_listening
    stop_listening = True

root = tk.Tk()
start_button = tk.Button(root, text="Start", command=start_listening)
stop_button = tk.Button(root, text="Stop", command=stop_listening_gui)
task_name_entry = tk.Entry(root)
task_desc_entry = tk.Entry(root)

def save_task_info():
    task
