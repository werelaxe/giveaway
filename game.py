from logic import Field, LEFT_PLAYER, RIGHT_PLAYER, BOTTOM_PLAYER, TOP_PLAYER,\
    EMPTY


class Game:
    def __init__(self, size):
        self.field = Field(size)
        self.current_player = BOTTOM_PLAYER
        self.selected_cells = []
        self.active_cell = None
    """
    def try_step(self, start_cell, final_cell):
        start_x, start_y = start_cell
        final_x, final_y = final_cell
        if is_correct_step(
                self.field.cells, self.current_player, start_cell, final_cell):
            self.field.cells[start_y][start_y] = EMPTY
            self.field.cells[final_y][final_x] = self.current_player
            return 0
        else:
            return 1
    """
    def click(self, x_coord, y_coord):

        if self.field.cells[y_coord][x_coord]:

            selected_cells = self.field.get_selected_cells(self.current_player, (x_coord, y_coord))
            print('expected: {}'.format(selected_cells))
            cut_cells = self.field.get_cut_cells(self.current_player, (x_coord, y_coord))
            if cut_cells:
                self.selected_cells = cut_cells
                print(cut_cells)
            else:
                self.selected_cells = selected_cells
            if selected_cells or cut_cells:
                self.active_cell = (x_coord, y_coord)
            else:
                self.active_cell = None
            print('game.selected cells: {}'.format(self.selected_cells))
        else:
            if (x_coord, y_coord) in self.selected_cells:
                self.field[x_coord, y_coord] = self.current_player
                self.field[self.active_cell] = EMPTY
                if type(self.selected_cells) == dict:
                    self.field[self.selected_cells[(x_coord, y_coord)]] = EMPTY
                self.selected_cells = []
                self.active_cell = None
                self.current_player += 1
                if self.current_player == 5:
                    self.current_player = 1


    def update(self):
        print('Updating field: {}'.format(self))

if __name__ == '__main__':
    game = Game(14)









