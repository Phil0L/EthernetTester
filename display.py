#!/usr/bin/env python

import os
import pygame
import select
from pygame import Surface
from pygame.font import Font

from data import Data

DISPLAY_SIZE = (800, 480)

screen: Surface
font: Font


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
    draw(Data())


def draw(data: Data):
    global screen
    global font
    screen.fill((0, 0, 0))
    if data is None:
        return
    screen.blit(font.render(f"Ethernet tester v {data.version}", False, (255, 255, 255)), (3, 3))

    pygame.display.update()
