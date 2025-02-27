#!/usr/bin/env python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# BLOCKED: GPIO 0, 1, 2, 3 (I2C of the battery pack)
# FREE   : GPIO 13, 19, 26, 16, 20, 21
# https://raw.githubusercontent.com/AchimPieters/pinout/main/Raspberry%20Pi/Raspberry-pin-out-overview.pdf

IN_1 = 14  # GPIO 14, PIN 8
IN_2 = 15  # GPIO 15, PIN 10
IN_3 = 18  # GPIO 18, PIN 12
IN_4 = 23  # GPIO 23, PIN 16
IN_5 = 24  # GPIO 24, PIN 18
IN_6 = 25  # GPIO 25, PIN 22
IN_7 = 8   # GPIO 8,  PIN 24
IN_8 = 7   # GPIO 7,  PIN 26
IN_S = 12  # GPIO 12, PIN 32
IN_POE = 13# GPIO 13, PIN 33

OUT_1 = 4   # GPIO 4,  PIN 7
OUT_2 = 17  # GPIO 17, PIN 11
OUT_3 = 27  # GPIO 27, PIN 13
OUT_4 = 22  # GPIO 22, PIN 15
OUT_5 = 10  # GPIO 10, PIN 19
OUT_6 = 9   # GPIO 9,  PIN 21
OUT_7 = 11  # GPIO 11, PIN 23
OUT_8 = 5   # GPIO 5,  PIN 29
OUT_S = 6   # GPIO 6,  PIN 31

GPIO.setup(IN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_S, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_POE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(OUT_1, GPIO.OUT)
GPIO.setup(OUT_2, GPIO.OUT)
GPIO.setup(OUT_3, GPIO.OUT)
GPIO.setup(OUT_4, GPIO.OUT)
GPIO.setup(OUT_5, GPIO.OUT)
GPIO.setup(OUT_6, GPIO.OUT)
GPIO.setup(OUT_7, GPIO.OUT)
GPIO.setup(OUT_8, GPIO.OUT)
GPIO.setup(OUT_S, GPIO.OUT)


def all_on():
    GPIO.output(OUT_2, True)
    GPIO.output(OUT_1, True)
    GPIO.output(OUT_3, True)
    GPIO.output(OUT_4, True)
    GPIO.output(OUT_5, True)
    GPIO.output(OUT_6, True)
    GPIO.output(OUT_7, True)
    GPIO.output(OUT_8, True)
    GPIO.output(OUT_S, True)


def all_off():
    GPIO.output(OUT_1, False)
    GPIO.output(OUT_2, False)
    GPIO.output(OUT_3, False)
    GPIO.output(OUT_4, False)
    GPIO.output(OUT_5, False)
    GPIO.output(OUT_6, False)
    GPIO.output(OUT_7, False)
    GPIO.output(OUT_8, False)
    GPIO.output(OUT_S, False)


current_pin = 0
current_output = []
current_pin_start = 0
speed_up = False
speed_up_count = 0


def test(data):
    global current_pin
    global current_output
    global current_pin_start
    global speed_up
    global speed_up_count

    frame = data.frame_count
    fps = int(data.frames_per_second)
    pin_test_length = fps // 4 if speed_up else fps
    if pin_test_length == 0:
        pin_test_length = 2**8
    # test each pin for 3/4 second, then wait 1/4 second
    # measure each voltage at each frame
    if frame - current_pin_start > pin_test_length:
        current_pin = (current_pin + 1) % 9
        current_pin_start = frame
        if speed_up:
            speed_up_count += 1
        if speed_up_count >= 9:
            speed_up_count = 0
            speed_up = False
    if frame - current_pin_start < pin_test_length // 4:
        # reset
        current_output = []
        all_off()
        pass

    if current_pin == 1:
        GPIO.output(OUT_1, True)
    if current_pin == 2:
        GPIO.output(OUT_2, True)
    if current_pin == 3:
        GPIO.output(OUT_3, True)
    if current_pin == 4:
        GPIO.output(OUT_4, True)
    if current_pin == 5:
        GPIO.output(OUT_5, True)
    if current_pin == 6:
        GPIO.output(OUT_6, True)
    if current_pin == 7:
        GPIO.output(OUT_7, True)
    if current_pin == 8:
        GPIO.output(OUT_8, True)
    if current_pin == 0:
        GPIO.output(OUT_S, True)
    current_output = _read(current_output)
    last_output = data.cable_data.get(current_pin, [])
    if len(last_output) != len(current_output) and not speed_up:
        speed_up = True
    if len(current_output) == 9: # unplugged
        return current_pin, []
    return current_pin, current_output


def _read(last):
    if 0 not in last:
        if GPIO.input(IN_S):
            last.append(0)
    if 1 not in last:
        if GPIO.input(IN_1):
            last.append(1)
    if 2 not in last:
        if GPIO.input(IN_2):
            last.append(2)
    if 3 not in last:
        if GPIO.input(IN_3):
            last.append(3)
    if 4 not in last:
        if GPIO.input(IN_4):
            last.append(4)
    if 5 not in last:
        if GPIO.input(IN_5):
            last.append(5)
    if 6 not in last:
        if GPIO.input(IN_6):
            last.append(6)
    if 7 not in last:
        if GPIO.input(IN_7):
            last.append(7)
    if 8 not in last:
        if GPIO.input(IN_8):
            last.append(8)
    return last


def test_poe():
    return GPIO.input(IN_POE)
