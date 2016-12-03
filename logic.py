from itertools import product


EMPTY = 0
BOTTOM_PLAYER = 1
LEFT_PLAYER = 2
TOP_PLAYER = 3
RIGHT_PLAYER = 4

RIGHT_DIRS = [[]] * 5
RIGHT_DIRS[BOTTOM_PLAYER] = [(1, -1), (-1, -1)]
RIGHT_DIRS[LEFT_PLAYER] = [(1, 1), (1, -1)]
RIGHT_DIRS[TOP_PLAYER] = [(1, 1), (-1, 1)]
RIGHT_DIRS[RIGHT_PLAYER] = [(-1, 1), (-1, -1)]
ANY_DIRS = list(product([-1, 1], repeat=2))


def check_direction(player, direction):
    return direction in RIGHT_DIRS[player]


def cell_sum(first_cell, second_cell):
    return tuple(map(sum, zip(first_cell, second_cell)))


def cell_mul(cell, number):
    return tuple(map(lambda x: x * number, cell))


def get_start_player(coord_x, coord_y, field_size):
    if (coord_x == 5) and (coord_y == 6):
        return -BOTTOM_PLAYER
    if (coord_x + coord_y) % 2:
        if 0 <= coord_x <= 2:  # left player
            if 3 <= coord_y <= field_size - 4:
                return LEFT_PLAYER
        if field_size - 3 <= coord_x <= field_size - 1:  # right player
            if 3 <= coord_y <= field_size - 4:
                return RIGHT_PLAYER
        if 0 <= coord_y <= 2:  # top player
            if 3 <= coord_x <= field_size - 4:
                return TOP_PLAYER
        if field_size - 3 <= coord_y <= field_size - 1:  # bottom player
            if 3 <= coord_x <= field_size - 4:
                return BOTTOM_PLAYER
    return EMPTY


class Field:
    def __init__(self, size):
        self.cells = []
        self.size = size
        for indy in range(size):
            self.cells.append([])
            for indx in range(size):
                self.cells[indy].append(get_start_player(indx, indy, size))

    def __getitem__(self, cell):
        x_coord, y_coord = cell
        return self.cells[y_coord][x_coord]

    def __setitem__(self, cell, value):
        x_coord, y_coord = cell
        self.cells[y_coord][x_coord] = value

    def print_field(self):
        for line in self.cells:
            for c in line:
                print(str(c) + ' ', end='')
            print()

    def is_inside(self, cell):
        field_size = self.size
        x_coord, y_coord = cell
        if not (0 <= x_coord < field_size):
            return False
        if not (0 <= y_coord < field_size):
            return False
        if (0 <= x_coord <= 3) and (0 <= y_coord <= 3):
            return False
        if (0 <= x_coord <= 2) and (field_size - 3 <= y_coord <= field_size - 1):
            return False
        if (0 <= y_coord <= 2) and (field_size - 3 <= x_coord <= field_size - 1):
            return False
        if (field_size - 3 <= y_coord <= field_size - 1) and \
                (field_size - 3 <= x_coord <= field_size - 1):
            return False
        return True

    def check_cut_exists(self, player):
        size = self.size
        for index in range(size ** 2):
            curr_cell = (index % size, index // size)
            if abs(self[curr_cell]) == abs(player):
                if self.get_cut_cells(self[curr_cell], curr_cell):
                    return True
        return False

    def get_selected_cells(self, player, start_cell):
        if self.check_cut_exists(player):
            return []
        if abs(self[start_cell]) != abs(player):
            return []
        selected_cells = []
        if player > 0:
            for right_dir in RIGHT_DIRS[player]:
                if self[cell_sum(start_cell, right_dir)] == EMPTY:
                    selected_cells.append(cell_sum(start_cell, right_dir))
        else:  # it's a king (pain)
            for direction in ANY_DIRS:
                for index in range(1, self.size):
                    if self.is_inside(cell_sum(start_cell, cell_mul(direction, index))) and \
                            not self[cell_sum(start_cell, cell_mul(direction, index))]:
                        selected_cells.append((cell_sum(start_cell, cell_mul(direction, index))))
                    else:
                        break

        return selected_cells

    def get_cut_cells(self, player, start_cell):
        if abs(self[start_cell]) != abs(player):
            return {}
        cut_cells = {}
        if player > 0:
            for right_dir in ANY_DIRS:
                if not self.is_inside(cell_sum(start_cell, cell_mul(right_dir, 2))):
                    continue
                if self[cell_sum(start_cell, cell_mul(right_dir, 2))] == EMPTY and \
                                abs(self[cell_sum(start_cell, right_dir)]) != abs(player) and \
                        self[cell_sum(start_cell, right_dir)]:
                    cut_cells[cell_sum(start_cell, cell_mul(right_dir, 2))] = \
                        cell_sum(start_cell, right_dir)
        if player < 0:
            for direction in ANY_DIRS:
                enemy_met = False
                enemy = None
                for index in range(1, self.size):
                    curr_cell = cell_sum(start_cell, cell_mul(direction, index))
                    if not self.is_inside(curr_cell):
                        break
                    if abs(self[curr_cell]) == abs(player):
                        break
                    if self[curr_cell]:
                        if not enemy_met:
                            enemy_met = True
                            enemy = curr_cell
                        else:
                            break
                    else:
                        if enemy_met:
                            cut_cells[curr_cell] = enemy
        return cut_cells
