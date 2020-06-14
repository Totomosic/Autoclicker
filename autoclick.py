from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import argparse
import time
import threading
import random
import sys

mouse = Controller()

class Clicker(threading.Thread):
    def __init__(self, interval, jitter, button):
        super(Clicker, self).__init__()
        self.interval = interval
        self.jitter = jitter
        self.button = button

        self.program_running = True
        self.clicking = False

    def resume_clicking(self):
        self.clicking = True

    def pause_clicking(self):
        self.clicking = False

    def exit(self):
        self.pause_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.clicking:
                mouse.click(self.button)
                direction = random.randint(0, 1)
                interval = self.interval / 1000 + ( -random.randrange(0, self.jitter[0]) if direction == 0 else random.randrange(0, self.jitter[1]) ) / 1000
                # print("Interval: {}ms".format(int(interval * 1000)))
                time.sleep(interval)
            time.sleep(0.1)

PAUSE_KEY = KeyCode(char='s')
EXIT_KEY = KeyCode(char='e')

print("Python Autoclicker")
print("Press s to start/stop clicking")
print("Press e to exit")

parser = argparse.ArgumentParser("Autoclicker")
parser.add_argument("-i", "--interval", type=int, required=True, help="Time in milliseconds between clicks")
parser.add_argument("-jmin", "--min-jitter", type=int, default=0, help="Time in milliseconds to subtract from interval")
parser.add_argument("-jmax", "--max-jitter", type=int, default=0, help="Time in milliseconds to add to interval")

args = parser.parse_args()

interval = args.interval
jitter = (args.min_jitter, args.max_jitter)

clicker = Clicker(interval, jitter, Button.left)
clicker.start()

def on_key_press(key):
    if key == PAUSE_KEY:
        if clicker.clicking:
            clicker.pause_clicking()
            print("Stop clicking...")
        else:
            clicker.resume_clicking()
            print("Start clicking")
    elif key == EXIT_KEY:
        clicker.exit()
        print("Exited...")
        sys.exit()

with Listener(on_press=on_key_press) as listener:
    listener.join()
clicker.join()
