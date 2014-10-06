from MotionCapture import ScreenMonitor
from DisplayCanvas import Display, DisplayImage
import time

size = (700, 400)
display = Display(size)
bbox = (0, 0, 100, 200)
sm = ScreenMonitor(bbox)
timer = 0  # we take a snapshot when limit is hit
limit = 20
pause = 0.01
dims = sm.total_refresh()
display.extend(dims)
dims = []
while display.tick():
    time.sleep(pause)
    timer += 1
    if timer > limit:
        dims = sm.update()
        display.extend(dims)
        dims = []  # clear the dims array
        timer = 0

