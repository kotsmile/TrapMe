import pygame
from pygame.locals import *
from constants import *
import pickle
import map_creator as ms




def draw_rect(surf, x1, y1, x2, y2, color_):
    r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.rect(surf, color_, r)


def draw_ellipse(surf, x1, y1, x2, y2, color_):
    r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.ellipse(surf, color_, r)


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


G = Vector(0, 1)


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

    def move(self, direct):
            self.vel.x = direct.x

    def update(self, w):

        if w[self.pos.x][self.pos.y+1] == 0:
            self.vel += G
        if w[(self.pos + self.vel).x][(self.pos + self.vel).y] != 0 or w[(self.pos + self.vel).x][(self.pos + self.vel).y] != 0:
            self.vel.x = 0
        if w[(self.pos + self.vel).x][(self.pos + self.vel).y] != 0 or w[(self.pos + self.vel).x][(self.pos + self.vel).y] != 0:
            self.vel.x = 0
        try:
            _points = [self.pos + Vector(0, self.vel.y//abs(self.vel.y))*i for i in range(1, int(abs(self.pos.y-self.vel.y))+1)]
            for _p in _points:
                if w[_p.x][_p.y] != 0:
                    self.pos = _p - Vector(0, self.vel.y)*(1//abs(self.vel.y))
                    self.vel.y = 0
                    break
        except ZeroDivisionError:
            pass

        self.pos += self.vel

    def jump(self, w):
        if w[self.pos.x][self.pos.y+1] != 0:
            self.vel = G*(-5)

    def draw(self, surface):
        draw_rect(surface,
                  ms.transform_from(self.pos.x, self.pos.y)[0][0],
                  ms.transform_from(self.pos.x, self.pos.y)[0][1],
                  ms.transform_from(self.pos.x, self.pos.y)[1][0],
                  ms.transform_from(self.pos.x, self.pos.y)[1][1], (255, 100, 0))


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

    def __init__(self, name):
        self.player = GoodGuy('hey')
        self.world = []
        with open('maps/' + name, 'rb') as _f:
            self.world = pickle.load(_f)
        spawn = 0
        for _i in range(WIDTH_):
            for _j in range(HEIGHT_):
                if self.world[_i][_j] == 2:
                    spawn = Vector(_i, _j-1)

        self.player.pos = spawn
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        self.sprites = [self.player]
        self.FPS = 100
        self.fpsClock = pygame.time.Clock()
        self.fpsClock.tick(self.FPS)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.surface.fill(WHITE)

    def draw(self):
        for _i in range(WIDTH_):
            for _j in range(HEIGHT_):
                draw_rect(self.surface,
                          ms.transform_from(_i, _j)[0][0],
                          ms.transform_from(_i, _j)[0][1],
                          ms.transform_from(_i, _j)[1][0],
                          ms.transform_from(_i, _j)[1][1], BLOCKS[self.world[_i][_j]].color)

        for _sprite in self.sprites:
            _sprite.draw(self.surface)

    def update(self):
        for _sprite in self.sprites:
            _sprite.update(self.world)

    def start(self):
        print('start')
        timer = 100000
        while self.running:
            timer -= 1

            if timer <= 0:
                timer = 100000
                if pygame.key.get_pressed()[K_a]:
                    self.player.move(Vector(-1, 0))
                elif pygame.key.get_pressed()[K_d]:
                    self.player.move(Vector(1, 0))
                else:
                    self.player.move(Vector(0, 0))
                if pygame.key.get_pressed()[K_UP]:
                    self.player.shoot(Vector(0, -1))
                elif pygame.key.get_pressed()[K_RIGHT]:
                    self.player.shoot(Vector(1, 0))
                elif pygame.key.get_pressed()[K_DOWN]:
                    self.player.shoot(Vector(0, 1))
                elif pygame.key.get_pressed()[K_LEFT]:
                    self.player.shoot(Vector(-1, 0))

                if pygame.key.get_pressed()[K_SPACE]:
                    self.player.jump(self.world)

                for event in pygame.event.get():

                    if event.type == QUIT:
                        return

                self.update()
                self.draw()
                self.screen.blit(self.surface, (0, 0))
                pygame.display.flip()