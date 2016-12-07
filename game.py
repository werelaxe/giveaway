from collections import defaultdict
from random import randint
from logic import Field, LEFT_PLAYER, RIGHT_PLAYER, BOTTOM_PLAYER, TOP_PLAYER,\
    EMPTY, is_final_line, get_name_by_id
from ai import count_stat, get_benefit


class Game:
    def __init__(self, size):
        self.field = Field(size)
        self.current_player = randint(1, 4)
        self.selected_cells = []
        self.active_cell = None
        self.over = False

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
            # print("cells was successfully selected")
        else:
            self.active_cell = None

    def change_player(self):
        self.current_player += 1
        if self.current_player == 5:
            self.current_player = 1

    def do_step(self, step_cell):
        if step_cell in self.selected_cells:
            # print("step was successfully done")
            self.field[step_cell] = self.field[self.active_cell]
            if is_final_line(abs(self.current_player), step_cell, self.field):
                self.field[step_cell] = -abs(self.field[step_cell])
            self.field[self.active_cell] = EMPTY
            if type(self.selected_cells) == dict:
                cut_player = abs(self.field[self.selected_cells[step_cell]])
                self.field.cells_count[cut_player] -= 1
                if not self.field.cells_count[cut_player]:
                    pass
                    # print("{} wins!".format(get_name_by_id(cut_player)))
                    self.over = True
                self.field[self.selected_cells[step_cell]] = EMPTY
                if not self.field.get_cut_cells(
                        self.field[step_cell], step_cell):
                    self.change_player()
            else:
                self.change_player()
            self.selected_cells = []
            self.active_cell = None

    def click(self, step_cell):
        if abs(self.field[step_cell]) == abs(self.current_player):
            self.select_cell(step_cell)
        elif not self.field[step_cell]:
            self.do_step(step_cell)
