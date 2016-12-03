from logic import Field, LEFT_PLAYER, RIGHT_PLAYER, BOTTOM_PLAYER, TOP_PLAYER,\
    EMPTY


class Game:
    def __init__(self, size):
        self.field = Field(size)
        self.current_player = BOTTOM_PLAYER
        self.selected_cells = []
        self.active_cell = None

    def change_cell(self, cell):
        self.field[cell] += 1
        if self.field[cell] == 5:
            self.field[cell] = -4

    def click(self, x_coord, y_coord):
        print(self.field.cells[y_coord][x_coord])
        if self.field.cells[y_coord][x_coord]:
            selected_cells = self.field.get_selected_cells(self.current_player, (x_coord, y_coord))
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









