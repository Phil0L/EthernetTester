#!/usr/bin/env python
import os
import sys

import evdev
import pygame
import select
import time

# Very important: the exact pixel size of the TFT screen must be known, so we can build graphics at this exact format
DISPLAY_SIZE = (800, 480)
DISPLAY_FB = "/dev/fb0"
DISPLAY_TOUCH = "/dev/input/event0"


def refresh():
    # We open the TFT screen's framebuffer as a binary file. Note that we will write bytes into it, hence the "wb"
    # operator
    f = open(DISPLAY_FB, "wb")
    # According to the TFT screen specs, it supports only 16bits pixels depth Pygame surfaces use 24bits pixels depth
    # by default, but the surface itself provides a very handy method to convert it. once converted, we write the
    # full byte buffer of the pygame surface into the TFT screen framebuffer like we would in a plain file:
    f.write(lcd.get_buffer().raw)
    # We can then close our access to the framebuffer
    f.close()
    time.sleep(0.1)


class Touch:
    touch_down_timestamp = 0
    touch_x_timestamp = 0
    touch_y_timestamp = 0
    touch_x_value = 0
    touch_y_value = 0


def parse_event(event, data):
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
        print("touch at: {0}:{1}".format(data.touch_x_value, data.touch_x_value))
        pygame.draw.circle(lcd, (255, 0, 0), [data.touch_y_value, data.touch_x_value], 10, 2)
        refresh()


if __name__ == "__main__" and "1" in sys.argv:
    # Note that we don't instantiate any display!
    pygame.init()

    # The pygame surface we are going to draw onto.
    # /!\ It must be the exact same size of the target display /!\
    lcd = pygame.Surface(DISPLAY_SIZE, depth=16)

    # Now we've got a function that can get the bytes from a pygame surface to the TFT framebuffer,
    # we can use the usual pygame primitives to draw on our surface before calling the refresh function.

    # Here we just blink the screen background in a few colors with the "Hello World!" text
    pygame.font.init()
    defaultFont = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    lcd.fill((0, 0, 0))
    lcd.blit(defaultFont.render("Hello World!", False, (255, 255, 255)), (0, 0))
    refresh()

    # We use evdev to read events from our touchscreen
    # (The device must exist and be properly installed for this to work)
    touch = evdev.InputDevice(DISPLAY_TOUCH)

    # We make sure the events from the touchscreen will be handled only by this program
    # (so the mouse pointer won't move on X when we touch the TFT screen)
    touch.grab()
    touch_data = Touch()

    # This loop allows us to write red dots on the screen where we touch it
    while True:
        # TOD O get the right e-codes instead of int
        r, w, x = select.select([touch], [], [])
        for ev in touch.read():
            parse_event(ev, touch_data)

if __name__ == "__main__" and "2" in sys.argv:
    # Based on "Python GUI in Linux frame buffer"
    # http://www.karoltomala.com/blog/?p=679
    disp_no = os.getenv("DISPLAY")
    if disp_no:
        print("I'm running under X display = {0}".format(disp_no))

    # Check which frame buffer drivers are available
    # Start with fbcon since directfb hangs with composite output
    drivers = ['fbcon', 'directfb', 'svgalib', 'xvfb', 'x11']
    found = False
    os.putenv("DISPLAY", ":0")
    for driver in drivers:
        # Make sure that SDL_VIDEODRIVER is set
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)
        try:
            pygame.display.init()
        except pygame.error:
            print('Driver: {0} failed.'.format(driver))
            continue
        found = True
        break

    if not found:
        raise Exception('No suitable video driver found!')

    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    print("Framebuffer size: %d x %d" % (size[0], size[1]))
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill((255, 0, 0))
    pygame.display.update()
    time.sleep(300)
    pygame.quit()

if __name__ == "__main__" and "3" in sys.argv:
    pygame.display.init()
    pygame.init()
    print(pygame.display.Info())
    lcd = pygame.display.set_mode(DISPLAY_SIZE)
    lcd.fill((255, 0, 0))
    pygame.display.flip()
