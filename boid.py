from vectorMath import PVector
import pygame
from numba import njit
import numpy as np
import math


green = pygame.color.Color("green")


class Boid(object):
    def __init__(
        self, px=0, py=0, vx=0, vy=0, ax=0, ay=0, minS=0.5, maxS=1, maxF=1, perRad=50
    ) -> None:
        self.pos = PVector(px, py)
        self.vel = PVector(vx, vy)
        self.acc = PVector(ax, ay)
        self.maxSpeed = maxS
        self.minSpeed = minS
        self.maxForce = maxF
        self.perceptionRad = perRad

    def update(self, edgeShape=None):
        self.vel.add(self.acc)
        if self.vel.mag() < self.minSpeed:
            self.vel.setMag(self.minSpeed)
        else:
            self.vel.limit(self.maxSpeed)
        self.pos.add(self.vel)
        self.acc.mult(0)

    def applyForce(self, force):
        self.acc += force
        self.acc.limit(self.maxForce)

    def show(self, screen):
        if self.pos.x > screen.get_width():
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screen.get_width()
        if self.pos.y > screen.get_height():
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = screen.get_height()

        if self.vel.mag() == 0:
            pygame.draw.circle(screen, green, self.pos.retF2(), 2, width=0)
        else:
            end = PVector(self.vel.x, self.vel.y)
            right = PVector(end.y, -end.x)
            left = PVector(-end.y, end.x)
            end.setMag(10)
            right.setMag(3)
            left.setMag(3)
            end += self.pos
            right += self.pos
            left += self.pos
            pygame.draw.polygon(
                screen, green, (end.retF2(), right.retF2(), left.retF2()), width=0
            )

    def distanceToTarget(self, targetPos):
        return (targetPos - self.pos).mag()

    def seek(self, targetPos):
        desiredVel = targetPos - self.pos
        steeringForce = desiredVel - self.vel
        steeringForce.limit(self.maxForce)
        self.applyForce(steeringForce)

    def arrive(self, targetPos, brakingRadius):
        desiredVel = targetPos - self.pos
        dist = self.distanceToTarget(targetPos)
        if dist < brakingRadius:
            desiredMag = np.interp(dist, [0, brakingRadius], [0, self.maxSpeed])
            desiredVel.setMag(desiredMag)
        else:
            desiredVel.setMag(self.maxSpeed)
        steeringForce = desiredVel - self.vel
        steeringForce.limit(self.maxForce)
        self.applyForce(steeringForce)

    def flock(self, boids):
        alignF = self.align(boids)
        self.applyForce(alignF)
        cohessionF = self.cohesion(boids)
        self.applyForce(cohessionF)

    def align(self, boids):
        desiredVel = PVector()
        steeringForce = PVector()
        count = 0
        for boid in boids:
            if boid != self and self.distanceToTarget(boid.pos) < self.perceptionRad:
                desiredVel.add(boid.vel)
                count += 1
        if count > 0:
            desiredVel.div(count)
            steeringForce = desiredVel - self.vel
        return steeringForce

    def cohesion(self, boids):
        desiredPos = PVector()
        steeringForce = PVector()
        count = 0
        for boid in boids:
            if boid != self and self.distanceToTarget(boid.pos) < self.perceptionRad:
                desiredPos.add(boid.pos)
                count += 1
        if count > 0:
            desiredVel = desiredPos / count
            steeringForce = desiredVel - self.pos
        return steeringForce

    @staticmethod
    def distFromBoid(selfPos, targetPos):
        magSq = 0
        for i in range(3):
            magSq += (selfPos[i] - targetPos[i]) ** 2
        return math.sqrt(magSq)

    @njit
    def flockBetter(selfBoidPos, selfBoidVel, boidsPosArr, boidsVelArr, perceptionRad):
        print("Entry")

        def distFromBoid(selfPos, targetPos):
            magSq = 0
            for i in range(3):
                magSq += (selfPos[i] - targetPos[i]) ** 2
            return math.sqrt(magSq)

        desiredVel = np.zeros((1, 3))
        steeringForce = np.zeros((1, 3))
        count = 0
        for i in range(boidsPosArr.shape[0]):
            if distFromBoid(selfBoidPos, boidsPosArr[i]) < perceptionRad:
                desiredVel = desiredVel + boidsVelArr[i]
                count += 1
        if count > 0:
            desiredVel = desiredVel / count
            steeringForce = desiredVel - selfBoidVel
        print(steeringForce)
        return steeringForce
