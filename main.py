import neopixel
from machine import Pin
import time

CHUNK_X = 4
CHUNK_Y = 2
CHUNK_Z = 8
CHUNK_SIZE = 64
CHUNK_COUNT = 8


def test_a(ctrl, slideup_ms, interval_ms):
    for z_change in range(CHUNK_Z):
        for l in range(CHUNK_X * CHUNK_Y):
            for i in ctrl:
                i[(l+1)*CHUNK_Z - (z_change+1) if l % 2 else l*CHUNK_Z + z_change] = (20, 20, 20)
        for i in ctrl:
            i.write()
        time.sleep_ms(slideup_ms)
    for i in range(CHUNK_SIZE):
        for c in ((0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 0, 0)):
            for j in ctrl:
                j[i] = c
                j.write()
            time.sleep_ms(interval_ms)
        

def btu_a(ctrl, color, interval_ms):
    for z_change in range(CHUNK_Z):
        for l in range(CHUNK_X * CHUNK_Y):
            for i in ctrl:
                i[(l+1)*CHUNK_Z - (z_change+1) if l % 2 else l*CHUNK_Z + z_change] = color
        for i in ctrl:
            i.write()
        time.sleep_ms(interval_ms)
        for l in range(CHUNK_X * CHUNK_Y):
            for i in ctrl:
                i[(l+1)*CHUNK_Z - (z_change+1) if l % 2 else l*CHUNK_Z + z_change] = (0, 0, 0)


def disp110(ctrl, interval_ms, susp_ms, reveal_ms, stop_ms, font_color):
    FONT_110 = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    for z_change in range(CHUNK_Z):
        for c in ((0, 255, 0), (255, 0, 0), (0, 0, 255), (25, 25, 25)):
            for l in range(CHUNK_X * CHUNK_Y):
                for i in ctrl:
                    i[(l+1)*CHUNK_Z - (z_change+1) if l % 2 else l*CHUNK_Z + z_change] = c
            for i in ctrl:
                i.write()
            time.sleep_ms(interval_ms)
    time.sleep_ms(susp_ms)
    for z_change in reversed(range(CHUNK_Z)):
        for l in range(CHUNK_X * CHUNK_Y):
            for i in ctrl:
                i[(l+1)*CHUNK_Z - (z_change+1) if l % 2 else l*CHUNK_Z + z_change] = (0, 0, 0)
        for idx, i in enumerate(FONT_110[z_change][1:5]):
            if i:
                ctrl[5][(idx+1)*CHUNK_Z - (z_change+1) if idx % 2 else idx*CHUNK_Z + z_change] = font_color;
        for idx, i in enumerate(FONT_110[z_change][5:]):
            if i:
                ctrl[4][(idx+1)*CHUNK_Z - (z_change+1) if idx % 2 else idx*CHUNK_Z + z_change] = font_color;
        for i in ctrl:
            i.write()
        time.sleep_ms(reveal_ms)
    time.sleep_ms(stop_ms)


def main():
    controllers = [neopixel.NeoPixel(Pin(i+3, Pin.OUT), CHUNK_SIZE) for i in range(CHUNK_COUNT)]
    while True:
        btu_a(controllers, (0, 255, 0), 100)
        btu_a(controllers, (255, 0, 0), 100)
        btu_a(controllers, (0, 0, 255), 100)
        disp110(controllers, 25, 1000, 250, 4000, (0x16, 0x9A, 0x2A))
        test_a(controllers, 100, 4)
        
        
if __name__ == "__main__":
    main()



