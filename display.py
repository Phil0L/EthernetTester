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
GRAY = (100, 100, 100)
GREEN = (30, 200, 80)
RED = (220, 0, 0)
ORANGE = (241, 130, 30)
BLUE = (52, 77, 160)
BROWN = (123, 84, 33)
RJ45 = [WHITE, ORANGE, WHITE, BLUE, WHITE, GREEN, WHITE, BROWN, GRAY]

screen: Surface
font: Font
small_font: Font
console_area = TouchArea(RIGHT-195, TOP, RIGHT-100, TOP+30, lambda: _console_clicked())
update_area = TouchArea(RIGHT-280, TOP, RIGHT-200, TOP+30, lambda: _update_clicked())
t568a_area = TouchArea(LEFT+60, BOTTOM-140, LEFT+160, BOTTOM-90, lambda: None)
t568b_area = TouchArea(LEFT+160, BOTTOM-140, LEFT+260, BOTTOM-90, lambda: None)
update_callback = None
console_callback = None


def initialize():
    global screen
    global font
    global small_font
    os.putenv("DISPLAY", ":0")
    pygame.display.init()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.FULLSCREEN)
    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    small_font = pygame.font.SysFont(pygame.font.get_default_font(), 23)
    draw(Data(), Data())


def draw(data: Data, last: Data):
    screen.fill(BLACK)
    if data is None:
        return
    if data != last:
        print(f"DEBUG draw data: {str(data)}")
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
    if data.charge_data.charging:
        screen.blit(font.render("{:3.1f}%+".format(data.charge_data.charge), False, WHITE), (RIGHT-80, TOP+3))
    else:
        screen.blit(font.render("{:3.1f}%".format(data.charge_data.charge), False, WHITE), (RIGHT-65, TOP+3))


def _draw_left(data: Data):
    screen.fill(WHITE, Rect(LEFT+3, TOP+25, 397, BOTTOM-30))
    screen.fill(BLACK, Rect(LEFT+3, TOP+25, 397, BOTTOM-30).inflate(-2 * 2, -2 * 2))
    left = LEFT + 10
    top = TOP + 30
    screen.blit(font.render("RJ45 tester:", False, WHITE), (left, top))
    points_left = _draw_rj45(left + 20, top + 50, False, data)
    points_right = _draw_rj45(left + 300, top + 50, True, data)
    _draw_rj45_connection(points_left, points_right, data)
    _draw_rj45_mode(left + 80, BOTTOM - 120, data)


def _draw_rj45(left, start_top, inverted, data: Data):
    points = []
    line_width = 5
    line_start = 20
    line_left = left + 20 if not inverted else left - 40
    for top in range(start_top, start_top + 9 * 30, 30):
        index = (top - start_top) // 30
        pygame.draw.line(screen, RJ45[index], (line_left, top + 5), (line_left + line_start, top + 5), line_width)
        screen.blit(font.render(str(index + 1) if index < 8 else "S", False, GREEN if data.cable_data.pin == (index + 1) % 9 and not inverted else WHITE), (left, top))
        points.append((line_left + line_start, top + 5) if not inverted else (line_left, top + 5))
    return points


def _draw_rj45_connection(points_left, points_right, data: Data):
    line_width = 5
    for key in data.cable_data:
        array_index_start = key - 1 if key > 0 else 8
        start_point = points_left[array_index_start]
        for value in data.cable_data[key]:
            array_index_end = value - 1 if value > 0 else 8
            end_point = points_right[array_index_end]
            is_correct = array_index_start == array_index_end
            pygame.draw.line(screen, RJ45[array_index_start] if is_correct else RED, start_point, end_point, line_width)


def _draw_rj45_mode(left, top, data: Data):
    screen.fill(GREEN, t568a_area.to_rect())
    screen.fill(BLACK, t568a_area.to_rect().inflate(-2 * 2, -2 * 2))
    screen.fill(RED, t568b_area.to_rect())
    screen.fill(BLACK, t568b_area.to_rect().inflate(-2 * 2, -2 * 2))
    font.set_underline(True)
    screen.blit(font.render("T-568A", False, WHITE), (left + 5, top + 3))
    screen.blit(font.render("T-568B", False, WHITE), (left + 95, top + 3))
    if t568a_area not in touch.touch_areas:
        touch.touch_areas.append(t568a_area)
    if t568b_area not in touch.touch_areas:
        touch.touch_areas.append(t568b_area)
    font.set_underline(False)


def _draw_right(data: Data):
    screen.fill(WHITE, Rect(LEFT+403, TOP+25, 397, BOTTOM-30))
    screen.fill(BLACK, Rect(LEFT+403, TOP+25, 397, BOTTOM-30).inflate(-2 * 2, -2 * 2))
    left = LEFT+406
    top = TOP+30
    screen.blit(font.render("IP tester:", False, WHITE), (left, top))
    screen.blit(font.render("IP v4 address:", False, WHITE), (left, top+40))
    screen.blit(small_font.render(data.ip_data.ipv4 if data.ip_data.ipv4 != "" else data.ip_data.wlan, False, GREEN if data.ip_data.ipv4 != "" else RED), (left, top+65))
    screen.blit(font.render("IP v6 address:", False, WHITE), (left, top+105))
    screen.blit(small_font.render(data.ip_data.ipv6, False, GREEN), (left, top+130))
    screen.blit(font.render("Speed:", False, WHITE), (left, top+170))
    screen.blit(small_font.render(data.ip_data.speed, False, GREEN), (left, top+195))
