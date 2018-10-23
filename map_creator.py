import pygame
from pygame.locals import *
from constants import *
import pickle

pygame.init()


def transform_to(x, y):
    return [x // GRID_SIZE, y // GRID_SIZE]


def transform_from(x, y):
    return [[x * GRID_SIZE, y * GRID_SIZE], [(x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE]]


def draw_rect(surf, x1, y1, x2, y2, c):
    _r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.rect(surf, c, _r)


def draw_ellipse(surf, x1, y1, x2, y2, c):
    _r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.ellipse(surf, c, _r)


def draw(surf, world_):
    for _i in range(WIDTH_):
        for _j in range(HEIGHT_):
            draw_rect(surf, transform_from(_i, _j)[0][0], transform_from(_i, _j)[0][1],
                      transform_from(_i, _j)[1][0], transform_from(_i, _j)[1][1], BLOCKS[world_[_i][_j]].color)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill(WHITE)

    pick = 0
    perm_m = True
    perm_k = True

    world = [[0 for _ in range(HEIGHT_)] for _ in range(WIDTH_)]

    while True:
        if pygame.key.get_pressed()[K_s]:
            _file_name = 'maps/' + input('(Write file name to save): ')

            with open(_file_name, 'wb') as _f:
                pickle.dump(world, _f)

        if pygame.key.get_pressed()[K_l]:
            _file_name = 'maps/' + input('(Write file name to load): ')
            try:
                with open(_file_name, 'rb') as _f:
                    world = pickle.load(_f)
            except FileNotFoundError:
                print('This file does not exist!')

        for event in pygame.event.get():

            if event.type == QUIT:
                return

        if (pygame.mouse.get_pressed()[2] and perm_m) or (pygame.key.get_pressed()[K_n] and perm_k):
            pick += 1
            if pick >= len(BLOCKS):
                pick = 0

            print('> ' + BLOCKS[pick].name)

        perm_m = not pygame.mouse.get_pressed()[2]
        perm_k = not pygame.key.get_pressed()[K_n]

        if pygame.mouse.get_pressed()[0]:
            _x, _y = transform_to(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            world[_x][_y] = pick

        draw(surface, world)
        screen.blit(surface, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
