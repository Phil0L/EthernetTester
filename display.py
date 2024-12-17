#!/usr/bin/env python

import os
from typing import Any
import evdev

import pygame
import select
from pygame import Surface
from pygame.font import Font

DISPLAY_SIZE = (800, 480)
DISPLAY_FB = "/dev/fb0"
DISPLAY_TOUCH = "/dev/input/event0"

screen: Surface
font: Font
touch: Any


def initialize():
    global screen
    global font
    global touch
    os.putenv("DISPLAY", ":0")
    pygame.display.init()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.FULLSCREEN)
    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    draw()

    touch = evdev.InputDevice(DISPLAY_TOUCH)
    touch.grab()


def draw():
    global screen
    global font
    screen.fill((100, 0, 0))
    screen.blit(font.render("Ethernet tester v.1", False, (255, 255, 255)), (3, 3))

    pygame.display.update()


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



