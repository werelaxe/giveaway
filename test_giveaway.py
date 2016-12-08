import unittest
from collections import defaultdict
import logic
from random import randint
import game
import ai


def create_rand_cell():
    x = randint(0, 20)
    y = randint(0, 20)
    return x, y


class Testing(unittest.TestCase):
    size = 10
    field = logic.Field(size)

    def test_creating_field(self):
        self.assertEquals(type(self.field.cells_count), dict)
        for val in self.field.cells_count.values():
            self.assertEquals(val, (self.size // 2 - 3) * 3)
        self.assertEquals(len(self.field.cells), self.size)

    def test_inside(self):
        cell = create_rand_cell()
        if self.field.is_inside(cell):
            player = self.field[cell]

    def test_cut(self):
        field = logic.Field(self.size)
        field[(3, 4)] = logic.RIGHT_PLAYER
        self.assertTrue(field.check_cut_exists(logic.LEFT_PLAYER))

    def test_getting_sel_cells(self):
        field = logic.Field(self.size)
        field[(3, 4)] = logic.RIGHT_PLAYER
        answer = field.get_selected_cells_without_cut_factor(
            logic.LEFT_PLAYER, (2, 5))
        self.assertEquals(answer, [(3, 6)])

    def test_empty_list(self):
        field = logic.Field(self.size)
        field[(3, 4)] = logic.RIGHT_PLAYER
        answer = field.get_selected_cells(logic.LEFT_PLAYER, (2, 5))
        self.assertEquals(answer, [])

    def test_cut_cells(self):
        field = logic.Field(self.size)
        field[(3, 4)] = logic.RIGHT_PLAYER
        answer = field.get_cut_cells(logic.LEFT_PLAYER, (2, 5))
        self.assertEquals(answer, {(4, 3): (3, 4)})
        field[(0, 9)] = -logic.RIGHT_PLAYER
        field[(6, 3)] = logic.BOTTOM_PLAYER
        self.assertEquals({(7, 2): (6, 3), (8, 1): (6, 3), (9, 0): (6, 3)},
                          field.get_cut_cells(-logic.RIGHT_PLAYER, (0, 9)))

    def test_creating_game(self):
        testing_game = game.Game(self.size)
        self.assertEquals(testing_game.active_cell, None)
        self.assertEquals(type(testing_game.current_player), int)
        self.assertTrue(1 <= testing_game.current_player <= 4)
        self.assertEquals(testing_game.field.cells,
                          logic.Field(self.size).cells)
        self.assertFalse(testing_game.over)
        self.assertFalse(testing_game.selected_cells)
        self.assertEquals(testing_game.winner, None)

    def test_game_click(self):
        for index in range(10):
            test_game = game.Game(self.size)
            test_game.click((7, 6))
            second_test_game = game.Game(self.size)
            second_test_game.field[(6, 5)] = logic.LEFT_PLAYER
            second_test_game.click((7, 4))
            if logic.RIGHT_PLAYER == test_game.current_player:
                self.assertEquals(test_game.selected_cells, [(6, 5)])
                self.assertEquals(test_game.active_cell, (7, 6))
            else:
                self.assertEquals(test_game.selected_cells, [])
            if logic.RIGHT_PLAYER == second_test_game.current_player:
                self.assertEquals(second_test_game.selected_cells,
                                  {(5, 6): (6, 5)})
            else:
                self.assertEquals(second_test_game.selected_cells, [])

    def test_cut_click(self):
        test_game = game.Game(self.size)
        test_game.current_player = logic.RIGHT_PLAYER
        test_game.field[(6, 5)] = logic.BOTTOM_PLAYER
        test_game.click((7, 4))
        test_game.click((5, 6))
        self.assertEquals(test_game.field[(7, 4)], logic.EMPTY)
        self.assertEquals(test_game.field[(6, 5)], logic.EMPTY)
        self.assertEquals(test_game.field[(5, 6)], logic.RIGHT_PLAYER)

    def test_final_line(self):
        test_game = game.Game(self.size)
        test_game.current_player = logic.RIGHT_PLAYER
        test_game.field[(1, 8)] = logic.RIGHT_PLAYER
        test_game.click((1, 8))
        test_game.click((0, 7))
        self.assertEquals(test_game.field[(0, 7)], -logic.RIGHT_PLAYER)

    def test_benefint(self):
        start = (9, 11, 5, 9)
        finish = (9, 11, 7, 9)
        self.assertEquals(ai.get_benefit(logic.TOP_PLAYER, start, finish), -2)

    def test_count_stat(self):
        field = logic.Field(self.size)
        stat = {}
        for index in range(self.size ** 2):
            curr_cell = (index % self.size, index // self.size)
            if field[curr_cell]:
                for cell in field.get_selected_cells_without_cut_factor(
                        field[curr_cell], curr_cell):
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
            bottom_sum += key[logic.BOTTOM_PLAYER]
            bottom_sum += key[-logic.BOTTOM_PLAYER]
            top_sum += key[logic.TOP_PLAYER]
            top_sum += key[-logic.TOP_PLAYER]
            left_sum += key[logic.LEFT_PLAYER]
            left_sum += key[-logic.LEFT_PLAYER]
            right_sum += key[logic.RIGHT_PLAYER]
            right_sum += key[-logic.RIGHT_PLAYER]
        self.assertEquals(ai.count_stat(field),
                          (bottom_sum, left_sum, top_sum, right_sum))

    def test_pos_steps(self):
        test_game = game.Game(self.size)
        current_player = test_game.current_player
        size = test_game.field.size
        field = test_game.field
        possible_steps = []
        cells = []
        for index in range(size ** 2):
            curr_cell = (index % size, index // size)
            if abs(field[curr_cell]) == abs(current_player):
                cells.append(curr_cell)
        for cell in cells:
            test_game.click(cell)
            if test_game.selected_cells:
                possible_cells = test_game.selected_cells
                for possible_cell in possible_cells:
                    possible_steps.append((cell, possible_cell))
        self.assertEquals(ai.get_possible_steps(test_game), possible_steps)

    def test_ai_difficulty(self):
        test_game = game.Game(10)
        test_game.players = [0, 0, 2, 2]
        while not test_game.over:
            if test_game.players[test_game.current_player - 1] == 0:
                ai.do_first_possible_step(test_game)
            else:
                ai.do_very_smart_step(test_game)
        self.assertTrue(test_game.winner == "blue" or
                        test_game.winner == "yellow")
