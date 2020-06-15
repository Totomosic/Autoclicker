import pynput
import time
import sys

clicks = []

print("Analyzing clicks...")
print("Press any key to stop analyzing")

def on_key_pressed(key):
    # Done
    if key != pynput.keyboard.KeyCode(char='e'):
        return
    if len(clicks) > 0:
        start_time = clicks[0]
        avg_interval = 0
        min_interval = 100000
        max_interval = -100000
        for i in range(1, len(clicks)):
            interval = clicks[i] - clicks[i - 1]
            avg_interval += interval * (1.0 / (len(clicks) - 1))
            if interval > max_interval:
                max_interval = interval
            if interval < min_interval:
                min_interval = interval
        print("Average Interval {}ms".format(int(avg_interval * 1000)))
        print("Min {}ms".format(min_interval * 1000))
        print("Max {}ms".format(max_interval * 1000))
    else:
        print("No clicks")
    sys.exit()

def on_click(x, y, button, pressed):
    if pressed:
        clicks.append(time.time())

with pynput.mouse.Listener(on_click=on_click) as listener:
    with pynput.keyboard.Listener(on_press=on_key_pressed) as key_listener:
        key_listener.join()
    sys.exit()
