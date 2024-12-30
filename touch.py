#!/usr/bin/env python
import threading

import evdev
from typing import Any

import select
from pygame import Rect

DISPLAY_TOUCH = "/dev/input/event0"

touch: Any
touch_areas = []
stop_signal = False


def initialize():
    global touch
    touch = evdev.InputDevice(DISPLAY_TOUCH)
    touch.grab()


def check_touch(touch_data):
    try:
        _read, _write, _execute = select.select([touch], [], [])
        ev = touch.read_one()
        if ev is not None:
            _parse_event(ev, touch_data, lambda _x, _y: _check_touch_area(_x, _y))
    except IOError:
        print("Error reading touch screen.")


def _parse_event(event, data, click_callback):
    if event.type == evdev.ecodes.EV_ABS:
        if event.code == 0:
            data.touch_x_value = event.value
            data.touch_x_timestamp = event.timestamp()
        elif event.code == 1:
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


class TouchArea:
    left = 0
    top = 0
    right = 0
    bottom = 0
    callback = None

    def __init__(self, left, top, right, bottom, callback):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.callback = callback

    def is_inside(self, x, y):
        print(f"DEBUG {self.left} < {x} < {self.right} | {self.top} < {y} < {self.bottom}")
        return self.left < x < self.right and self.top < y < self.bottom

    def execute(self):
        if self.callback is not None:
            self.callback()

    def to_rect(self):
        return Rect(self.left, self.top, self.right-self.left, self.bottom-self.top)


def _check_touch_area(x, y):
    print(f"DEBUG touched screen")
    for touch_area in touch_areas:
        if touch_area.is_inside(x, y):
            print(f"DEBUG touch area hit")
            touch_area.execute()


def start_touch_loop(touch_data):
    thread = threading.Thread(target=_touch_loop, args=(touch_data,))
    thread.start()


def _touch_loop(data):
    while not stop_signal:
        check_touch(data)
