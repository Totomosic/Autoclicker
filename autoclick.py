from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import argparse
import time
import threading
import random
import sys

mouse = Controller()

class Clicker(threading.Thread):
    def __init__(self, interval, jitter, button, timeout=None):
        super(Clicker, self).__init__()
        self.interval = interval
        self.jitter = jitter
        self.button = button
        # Timeout in seconds
        self.timeout = timeout
        self.start_time = time.time()

        self.program_running = True
        self.clicking = False

    def resume_clicking(self):
        self.clicking = True
        self.start_time = time.time()
        print("Started clicking...")

    def pause_clicking(self):
        self.clicking = False
        print("Stopped clicking")

    def exit(self):
        self.pause_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.clicking:
                mouse.click(self.button)
                direction = random.randint(0, 1)
                interval = self.interval / 1000 + ( -random.randrange(0, self.jitter[0]) if direction == 0 else random.randrange(0, self.jitter[1]) ) / 1000
                time.sleep(interval)
                if self.timeout is not None and time.time() - self.start_time > self.timeout:
                    self.pause_clicking()
            time.sleep(0.1)

PAUSE_KEY = KeyCode(char='s')
EXIT_KEY = KeyCode(char='e')

parser = argparse.ArgumentParser("Autoclicker")
parser.add_argument("-i", "--interval", type=int, required=True, help="Time in milliseconds between clicks")
parser.add_argument("-jmin", "--min-jitter", type=int, default=0, help="Time in milliseconds to subtract from interval")
parser.add_argument("-jmax", "--max-jitter", type=int, default=0, help="Time in milliseconds to add to interval")
parser.add_argument("--timeout", type=int, required=False, help="Time in seconds after which to stop")

args = parser.parse_args()

print("Python Autoclicker")
print("Press s to start/stop clicking")
print("Press e to exit")

interval = args.interval
jitter = (args.min_jitter, args.max_jitter)
timeout = None
if "timeout" in args:
    timeout = args.timeout

clicker = Clicker(interval, jitter, Button.left, timeout)
clicker.start()

def on_key_press(key):
    if key == PAUSE_KEY:
        if clicker.clicking:
            clicker.pause_clicking()
        else:
            clicker.resume_clicking()
    elif key == EXIT_KEY:
        clicker.exit()
        print("Exited...")
        sys.exit()

with Listener(on_press=on_key_press) as listener:
    listener.join()
clicker.join()
