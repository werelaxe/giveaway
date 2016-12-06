from collections import defaultdict

from logic import LEFT_PLAYER, RIGHT_PLAYER, BOTTOM_PLAYER, TOP_PLAYER, Field
from game import Game


def count_stat(field):
    size = field.size
    stat = {}
    for index in range(size ** 2):
        curr_cell = (index % size, index // size)
        if field[curr_cell]:
            for cell in field.get_selected_cells_without_cut_factor(field[curr_cell], curr_cell):
                if cell not in stat:
                    stat[cell] = defaultdict(int)
                stat[cell][field[curr_cell]] += 1
            for cell in field.get_cut_cells(field[curr_cell], curr_cell):
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


def do_first_possible_step(game:Game):
    player = game.current_player
    field = game.field
    size = field.size
    for index in range(size ** 2):
        curr_cell = (index % size, index // size)
        if abs(field[curr_cell]) == abs(player):
            game.click(curr_cell)
            if game.selected_cells:
                if type(game.selected_cells) == dict:
                    game.do_step(list(game.selected_cells.keys())[0])
                elif type(game.selected_cells) == list:
                    game.do_step(game.selected_cells[0])

game = Game(14)







