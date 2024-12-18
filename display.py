#!/usr/bin/env python
import contextlib
import os
with contextlib.redirect_stdout(None):
    import pygame
    from pygame import Surface, Rect
    from pygame.font import Font

import touch
from touch import TouchArea
from data import Data

DISPLAY_SIZE = (800, 480)
LEFT = 0
RIGHT = 800
TOP = 0
BOTTOM = 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen: Surface
font: Font
console_area = TouchArea(RIGHT-195, TOP, RIGHT-100, TOP+30, lambda: _console_clicked())
update_area = TouchArea(RIGHT-280, TOP, RIGHT-200, TOP+30, lambda: _update_clicked())
update_callback = None
console_callback = None


def initialize():
    global screen
    global font
    os.putenv("DISPLAY", ":0")
    pygame.display.init()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.FULLSCREEN)
    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    draw(Data())


def draw(data: Data):
    screen.fill(BLACK)
    if data is None:
        return
    json = data.toJSON().replace('\n', '')
    if data.frame_count % 300 == 0:
        print(f"DEBUG data to draw = {json}")
    screen.blit(font.render(f"Ethernet tester v {data.version}", False, WHITE), (LEFT + 3, TOP + 3))
    _draw_update(data)
    _draw_console(data)
    _draw_charge(data)
    _draw_left(data)
    _draw_right(data)

    pygame.display.update()


def on_update_clicked(callback):
    global update_callback
    update_callback = callback


def on_console_clicked(callback):
    global console_callback
    console_callback = callback


def _update_clicked():
    if callable(update_callback):
        update_callback()


def _console_clicked():
    if callable(console_callback):
        console_callback()


def _draw_update(data: Data):
    if data.update_count <= 0:
        while update_area in touch.touch_areas:
            touch.touch_areas.remove(update_area)
    else:
        # screen.fill(WHITE, update_area.to_rect())
        # screen.fill(BLACK, update_area.to_rect().inflate(-2 * 2, -2 * 2))
        font.set_underline(True)
        screen.blit(font.render("Update", False, WHITE), (update_area.left+5, TOP+3))
        if update_area not in touch.touch_areas:
            touch.touch_areas.append(update_area)
        font.set_underline(False)


def _draw_console(data: Data):
    # screen.fill(WHITE, console_area.to_rect())
    # screen.fill(BLACK, console_area.to_rect().inflate(-2 * 2, -2 * 2))
    font.set_underline(True)
    screen.blit(font.render("Console", False, WHITE), (console_area.left+5, TOP+3))
    if console_area not in touch.touch_areas:
        touch.touch_areas.append(console_area)
    font.set_underline(False)


def _draw_charge(data: Data):
    if data.charging:
        screen.blit(font.render("{:3.1f}%+".format(data.charge), False, WHITE), (RIGHT-80, TOP+3))
    else:
        screen.blit(font.render("{:3.1f}%".format(data.charge), False, WHITE), (RIGHT-65, TOP+3))


def _draw_left(data: Data):
    screen.fill(WHITE, Rect(LEFT+3, TOP+25, 397, BOTTOM-30))
    screen.fill(BLACK, Rect(LEFT+3, TOP+25, 397, BOTTOM-30).inflate(-2 * 2, -2 * 2))


def _draw_right(data: Data):
    screen.fill(WHITE, Rect(LEFT+403, TOP+25, 397, BOTTOM-30))
    screen.fill(BLACK, Rect(LEFT+403, TOP+25, 397, BOTTOM-30).inflate(-2 * 2, -2 * 2))
