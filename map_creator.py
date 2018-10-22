import pygame
from pygame.locals import *
import game
from constants import *
import pickle

pygame.init()


def transform_to(x, y):
    return [x // GRID_SIZE, y // GRID_SIZE]


def transform_from(x, y):
    return [[x * GRID_SIZE, y * GRID_SIZE],[(x+1) * GRID_SIZE, (y+1) * GRID_SIZE]]


def draw_rect(surf, x1, y1, x2, y2, c):
    _r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.rect(surf, c, _r)


def draw_ellipse(surf, x1, y1, x2, y2, c):
    _r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.ellipse(surf, c, _r)


def draw(surf, world_):
    for _i in range(WIDTH_):
        for _j in range(HEIGHT_):
            if world_[_i][_j] == 0:
                draw_rect(surf, transform_from(_i, _j)[0][0], transform_from(_i, _j)[0][1],
                          transform_from(_i, _j)[1][0], transform_from(_i, _j)[1][1], WHITE)
            elif world_[_i][_j] == 1:
                draw_rect(surf, transform_from(_i, _j)[0][0], transform_from(_i, _j)[0][1],
                          transform_from(_i, _j)[1][0], transform_from(_i, _j)[1][1], BLACK)
            elif world_[_i][_j] == 2:
                draw_rect(surf, transform_from(_i, _j)[0][0], transform_from(_i, _j)[0][1],
                          transform_from(_i, _j)[1][0], transform_from(_i, _j)[1][1], GREEN)
            elif world_[_i][_j] == 3:
                draw_rect(surf, transform_from(_i, _j)[0][0], transform_from(_i, _j)[0][1],
                          transform_from(_i, _j)[1][0], transform_from(_i, _j)[1][1], RED)
            elif world_[_i][_j] == 4:
                draw_rect(surf, transform_from(_i, _j)[0][0], transform_from(_i, _j)[0][1],
                          transform_from(_i, _j)[1][0], transform_from(_i, _j)[1][1], BLUE)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill(WHITE)

    world = [[0 for _ in range(HEIGHT_)] for _ in range(WIDTH_)]

    while True:
        if pygame.key.get_pressed()[K_s]:
            _file_name = 'maps/' + input('(Write file name): ')

            with open(_file_name, 'wb') as _f:
                pickle.dump(world, _f)

        if pygame.key.get_pressed()[K_l]:
            _file_name = 'maps/' + input('(Write file name): ')
            try:
                with open(_file_name, 'rb') as _f:
                    world = pickle.load(_f)
            except FileNotFoundError:
                print('This file does not exist!')

        for event in pygame.event.get():

            if event.type == QUIT:
                return

        if pygame.mouse.get_pressed()[0]:
            _x, _y = transform_to(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            world[_x][_y] = 1
        if pygame.key.get_pressed()[K_d]:
            _x, _y = transform_to(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            world[_x][_y] = 0
        if pygame.key.get_pressed()[K_b]:
            _x, _y = transform_to(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            world[_x][_y] = 3
        if pygame.key.get_pressed()[K_g]:
            _x, _y = transform_to(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            world[_x][_y] = 2
        if pygame.key.get_pressed()[K_p]:
            _x, _y = transform_to(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            world[_x][_y] = 4

        draw(surface, world)
        screen.blit(surface, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
