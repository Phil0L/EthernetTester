#!/usr/bin/env python

import os
import evdev
from threading import Thread

import pygame
from pygame import Surface
from pygame.font import Font

DISPLAY_SIZE = (800, 480)
DISPLAY_FB = "/dev/fb0"
DISPLAY_TOUCH = "/dev/input/event0"

screen: Surface
font: Font


def initialize():
    global screen
    global font
    os.putenv("DISPLAY", ":0")
    pygame.display.init()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.FULLSCREEN)
    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    screen.fill((100, 0, 0))
    draw()

    touch_thread = Thread(target=_touch_loop)
    touch_thread.start()


def draw():
    screen.blit(font.render("Ethernet tester v.1", False, (255, 255, 255)), (3, 3))

    pygame.display.update()


class _Touch:
    touch_down_timestamp = 0
    touch_x_timestamp = 0
    touch_y_timestamp = 0
    touch_x_value = 0
    touch_y_value = 0


def _parse_event(event, data, click_callback):
    # printEvent(event)
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


def _touched(x, y):
    print(f"Touch at: {x}|{y}")


def _touch_loop():
    touch = evdev.InputDevice(DISPLAY_TOUCH)
    touch.grab()
    touch_data = _Touch()
    while True:
        # TOD O get the right e-codes instead of int
        # r, w, x = select.select([touch], [], [])
        for ev in touch.read():
            _parse_event(ev, touch_data, lambda _x, _y: _touched(_x, _y))
