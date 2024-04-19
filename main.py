import pyaudio as p
import pygame
import math
import time

FORMAT = p.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SQUARE_SIZE = 50
GAP = 10
SQUARES = 40
MAX_LEVEL = 8000

audio = p.PyAudio()

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)


print("Recording...")

def audioInputLevel(data):
    rms = 0
    for i in range(0, len(data), 2):
        sample = int.from_bytes(data[i:i+2], byteorder='little', signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (len(data) / 2))
    return rms

def draw_squares(surface, color, x, y, size, gap, n, level):
    for i in range(n):
        if x + (size + gap) * i > WIDTH:
            x = 50
            y += 100
        if i == n-1:
            Ncolor = calcColor(level, n)
            pygame.draw.rect(surface, Ncolor, (x + (size + gap) * i, y, size, size))
        else:
            pygame.draw.rect(surface, color, (x + (size + gap) * i, y, size, size))


def calcSquares(input):
    unitLevel = MAX_LEVEL/ SQUARES
    num = math.ceil(input / unitLevel)
    return num

def calcColor(level, no):
    unitLevel = MAX_LEVEL/ SQUARES
    remainingLevel = abs(level - (no * unitLevel))
    rgb = int((remainingLevel / unitLevel) * 255)
    print("RGB", rgb)
    return (rgb, rgb ,rgb)
    



WIDTH = 1000
HEIGHT = 500
pygame.init()
pygame.display.set_caption("Visualizer")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
max = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
        level = audioInputLevel(data)
        print(level)
    except IOError as ex:
        print(ex)
    SQUARE_LEVEL = calcSquares(level)
    screen.fill((0,0,0))
    draw_squares(screen, (255,255,255), 50, 50, SQUARE_SIZE, GAP, SQUARE_LEVEL, level)
    if level > max : max = level

    pygame.display.flip()

    clock.tick(10)
print("Max = ", max)
pygame.quit()
