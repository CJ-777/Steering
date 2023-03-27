import pygame
import math
from numpy import interp
from vectorMath import PVector
import boid
import target
from noise import pnoise1


shape = (400, 400)
gray = pygame.color.Color("gray22")
white = pygame.color.Color("white")
black = pygame.color.Color("black")

screen = pygame.display.set_mode(shape)
clock = pygame.time.Clock()
fps = 60

v = boid.Boid(100, 100, maxF=1, maxS=4, perRad=1000)
t = target.Target(200, 300)


xoff, yoff = 0, 1000

running = True

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(gray)

    # x = interp(pnoise1(xoff), [-1, 1], [0, shape[0]])
    # y = interp(pnoise1(yoff), [-1, 1], [0, shape[1]])

    (x, y) = pygame.mouse.get_pos()

    xoff += 0.005
    yoff += 0.005

    t.setPos(x, y)

    v.arrive(t.pos, 100)
    # v.seek(t.pos)
    v.update()
    v.show(screen)
    t.show(screen)
    pygame.display.update()

pygame.quit()
