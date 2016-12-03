EMPTY = 0
BOTTOM_PLAYER = 1
LEFT_PLAYER = 2
TOP_PLAYER = 3
RIGHT_PLAYER = 4

RIGHT_DIRS = [0] * 5
RIGHT_DIRS[BOTTOM_PLAYER] = [(1, -1), (-1, -1)]
RIGHT_DIRS[LEFT_PLAYER] = [(1, 1), (1, -1)]
RIGHT_DIRS[TOP_PLAYER] = [(1, 1), (-1, 1)]
RIGHT_DIRS[RIGHT_PLAYER] = [(-1, 1), (-1, -1)]


def check_direction(player, direction):
    return direction in RIGHT_DIRS[player]


def get_start_player(coord_x, coord_y, field_size):
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
        self.cut_exists = False
        for indy in range(size):
            self.cells.append([])
            for indx in range(size):
                self.cells[indy].append(get_start_player(indx, indy, size))

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

    def get_selected_cells(self, player, start_cell):
        start_x, start_y = start_cell
        if self.cells[start_y][start_x] != player:
            return []
        selected_cells = []
        for right_dir in RIGHT_DIRS[player]:
            x_bias, y_bias = right_dir
            if player > 0:
                cut_way = self.cells[start_y + y_bias * 2][start_x + x_bias * 2]
                pass
        return selected_cells
