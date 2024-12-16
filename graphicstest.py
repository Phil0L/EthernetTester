#!/usr/bin/env python

##
# Prerequisites:
# A Touchscreen properly installed on your system:
# - a device to output to it, e.g. /dev/fb0
# - a device to get input from it, e.g. /dev/input/event0
##

import evdev
import pygame
import select
import time

# Very important: the exact pixel size of the TFT screen must be known, so we can build graphics at this exact format
surfaceSize = (800, 480)

# Note that we don't instantiate any display!
pygame.init()

# The pygame surface we are going to draw onto.
# /!\ It must be the exact same size of the target display /!\
lcd = pygame.Surface(surfaceSize, depth=16)


# This is the important bit
def refresh():
    # We open the TFT screen's framebuffer as a binary file. Note that we will write bytes into it, hence the "wb"
    # operator
    f = open("/dev/fb0", "wb")
    # According to the TFT screen specs, it supports only 16bits pixels depth Pygame surfaces use 24bits pixels depth
    # by default, but the surface itself provides a very handy method to convert it. once converted, we write the
    # full byte buffer of the pygame surface into the TFT screen framebuffer like we would in a plain file:
    f.write(lcd.get_buffer())
    # We can then close our access to the framebuffer
    f.close()
    time.sleep(0.1)


# Now we've got a function that can get the bytes from a pygame surface to the TFT framebuffer,
# we can use the usual pygame primitives to draw on our surface before calling the refresh function.

# Here we just blink the screen background in a few colors with the "Hello World!" text
pygame.font.init()
defaultFont = pygame.font.SysFont(pygame.font.get_default_font(), 30)

lcd.fill((255, 0, 0))
lcd.blit(defaultFont.render("Hello World!", False, (0, 0, 0)), (0, 0))
refresh()

lcd.fill((0, 255, 0))
lcd.blit(defaultFont.render("Hello World!", False, (0, 0, 0)), (0, 0))
refresh()

lcd.fill((0, 0, 255))
lcd.blit(defaultFont.render("Hello World!", False, (0, 0, 0)), (0, 0))
refresh()

lcd.fill((0, 0, 0))
lcd.blit(defaultFont.render("Hello World!", False, (255, 255, 255)), (0, 0))
refresh()

##
# Everything that follows is for handling the touchscreen touch events via evdev
##

# Used to map touch event from the screen hardware to the pygame surface pixels.
# (Those values have been found empirically, but I'm working on a simple interactive calibration tool
tftOrig = (3750, 180)
tftEnd = (150, 3750)
tftDelta = (tftEnd[0] - tftOrig[0], tftEnd[1] - tftOrig[1])
tftAbsDelta = (abs(tftEnd[0] - tftOrig[0]), abs(tftEnd[1] - tftOrig[1]))

# We use evdev to read events from our touchscreen
# (The device must exist and be properly installed for this to work)
touch = evdev.InputDevice('/dev/input/event0')

# We make sure the events from the touchscreen will be handled only by this program
# (so the mouse pointer won't move on X when we touch the TFT screen)
touch.grab()


# Prints some info on how evdev sees our input device
# print(touch)


# Even more info for curious people
# print(touch.capabilities())

# Here we convert the evdev "hardware" touch coordinates into pygame surface pixel coordinates
def get_pixels_from_coordinates(coords):
    # TOD O check divide by 0!
    if tftDelta[0] < 0:
        x = float(tftAbsDelta[0] - coords[0] + tftEnd[0]) / float(tftAbsDelta[0]) * float(surfaceSize[0])
    else:
        x = float(coords[0] - tftOrig[0]) / float(tftAbsDelta[0]) * float(surfaceSize[0])
    if tftDelta[1] < 0:
        y = float(tftAbsDelta[1] - coords[1] + tftEnd[1]) / float(tftAbsDelta[1]) * float(surfaceSize[1])
    else:
        y = float(coords[1] - tftOrig[1]) / float(tftAbsDelta[1]) * float(surfaceSize[1])
    return int(x), int(y)


# Was useful to see what pieces I would need from the evdev events
def printEvent(ev):
    print(evdev.categorize(ev))
    print("Value: {0}".format(ev.value))
    print("Type: {0}".format(ev.type))
    print("Code: {0}".format(ev.code))


touch_down_timestamp = 0
touch_x_timestamp = 0
touch_y_timestamp = 0
touch_x_value = 0
touch_y_value = 0


def parse_event(event):
    global touch_down_timestamp
    global touch_x_timestamp
    global touch_y_timestamp
    global touch_x_value
    global touch_y_value

    #printEvent(event)
    if event.type == evdev.ecodes.EV_ABS:
        if event.code == 1:
            touch_x_value = event.value
            touch_x_timestamp = event.timestamp()
        elif event.code == 0:
            touch_y_value = event.value
            touch_y_timestamp = event.timestamp()
    elif event.type == evdev.ecodes.EV_KEY:
        if event.code == 330 and event.value == 1:
            touch_down_timestamp = event.timestamp()
    if touch_down_timestamp == touch_x_timestamp == touch_y_timestamp:
        print(f"Touch at: {touch_x_value}, {touch_y_value}")


# This loop allows us to write red dots on the screen where we touch it
while True:
    # TOD O get the right e-codes instead of int
    r, w, x = select.select([touch], [], [])
    for ev in touch.read():
        parse_event(ev)
