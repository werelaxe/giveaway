from collections import defaultdict
from copy import copy, deepcopy
import sys
from logic import LEFT_PLAYER, RIGHT_PLAYER, BOTTOM_PLAYER, TOP_PLAYER


def get_benefit(player, start_stat, finish_stat):
    benefit = 0
    for index in range(4):
        if index + 1 == player:
            benefit += start_stat[index] - finish_stat[index]
        else:
            benefit -= start_stat[index] - finish_stat[index]
    return benefit


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


def do_first_possible_step(game):
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
                    return
                elif type(game.selected_cells) == list:
                    game.do_step(game.selected_cells[0])
                    return


def get_cut_benefit(game, step_chain):
    copy_game = deepcopy(game)
    current_player = deepcopy(copy_game.current_player)
    start_cells_count = deepcopy(copy_game.field.cells_count)
    for step in step_chain:
        # print("select cells")
        copy_game.click(step[0])
        # print("do step")
        copy_game.click(step[1])
    finish_cells_count = copy_game.field.cells_count
    return start_cells_count[current_player] - finish_cells_count[current_player]


def get_step_benefit(counting_game, start_cell, finish_step):
    game = deepcopy(counting_game)
    start_stat = count_stat(game.field)
    player = game.current_player
    game.click(start_cell)
    game.do_step(finish_step)
    finish_stat = count_stat(game.field)
    return get_benefit(abs(player), start_stat, finish_stat)


def get_possible_steps(copy_game):
    game = deepcopy(copy_game)
    current_player = game.current_player
    size = game.field.size
    field = game.field
    possible_steps = []
    cells = []
    for index in range(size ** 2):
        curr_cell = (index % size, index // size)
        if abs(field[curr_cell]) == abs(current_player):
            cells.append(curr_cell)
    for cell in cells:
        game.click(cell)
        if game.selected_cells:
            possible_cells = game.selected_cells
            for possible_cell in possible_cells:
                possible_steps.append((cell, possible_cell))
    return possible_steps


def get_steps_chain(game, steps, deep, max_deep):
    if deep == max_deep:
        return 'end'
    result = []
    for step in steps:
        copy_game = deepcopy(game)
        copy_game.click(step[0])
        copy_game.click(step[1])
        result.append((step, get_steps_chain(copy_game, get_possible_steps(copy_game), deep + 1, max_deep)))
    return result


def get_states(chain, deep, global_dict, state, states_list):
    for element in chain:
        # print("    " * deep + str(element[0]))
        global_dict[element[0]] = {}
        if element[1] != 'end':
            # print("    " * deep)
            get_states(element[1], deep + 1, global_dict[element[0]], state + [element[0]], states_list)
        else:
            if state not in states_list:
                states_list.append(state)


def do_smart_step(game):
    max_benefit = 10000000000000
    max_possible_step = (-1, -1)
    possible_steps = get_possible_steps(game)
    if not possible_steps:
        print("No way!")
        return
    for start_cell, finish_cell in possible_steps:
        current_benefit = -get_step_benefit(game, start_cell, finish_cell)
        if current_benefit < max_benefit:
            max_benefit = current_benefit
            max_possible_step = (start_cell, finish_cell)
    max_start_cell, max_finish_cell = max_possible_step
    game.click(max_start_cell)
    game.click(max_finish_cell)


def do_very_smart_step(game, deep=3):
    steps = get_steps_chain(game, get_possible_steps(game), 0, deep)
    states = []
    get_states(steps, 0, {}, [], states)
    benefit_dict = defaultdict(int)
    # print(states)
    for state in states:
        benefit = get_cut_benefit(game, state)
        if benefit == 1:
            max_step = state[0]
            game.click(max_step[0])
            game.click(max_step[1])
            return
        benefit_dict[state[0]] += benefit
    max_benefit = -9999999
    max_step = None

    for step in benefit_dict.keys():
        if max_benefit < benefit_dict[step]:
            max_benefit = benefit_dict[step]
            max_step = step

    if max_step is None:
        do_first_possible_step(game)
        for player, count in game.field.cells_count.items():
            if count == 0:
                # print("Player {} wins!".format(player))
                game.over = True
    if max_step is not None:
        game.click(max_step[0])
        game.click(max_step[1])
