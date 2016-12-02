EMPTY = 0
BOTTOM_PLAYER = 1
LEFT_PLAYER = 2
TOP_PLAYER = 3
RIGHT_PLAYER = 4


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

    def is_correct_step(self, player, start_cell, final_cell):
        start_x, start_y = start_cell
        final_x, final_y = final_cell
        if not self.is_inside(final_cell):
            return False
        if self.cells[final_y][final_x]:
            return False
        if player == BOTTOM_PLAYER:
            if start_y - final_y != 1:
                return False
            return abs(start_x - final_x) == 1
        if player == LEFT_PLAYER:
            if final_x - start_x != 1:
                return False
            return abs(start_y - final_y) == 1
        if player == TOP_PLAYER:
            if final_y - start_y != 1:
                return False
            return abs(start_x - final_x) == 1
        if player == RIGHT_PLAYER:
            if start_x - final_x != 1:
                return False
            return abs(start_y - final_y) == 1
        raise ValueError

    def get_selected_cells(self, x_coord, y_coord):
        cells = self.cells
        current_player = cells[y_coord][x_coord]
        selected_cells = []
        first_way = (x_coord + 1, y_coord + 1)
        second_way = (x_coord + 1, y_coord - 1)
        third_way = (x_coord - 1, y_coord + 1)
        fourth_way = (x_coord - 1, y_coord - 1)
        ways = [first_way, second_way, third_way, fourth_way]
        for way in ways:
            is_corrected = self.is_correct_step(current_player, (x_coord, y_coord), way)
            if is_corrected:
                selected_cells.append(way)
        return selected_cells
