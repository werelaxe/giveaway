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

    def click(self, step_cell):
        if self.field[step_cell]:
            selected_cells = self.field.get_selected_cells(self.current_player, step_cell)
            cut_cells = self.field.get_cut_cells(self.current_player, step_cell)
            if cut_cells:
                self.selected_cells = cut_cells
            else:
                self.selected_cells = selected_cells
            if selected_cells or cut_cells:
                self.active_cell = step_cell
            else:
                self.active_cell = None
        else:
            if step_cell in self.selected_cells:
                self.field[step_cell] = self.current_player
                self.field[self.active_cell] = EMPTY
                if type(self.selected_cells) == dict:
                    self.field[self.selected_cells[step_cell]] = EMPTY
                self.selected_cells = []
                self.active_cell = None
                self.current_player += 1
                if self.current_player == 5:
                    self.current_player = 1

    def update(self):
        print('Updating field: {}'.format(self))

if __name__ == '__main__':
    game = Game(14)









