#!/usr/bin/env python3
# Pirate Audio button test on Orange Pi Zero 2W. Active-low, internal pull-ups.
import time, gpiod
from gpiod.line import Direction, Bias, Value

CHIP = "/dev/gpiochip1"
BUTTONS = {256: "A", 271: "B", 76: "X", 228: "Y"}  # PI0, PI15, PC12, PH4

cfg = {off: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP)
       for off in BUTTONS}
req = gpiod.request_lines(CHIP, consumer="pirate-buttons", config=cfg)

print("Press each button (A B X Y). Watching 25s...", flush=True)
state = {off: Value.ACTIVE for off in BUTTONS}
seen = set()
end = time.time() + 25
while time.time() < end:
    for off, name in BUTTONS.items():
        v = req.get_value(off)
        if v == Value.INACTIVE and state[off] == Value.ACTIVE:
            print(f"  {name} pressed", flush=True)
            seen.add(name)
        state[off] = v
    time.sleep(0.02)
print("seen:", " ".join(sorted(seen)) or "NONE", flush=True)
