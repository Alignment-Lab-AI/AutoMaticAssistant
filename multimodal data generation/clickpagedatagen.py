from pynput.mouse import Listener, Button
import pyautogui
import time

def on_click(x, y, button, pressed):
    if button == Button.left and pressed:
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{time.time()}_screenshot.png")
        with open("commands.log", "a") as file:
            file.write(f"{time.time()} - xdotool mousemove {x} {y} click 1\n")

with Listener(on_click=on_click) as listener:
    listener.join()

#outputs xdotool cli commands to generate a click event at a location on a screen along with a screenshot. for use in multimodal training data to teach ActualAssistant to control the UI with a mouse
