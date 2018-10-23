from collections import namedtuple

block = namedtuple('type', ['name', 'color'])

WIDTH = 900
HEIGHT = 600

GRID_SIZE = 10

WIDTH_ = WIDTH // GRID_SIZE
HEIGHT_ = HEIGHT // GRID_SIZE

BULLET_VELOCITY = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (211, 211, 211)

BLOCKS = [block('air', WHITE), block('box', BLACK),
          block('good spawn', GREEN), block('bad spawn', RED), block('plant zone', BLUE), block('smoke', GREY)]