#!/usr/bin/env python3
# Minimal ST7789 240x240 fill test for Pirate Audio on Orange Pi Zero 2W.
import time, spidev, gpiod
from gpiod.line import Direction, Value

CHIP = "/dev/gpiochip1"
DC = 232        # PH8, phys21
BACKLIGHT = 268  # PI12, phys33
W = H = 240

req = gpiod.request_lines(CHIP, consumer="pirate-lcd", config={
    DC: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    BACKLIGHT: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.ACTIVE),
})

spi = spidev.SpiDev()
spi.open(1, 1)              # /dev/spidev1.1
spi.max_speed_hz = 40000000
spi.mode = 0

def cmd(c):
    req.set_value(DC, Value.INACTIVE)
    spi.writebytes([c])

def data(d):
    req.set_value(DC, Value.ACTIVE)
    for i in range(0, len(d), 4096):
        spi.writebytes2(d[i:i+4096])

def init():
    cmd(0x01); time.sleep(0.15)     # SWRESET
    cmd(0x11); time.sleep(0.12)     # SLPOUT
    cmd(0x3A); data([0x55])         # COLMOD 16bit
    cmd(0x36); data([0x00])         # MADCTL
    cmd(0x21)                       # INVON (IPS panels)
    cmd(0x13)                       # NORON
    cmd(0x29); time.sleep(0.02)     # DISPON

def fill(r, g, b):
    px = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    hi, lo = px >> 8, px & 0xFF
    cmd(0x2A); data([0, 0, 0, W-1])   # CASET 0..239
    cmd(0x2B); data([0, 0, 0, H-1])   # RASET 0..239
    cmd(0x2C)                          # RAMWR
    data([hi, lo] * (W * H))

init()
for name, rgb in [("RED", (255,0,0)), ("GREEN", (0,255,0)), ("BLUE", (0,0,255)), ("WHITE", (255,255,255))]:
    print(name, flush=True)
    fill(*rgb)
    time.sleep(1.2)
print("done - screen left WHITE")
