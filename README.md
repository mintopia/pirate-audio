# Pirate Audio on Orange Pi Zero 2W

Device-tree overlays and test scripts to run a [Pimoroni Pirate Audio Line Out](https://shop.pimoroni.com/products/pirate-audio-line-out)
(PCM5102A I2S DAC + ST7789 240x240 display + 4 buttons) on an **Orange Pi Zero 2W**
(Allwinner H618) running **Armbian** (mainline `current` sunxi64, kernel 6.18).

The Raspberry Pi instructions do not apply — the H618 uses a different GPIO
controller, and mainline has no simple I2S driver, so audio goes through
Allwinner's BSP "AHUB" audio subsystem instead of `hifiberry-dac`.

## Pin mapping

The HAT sits on fixed physical header pins; these are the Orange Pi ports they land on.

| Function        | Pi BCM | Phys | OPi port | gpiochip1 line |
|-----------------|--------|------|----------|----------------|
| I2S BCLK        | 18     | 12   | PI1      | 257            |
| I2S LRCLK       | 19     | 35   | PI2      | 258            |
| I2S DATA        | 21     | 40   | PI3      | 259            |
| DAC enable      | 25     | 22   | PI6      | 262 (held high)|
| Display SCLK    | 11     | 23   | PH6      | 230            |
| Display MOSI    | 10     | 19   | PH7      | 231            |
| Display DC      | 9      | 21   | PH8      | 232            |
| Display CS (CE1)| 7      | 26   | PH9      | 233            |
| Backlight       | 13     | 33   | PI12     | 268            |
| Button A        | 5      | 29   | PI0      | 256            |
| Button B        | 6      | 31   | PI15     | 271            |
| Button X        | 16     | 36   | PC12     | 76             |
| Button Y        | 24     | 18   | PH4      | 228            |

Notes:
- The header's "SPI0" is Allwinner **spi1**. The overlay muxes only SCLK+MOSI so
  PH8 stays free as the display's DC line; CS1 (PH9) is a GPIO chip-select.
- Audio uses AHUB DAI **i2s0** (`tdm_num=0`). SoC is bit+frame clock master; the
  PCM5102A is a dumb DAC (no I2C control) so the overlay uses an empty codec node.
- `gpiochip1 line = bank*32 + pin` (PC=64, PH=224, PI=256).

## Install

```sh
# on the board, as root
dtc -@ -I dts -O dtb -o /boot/overlay-user/pirate-audio.dtbo overlays/pirate-audio.dts
dtc -@ -I dts -O dtb -o /boot/overlay-user/pirate-dac.dtbo   overlays/pirate-dac.dts
mkdir -p /boot/overlay-user   # if missing

# append to /boot/armbianEnv.txt:
#   user_overlays=pirate-audio pirate-dac

reboot
```

Optional — make the DAC the default ALSA output, `/etc/asound.conf`:

```
pcm.!default {
    type plug
    slave.pcm { type hw; card piratei2s }
}
ctl.!default { type hw; card piratei2s }
```

## Verify

```sh
ls /dev/spidev1.1                     # display SPI present
aplay -l | grep pirate-i2s            # sound card present
python3 examples/lcd_test.py          # cycles R/G/B/W on the screen
python3 examples/button_test.py       # prints A/B/X/Y as you press
speaker-test -t sine -f 440 -c 2      # tone out the DAC (default device)
```

`examples/` needs `python3-spidev` and `python3-libgpiod`.

## Overlays

- `overlays/pirate-audio.dts` — SPI1 display + DAC-enable gpio-hog
- `overlays/pirate-dac.dts` — AHUB i2s0 sound card (experimental on 6.18; works here)
