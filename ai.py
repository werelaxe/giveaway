from collections import defaultdict

from logic import LEFT_PLAYER, RIGHT_PLAYER, BOTTOM_PLAYER, TOP_PLAYER, Field


def count_stat(field):
    size = field.size
    stat = {}
    for index in range(size ** 2):
        curr_cell = (index % size, index // size)
        if field[curr_cell]:
            for cell in field.get_selected_cells(field[curr_cell], curr_cell):
                if cell not in stat:
                    stat[cell] = defaultdict(int)
                stat[cell][field[curr_cell]] += 1
    bottom_sum = 0
    top_sum = 0
    left_sum = 0
    right_sum = 0
    for key in stat.values():
        bottom_sum += key[BOTTOM_PLAYER]
        bottom_sum += key[-BOTTOM_PLAYER]
        top_sum += key[TOP_PLAYER]
        top_sum += key[-TOP_PLAYER]
        left_sum += key[LEFT_PLAYER]
        left_sum += key[-LEFT_PLAYER]
        right_sum += key[RIGHT_PLAYER]
        right_sum += key[-RIGHT_PLAYER]
    return bottom_sum, left_sum, top_sum, right_sum


def get_first_possible_step(player, field):
    size = field.size
    for index in range(size ** 2):
        curr_cell = (index % size, index // size)
        if abs(field[curr_cell]) == abs(player):
            steps = field.get_selected_cells(field[curr_cell], curr_cell)
            if steps:
                return curr_cell, steps[0]
            cuts = field.get_cut_cells(field[curr_cell], curr_cell)
            if cuts:
                return curr_cell, cuts[0]

field = Field(14)

print(get_first_possible_step(BOTTOM_PLAYER, field))
