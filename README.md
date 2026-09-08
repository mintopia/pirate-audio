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

## License

MIT License

Copyright (c) 2026 mintopia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
