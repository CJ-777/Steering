from vectorMath import PVector
import pygame


red = pygame.color.Color("red")


class Target:
    def __init__(self, px, py) -> None:
        self.pos = PVector(px, py)

    def setPos(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def show(self, screen):
        pygame.draw.circle(screen, red, self.pos.retF2(), 5, width=0)
