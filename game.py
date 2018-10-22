import pygame
from collections import namedtuple
from constants import *


def draw_rect(surf, color, x1, y1, x2, y2):
    r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.rect(surf, color, r)


def draw_ellipse(surf, color, x1, y1, x2, y2):
    r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.ellipse(surf, color, r)


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def in_radius(self, r, vec):
        return (self.x-vec.x)**2 + (self.y-vec.y)**2 <= r

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __abs__(self):
        return (self.x**2 + self.y**2)**(1/2)

    def __mul__(self, num):
        return Vector(self.x*num, self.y*num)


class Bullet:

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def update(self):
        self.pos += self.vel

    def is_hit(self, players):
        for _p in players:
            if _p.pos.in_radius(6, self.pos):
                return _p

    def draw(self, surf):
        pass


class Bomb:

    def __init__(self, pos):
        self.pos = pos
        self.timer = 100
        self.exp = False

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.exp = True

    def draw(self, surf):
        pass


class Trap:

    def __init__(self, pos):
        self.pos = pos

    def is_catch(self, players):
        for _p in players:
            if _p.pos.in_radius(2, self.pos):
                return _p

    def draw(self, surf):
        pass


class Player:

    def __init__(self, name):
        self.name = name
        self.pos = Vector(0, 0)
        self.vel = Vector(0, 0)
        self.hp = 5
        self.score = 0

    def update(self):
        self.pos += self.vel

    def acc(self, a):
        self.vel = a

    def draw(self, surface):
        pass # draw box with name


class BadGuy(Player):

    def __init__(self, name):
        Player.__init__(self, name)
        self.has_bomb = True

    def shoot(self, side):
        return Bullet(self.pos, side*BULLET_VELOCITY + self.vel)

    def plant(self):
        return Bomb(self.pos)


class GoodGuy(Player):

    def __init__(self, name):
        Player.__init__(self, name)
        self.has_trap = True

    def shoot(self, side):
        return Bullet(self.pos, side*BULLET_VELOCITY + self.vel)

    def trap(self):
        return Trap(self.pos)


class Game(object):

    def __init__(self):
        pass
