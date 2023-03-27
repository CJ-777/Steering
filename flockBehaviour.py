import pygame
import numpy as np
from vectorMath import PVector
from boid import Boid
from random import randint, uniform
from timeit import default_timer as timer


gray = pygame.color.Color("gray22")
white = pygame.color.Color("white")
black = pygame.color.Color("black")
green = pygame.color.Color("green")

shape = (800, 800)
screen = pygame.display.set_mode(shape)
clock = pygame.time.Clock()
fps = 60

running = True

boids = []
boidCount = 100
for _ in range(boidCount):
    boids.append(
        Boid(
            px=randint(0, shape[0]),
            py=randint(0, shape[1]),
            vx=uniform(-4, 4),
            vy=uniform(-4, 4),
            maxF=0.5,
            minS=4,
            maxS=4,
            perRad=100,
        )
    )
boidPosArr = np.empty((boidCount, 9))
boidVelArr = np.empty((boidCount, 9))
boidAccArr = np.empty((boidCount, 9))

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(gray)

    start = timer()
    for i, boid in enumerate(boids):
        boidPosArr[i][0] = boid.pos.x
        boidPosArr[i][1] = boid.pos.y
        boidPosArr[i][2] = boid.pos.z
        boidVelArr[i][0] = boid.vel.x
        boidVelArr[i][1] = boid.vel.y
        boidVelArr[i][2] = boid.vel.z
        boidAccArr[i][0] = boid.acc.x
        boidAccArr[i][1] = boid.acc.y
        boidAccArr[i][2] = boid.acc.z
    for boid in boids:
        selfBoidPos = np.asarray([boid.pos.x, boid.pos.y, boid.pos.z])
        selfBoidVel = np.asarray([boid.vel.x, boid.vel.y, boid.vel.z])
        steeringForce = Boid.flockBetter(
            selfBoidPos, selfBoidVel, boidPosArr, boidVelArr, boid.perceptionRad
        )
        boid.applyForce(PVector(steeringForce))
        # boid.flock(boids)
        boid.update()
        boid.show(screen)

    end = timer()
    print(end - start)
    exit()

    pygame.display.update()

pygame.quit()

# initial = 0.10277350002434105 - 0.0747304999968037
