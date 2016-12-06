from logic import Field, LEFT_PLAYER, RIGHT_PLAYER, BOTTOM_PLAYER, TOP_PLAYER,\
    EMPTY, is_final_line


class Game:
    def __init__(self, size):
        self.field = Field(size)
        self.current_player = BOTTOM_PLAYER
        self.selected_cells = []
        self.active_cell = None
        self.cells_count = {LEFT_PLAYER: 0, RIGHT_PLAYER: 0, TOP_PLAYER: 0, BOTTOM_PLAYER: 0}

    def change_cell(self, cell):
        self.field[cell] += 1
        if self.field[cell] == 5:
            self.field[cell] = -4

    def select_cell(self, step_cell):
        selected_cells = self.field.get_selected_cells(self.field[step_cell], step_cell)
        cut_cells = self.field.get_cut_cells(self.field[step_cell], step_cell)
        if cut_cells:
            self.selected_cells = cut_cells
        else:
            self.selected_cells = selected_cells
        if selected_cells or cut_cells:
            self.active_cell = step_cell
        else:
            self.active_cell = None

    def change_player(self):
        self.current_player += 1
        if self.current_player == 5:
            self.current_player = 1

    def do_step(self, step_cell):
        if step_cell in self.selected_cells:
            self.field[step_cell] = self.field[self.active_cell]
            if is_final_line(abs(self.current_player), step_cell, self.field):
                self.field[step_cell] *= -1
            self.field[self.active_cell] = EMPTY
            if type(self.selected_cells) == dict:
                print('do cut')
                self.field[self.selected_cells[step_cell]] = EMPTY
                if not self.field.get_cut_cells(self.field[step_cell], step_cell):
                    self.change_player()
            else:
                print('do step')
                self.change_player()
            self.selected_cells = []
            self.active_cell = None

    def click(self, step_cell):
        if abs(self.field[step_cell]) == abs(self.current_player):
            self.select_cell(step_cell)
        elif not self.field[step_cell]:
            self.do_step(step_cell)

    def update(self):
        print('Updating field: {}'.format(self))

if __name__ == '__main__':
    game = Game(14)