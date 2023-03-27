import pygame
import numpy as np
from vectorMath import PVector
from noise import pnoise2, pnoise3
from boid import Boid
from random import randint, uniform


scl = 20
shape = (800, 800)
rows, cols = (shape[0] // scl) + 1, (shape[1] // scl) + 1
screen = pygame.display.set_mode(shape)

grey = pygame.color.Color("grey22")
white = pygame.color.Color("white")
green = pygame.color.Color("green")

flowfield = [[0] * cols for _ in range(rows)]

run = True

vehicles = []
vehicleCount = 100

for _ in range(vehicleCount):
    vehicles.append(
        Boid(
            px=randint(0, shape[0]),
            py=randint(0, shape[1]),
            vx=uniform(0.5, 4),
            vy=uniform(0.5, 4),
            maxS=4,
            maxF=1,
        )
    )

zoff = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(grey)

    xoff = 0
    for i in range(rows):
        yoff = 0
        for j in range(cols):
            ngl = np.interp(pnoise3(xoff, yoff, zoff), [-1, 1], [-np.pi, np.pi])
            vec = PVector.fromAngle(ngl)
            vec.setMag(1)
            flowfield[i][j] = vec
            start = (j * scl, i * scl)
            end = ((j + vec.x) * scl, (i + vec.y) * scl)
            # pygame.draw.line(screen, white, start, end, width=1)
            zoff += 0.00001
            yoff += 0.05
        xoff += 0.05

    for v in vehicles:
        j = int(v.pos.x // scl)
        i = int(v.pos.y // scl)
        force = flowfield[i][j]
        force.setMag(1)
        v.applyForce(force)
        v.update()
        v.show(screen)

    pygame.display.update()

pygame.quit()
