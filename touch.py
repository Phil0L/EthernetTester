#!/usr/bin/env python
import evdev
from typing import Any
import select

DISPLAY_TOUCH = "/dev/input/event0"

touch: Any


def initialize():
    global touch
    touch = evdev.InputDevice(DISPLAY_TOUCH)
    touch.grab()


def check_touch(touch_data, callback):
    try:
        _read, _write, _execute = select.select([touch], [], [])
        for ev in touch.read():
            _parse_event(ev, touch_data, lambda _x, _y: callback(_x, _y))
    except IOError:
        print("Error reading touch screen.")


def _parse_event(event, data, click_callback):
    if event.type == evdev.ecodes.EV_ABS:
        if event.code == 1:
            data.touch_x_value = event.value
            data.touch_x_timestamp = event.timestamp()
        elif event.code == 0:
            data.touch_y_value = event.value
            data.touch_y_timestamp = event.timestamp()
        else:
            return
    elif event.type == evdev.ecodes.EV_KEY:
        if event.code == 330 and event.value == 1:
            data.touch_down_timestamp = event.timestamp()
        else:
            return
    else:
        return
    if data.touch_down_timestamp == data.touch_x_timestamp == data.touch_y_timestamp:
        click_callback(data.touch_x_value, data.touch_y_value)
