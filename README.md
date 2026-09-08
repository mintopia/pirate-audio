# Pirate Audio on non-Pi single-board computers

Device-tree overlays and test scripts for running the
[Pimoroni Pirate Audio](https://shop.pimoroni.com/collections/pirate-audio) range
(PCM5102A I2S DAC + ST7789 display + 4 buttons) on single-board computers other
than the Raspberry Pi, where the Pi setup (`config.txt`, `hifiberry-dac`,
BCM pin numbers) does not apply.

Each board has its own directory with overlays, tests, and setup notes.

## Boards

| Board | SoC | OS / kernel | DAC | Display | Buttons |
|-------|-----|-------------|-----|---------|---------|
| [Orange Pi Zero 2W](orange-pi-zero-2w/) | Allwinner H618 | Armbian, mainline 6.18 | working | working | working |

## Adding a board

Copy the layout of an existing board directory:

```
<board-name>/
  README.md      # pin mapping, install steps, verify commands
  overlays/      # .dts sources
  examples/      # display/button test scripts
```

The hard part is always the same: find which SoC pins the HAT's fixed header
positions land on, and which audio DAI reaches the I2S pins. Each board's README
records that mapping.
