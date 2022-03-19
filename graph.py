from math import ceil
import pygame as pg
from collections import deque

standard_size = 20


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Less operator

    def __lt__(self, second):
        return ((self.x, self.y) < (second.x, second.y))

    @staticmethod
    def distance(first, second):
        dx, dy = abs(first.x - second.x), abs(first.y - second.y)
        return (dx ** 2 + dy ** 2) ** 0.5

    def draw(self, surface, grid, color):
        surface.fill(color, grid[self.y][self.x])

    # Draw line between two cells
    @staticmethod
    def draw_line(first, second, surface, grid, color, mark=None):
        dx, dy = first.x - second.x, first.y - second.y
        dx_abs, dy_abs = abs(dx), abs(dy)
        px, py = 2 * dy_abs - dx_abs, 2 * dx_abs - dy_abs

        # X-axis
        if dx_abs > dy_abs:
            if dx < 0:
                xs, xe, y = first.x, second.x, first.y
            else:
                xs, xe, y = second.x, first.x, second.y

            while xs <= xe:
                surface.fill(color, grid[y][xs])
                if mark is not None:
                    mark[y][xs] = True

                xs += 1
                if px < 0:
                    px += 2 * dy_abs
                else:
                    y += (1 if dx * dy > 0 else -1)
                    px += 2 * (dy_abs - dx_abs)

        # Y-axis
        else:
            if dy < 0:
                ys, ye, x = first.y, second.y, first.x
            else:
                ys, ye, x = second.y, first.y, second.x

            while ys <= ye:
                surface.fill(color, grid[ys][x])

                if mark is not None:
                    mark[ys][x] = True

                ys += 1
                if py < 0:
                    py += 2 * dx_abs
                else:
                    x += (1 if dx * dy > 0 else -1)
                    py += 2 * (dx_abs - dy_abs)

    @staticmethod
    def initialize(line, delimeter=','):
        parsed = []
        try:
            # Split line to integer (coordinates) arrays seperated by delimiter
            list_coors = list(map(int, line.split(delimeter)))
            len_coors = int(ceil(len(list_coors) / 2))

            # Group pair coordinates as a cell (x, y)
            for i in range(len_coors):
                x, y = list_coors[i * 2], list_coors[i * 2 + 1]
                parsed.append(Cell(x=x, y=y))

        except:
            raise Exception('Fail to initial cell from line \'{}\''.format(line))
            return

        return parsed


class Border:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.rect = pg.Rect((0, 0, self.w * standard_size, self.h * standard_size))

    def create_grid(self):
        grid = [[pg.Rect((0, 0, standard_size, standard_size)) for j in range(self.w)] for i in range(self.h)]
        return grid

    # Draw grid of cells within border
    def draw(self, surface, grid, color):
        self.rect.center = surface.get_rect().center
        self.rect.x = surface.get_rect().w * 0.32
        self.rect.y = surface.get_rect().h * 0.18
        pg.draw.rect(surface, color, self.rect, 30)

        # Draw cells
        for i in range(self.h):
            for j in range(self.w):
                grid[i][j].x = self.rect.x + standard_size * j
                grid[i][j].y = self.rect.y + standard_size * i
                surface.fill(pg.Color('white'), grid[i][j])
                pg.draw.rect(surface, color, grid[i][j], 1)

    # Get size of border
    def get_size(self):
        return (0, 0, self.w, self.h)

    @staticmethod
    def initialize(line, delimeter=','):
        try:
            w, h = map(int, line.split(delimeter))
            parsed = Border(w=w, h=h)
        except:
            raise Exception('Fail to init border from line \'{}\''.format(line))
            return

        return parsed


# Create a moving cycle within d units
def moving_steps(d, steps):
    for i in range(d + 1):
        steps.append(i)
    for i in range(d, -d, -1):
        steps.append(i)
    for i in range(-d, 0):
        steps.append(i)
    return steps


class Obstacle:
    def __init__(self, list_cells):
        self.list_cells = list_cells

    """
    Draw line between every pairs of obstacle coordinates
    """

    def draw(self, surface, grid, mark, color, movable=False):
        len_cells = len(self.list_cells)

        if movable:
            for i in range(len_cells):
                self.list_cells[i].move()

        for i in range(len_cells + 1):
            u, v = i % len_cells, (i + 1) % len_cells
            CellObstacle.draw_line(first=self.list_cells[u], second=self.list_cells[v], surface=surface, grid=grid,
                                   mark=mark, color=color)

    @staticmethod
    def initialize(line, delimeter=',', dx=0, dy=0):
        try:
            list_cells = CellObstacle.initialize(line=line, delimeter=delimeter, dx=dx, dy=dy)
            parsed = Obstacle(list_cells=list_cells)
        except:
            raise Exception('MAP: Fail to init obstacle from line \'{}\''.format(line))
            return

        return parsed


class CellObstacle(Cell):
    def __init__(self, x, y, dx=0, dy=0):
        Cell.__init__(self, x, y)
        self.origin_x = x
        self.origin_y = y
        self.next_x = deque()
        self.next_y = deque()

        moving_steps(dx, self.next_x)
        moving_steps(dy, self.next_y)

    # Move to next state
    def move(self):
        dx, dy = self.next_x.popleft(), self.next_y.popleft()
        self.x = self.origin_x + dx
        self.y = self.origin_y + dy
        self.next_x.append(dx)
        self.next_y.append(dy)

    """
    Parse a group of obstacles' cells from line
    """

    @staticmethod
    def initialize(line, dx=0, dy=0, delimeter=','):
        parsed = []

        try:
            list_coors = list(map(int, line.split(delimeter)))
            len_coors = int(ceil(len(list_coors) / 2))
            for i in range(len_coors):
                x, y = list_coors[i * 2], list_coors[i * 2 + 1]
                parsed.append(CellObstacle(x=x, y=y, dx=dx, dy=dy))

        except:
            raise Exception('MAP: Fail to init obstacle cell from line \'{}\''.format(line))
            return
        return parsed


class Map:
    def __init__(self):
        self.border = None
        self.S = self.G = None
        self.obstacles = []

    """
    Draw map's components
    """

    def draw(self, surface, grid, movable=False):
        w, h = self.border.w, self.border.h
        obstacle = [[False] * w for _ in range(h)]

        self.border.draw(surface=surface, grid=grid, color=pg.Color('lightyellow4'))
        self.S.draw(surface=surface, grid=grid, color=pg.Color('steelblue'))
        self.G.draw(surface=surface, grid=grid, color=pg.Color('tomato'))
        for e in self.obstacles:
            e.draw(surface=surface, grid=grid, color=pg.Color('orange'), mark=obstacle, movable=movable)

        return obstacle

    """
    Create a complete path starting from end node
    """

    @staticmethod
    def trace_path_by_direction(s, g, direction):
        sx, sy = s.x, s.y
        gx, gy = g.x, g.y
        dx = [0, 0, 1, -1]
        dy = [1, -1, 0, 0]
        path = []

        while not (gx == sx and gy == sy):

            i = direction[gy][gx]
            gx, gy = gx - dx[i], gy - dy[i]

            # Encounter the start node
            if gx == sx and gy == sy:
                break

            path.append(Cell(x=gx, y=gy))

        # Reverse the path from start node to end node
        path.reverse()
        return path

    # Load a map from file
    def load(self, path):
        try:
            map_file = open(path, 'r')
        except:
            raise Exception('File path is not valid:\'{}\''.format(path))
            return

        try:
            self.border = Border.initialize(line=map_file.readline().rstrip('\n'))
            self.S, self.G, *self.stops = tuple(Cell.initialize(line=map_file.readline().rstrip('\n')))
            len_obstacles = int(map_file.readline().rstrip('\n'))
            dx = 0
            dy = 1 - dx

            for _ in range(len_obstacles):
                self.obstacles.append(Obstacle.initialize(line=map_file.readline().rstrip('\n'), dx=dx, dy=dy))
                dx = 1 - dx
                dy = 1 - dx

        except Exception as e:
            raise Exception('{}'.format(e))

        map_file.close()
        grid = self.border.create_grid()

        print('Load map successfully with file path:\'{}\''.format(path))
        return self.border.get_size(), grid


from math import ceil
import pygame as pg
from collections import deque

standard_size = 20


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Less operator

    def __lt__(self, second):
        return ((self.x, self.y) < (second.x, second.y))

    @staticmethod
    def distance(first, second):
        dx, dy = abs(first.x - second.x), abs(first.y - second.y)
        return (dx ** 2 + dy ** 2) ** 0.5

    def draw(self, surface, grid, color):
        surface.fill(color, grid[self.y][self.x])

    # Draw line between two cells
    @staticmethod
    def draw_line(first, second, surface, grid, color, mark=None):
        dx, dy = first.x - second.x, first.y - second.y
        dx_abs, dy_abs = abs(dx), abs(dy)
        px, py = 2 * dy_abs - dx_abs, 2 * dx_abs - dy_abs

        # X-axis
        if dx_abs > dy_abs:
            if dx < 0:
                xs, xe, y = first.x, second.x, first.y
            else:
                xs, xe, y = second.x, first.x, second.y

            while xs <= xe:
                surface.fill(color, grid[y][xs])
                if mark is not None:
                    mark[y][xs] = True

                xs += 1
                if px < 0:
                    px += 2 * dy_abs
                else:
                    y += (1 if dx * dy > 0 else -1)
                    px += 2 * (dy_abs - dx_abs)

        # Y-axis
        else:
            if dy < 0:
                ys, ye, x = first.y, second.y, first.x
            else:
                ys, ye, x = second.y, first.y, second.x

            while ys <= ye:
                surface.fill(color, grid[ys][x])

                if mark is not None:
                    mark[ys][x] = True

                ys += 1
                if py < 0:
                    py += 2 * dx_abs
                else:
                    x += (1 if dx * dy > 0 else -1)
                    py += 2 * (dx_abs - dy_abs)

    @staticmethod
    def initialize(line, delimeter=','):
        parsed = []
        try:
            # Split line to integer (coordinates) arrays seperated by delimiter
            list_coors = list(map(int, line.split(delimeter)))
            len_coors = int(ceil(len(list_coors) / 2))

            # Group pair coordinates as a cell (x, y)
            for i in range(len_coors):
                x, y = list_coors[i * 2], list_coors[i * 2 + 1]
                parsed.append(Cell(x=x, y=y))

        except:
            raise Exception('Fail to initial cell from line \'{}\''.format(line))
            return

        return parsed


class Border:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.rect = pg.Rect((0, 0, self.w * standard_size, self.h * standard_size))

    def create_grid(self):
        grid = [[pg.Rect((0, 0, standard_size, standard_size)) for j in range(self.w)] for i in range(self.h)]
        return grid

    # Draw grid of cells within border
    def draw(self, surface, grid, color):
        self.rect.center = surface.get_rect().center
        self.rect.x = surface.get_rect().w * 0.32
        self.rect.y = surface.get_rect().h * 0.18
        pg.draw.rect(surface, color, self.rect, 30)

        # Draw cells
        for i in range(self.h):
            for j in range(self.w):
                grid[i][j].x = self.rect.x + standard_size * j
                grid[i][j].y = self.rect.y + standard_size * i
                surface.fill(pg.Color('white'), grid[i][j])
                pg.draw.rect(surface, color, grid[i][j], 1)

    # Get size of border
    def get_size(self):
        return (0, 0, self.w, self.h)

    @staticmethod
    def initialize(line, delimeter=','):
        try:
            w, h = map(int, line.split(delimeter))
            parsed = Border(w=w, h=h)
        except:
            raise Exception('Fail to init border from line \'{}\''.format(line))
            return

        return parsed


# Create a moving cycle within d units
def moving_steps(d, steps):
    for i in range(d + 1):
        steps.append(i)
    for i in range(d, -d, -1):
        steps.append(i)
    for i in range(-d, 0):
        steps.append(i)
    return steps


class Obstacle:
    def __init__(self, list_cells):
        self.list_cells = list_cells

    """
    Draw line between every pairs of obstacle coordinates
    """

    def draw(self, surface, grid, mark, color, movable=False):
        len_cells = len(self.list_cells)

        if movable:
            for i in range(len_cells):
                self.list_cells[i].move()

        for i in range(len_cells + 1):
            u, v = i % len_cells, (i + 1) % len_cells
            CellObstacle.draw_line(first=self.list_cells[u], second=self.list_cells[v], surface=surface, grid=grid,
                                   mark=mark, color=color)

    @staticmethod
    def initialize(line, delimeter=',', dx=0, dy=0):
        try:
            list_cells = CellObstacle.initialize(line=line, delimeter=delimeter, dx=dx, dy=dy)
            parsed = Obstacle(list_cells=list_cells)
        except:
            raise Exception('MAP: Fail to init obstacle from line \'{}\''.format(line))
            return

        return parsed


class CellObstacle(Cell):
    def __init__(self, x, y, dx=0, dy=0):
        Cell.__init__(self, x, y)
        self.origin_x = x
        self.origin_y = y
        self.next_x = deque()
        self.next_y = deque()

        moving_steps(dx, self.next_x)
        moving_steps(dy, self.next_y)

    # Move to next state
    def move(self):
        dx, dy = self.next_x.popleft(), self.next_y.popleft()
        self.x = self.origin_x + dx
        self.y = self.origin_y + dy
        self.next_x.append(dx)
        self.next_y.append(dy)

    """
    Parse a group of obstacles' cells from line
    """

    @staticmethod
    def initialize(line, dx=0, dy=0, delimeter=','):
        parsed = []

        try:
            list_coors = list(map(int, line.split(delimeter)))
            len_coors = int(ceil(len(list_coors) / 2))
            for i in range(len_coors):
                x, y = list_coors[i * 2], list_coors[i * 2 + 1]
                parsed.append(CellObstacle(x=x, y=y, dx=dx, dy=dy))

        except:
            raise Exception('MAP: Fail to init obstacle cell from line \'{}\''.format(line))
            return
        return parsed


class Map:
    def __init__(self):
        self.border = None
        self.S = self.G = None
        self.obstacles = []

    """
    Draw map's components
    """

    def draw(self, surface, grid, movable=False):
        w, h = self.border.w, self.border.h
        obstacle = [[False] * w for _ in range(h)]

        self.border.draw(surface=surface, grid=grid, color=pg.Color('lightyellow4'))
        self.S.draw(surface=surface, grid=grid, color=pg.Color('steelblue'))
        self.G.draw(surface=surface, grid=grid, color=pg.Color('tomato'))
        for e in self.obstacles:
            e.draw(surface=surface, grid=grid, color=pg.Color('orange'), mark=obstacle, movable=movable)

        return obstacle

    """
    Create a complete path starting from end node
    """

    @staticmethod
    def trace_path_by_direction(s, g, direction):
        sx, sy = s.x, s.y
        gx, gy = g.x, g.y
        dx = [0, 0, 1, -1]
        dy = [1, -1, 0, 0]
        path = []

        while not (gx == sx and gy == sy):

            i = direction[gy][gx]
            gx, gy = gx - dx[i], gy - dy[i]

            # Encounter the start node
            if gx == sx and gy == sy:
                break

            path.append(Cell(x=gx, y=gy))

        # Reverse the path from start node to end node
        path.reverse()
        return path

    # Load a map from file
    def load(self, path):
        try:
            map_file = open(path, 'r')
        except:
            raise Exception('File path is not valid:\'{}\''.format(path))
            return

        try:
            self.border = Border.initialize(line=map_file.readline().rstrip('\n'))
            self.S, self.G, *self.stops = tuple(Cell.initialize(line=map_file.readline().rstrip('\n')))
            len_obstacles = int(map_file.readline().rstrip('\n'))
            dx = 0
            dy = 1 - dx

            for _ in range(len_obstacles):
                self.obstacles.append(Obstacle.initialize(line=map_file.readline().rstrip('\n'), dx=dx, dy=dy))
                dx = 1 - dx
                dy = 1 - dx

        except Exception as e:
            raise Exception('{}'.format(e))

        map_file.close()
        grid = self.border.create_grid()

        print('Load map successfully with file path:\'{}\''.format(path))
        return self.border.get_size(), grid
