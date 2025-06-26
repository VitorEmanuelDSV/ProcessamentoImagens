from OpenGL.GL import *
import numpy as np

def draw_pixel(x, y, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def load_pgm_ascii(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines if l.strip() and not l.startswith('#')]

    assert lines[0] == 'P2', "Formato não suportado: apenas P2 (ASCII)"

    width, height = map(int, lines[1].split())
    maxval = int(lines[2])

    pixels = []
    for line in lines[3:]:
        pixels.extend(map(int, line.split()))

    image = np.array(pixels, dtype=np.uint8).reshape((height, width))
    return image