#!/usr/bin/env python

import os
import pygame
from pygame import Surface
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
    screen.blit(font.render(f"Ethernet tester v {data.version}", False, WHITE), (TOP + 3, LEFT + 3))
    _draw_update(data)

    pygame.display.update()


def _update_clicked():
    pass


def _draw_update(data: Data):
    font.set_underline(True)
    screen.blit(font.render("Update", False, WHITE), (TOP + 3, RIGHT - 50))
    touch.touch_areas.append(TouchArea(RIGHT - 50, TOP + 3, RIGHT - 3, TOP + 30, lambda _: _update_clicked()))
    font.set_underline(False)
