from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen

from logic import LEFT_PLAYER, RIGHT_PLAYER, BOTTOM_PLAYER, TOP_PLAYER

DARK_BROWN = QColor(150, 53, 0)
LIGHT_BROWN = QColor(255, 209, 71)


def set_current_color(cell, qp):
    if abs(cell) == BOTTOM_PLAYER:
        qp.setBrush(Qt.red)
    elif abs(cell) == LEFT_PLAYER:
        qp.setBrush(Qt.green)
    elif abs(cell) == TOP_PLAYER:
        qp.setBrush(Qt.blue)
    elif abs(cell) == RIGHT_PLAYER:
        qp.setBrush(Qt.yellow)


def draw_game(qp, game, width, height, factor, correction=0.8):
    field = game.field
    qp.setBrush(DARK_BROWN)
    qp.drawRect(0, 0, width, height)
    qp.setPen(Qt.black)
    for index in range(field.size * field.size):
        x_coord = index % field.size
        y_coord = index // field.size
        if (index + y_coord + 1) % 2:
            qp.setBrush(LIGHT_BROWN)
            qp.drawRect(x_coord * factor, y_coord * factor, factor, factor)

    pen = QPen(Qt.green, 5, Qt.SolidLine)
    qp.setPen(pen)
    qp.setBrush(DARK_BROWN)
    # print(game.selected_cells)
    for selected_cell in game.selected_cells:
        x_coord, y_coord = selected_cell
        qp.drawRect(x_coord * factor, y_coord * factor, factor, factor)
    if game.active_cell is not None:
        x_coord, y_coord = game.active_cell
        qp.drawRect(x_coord * factor, y_coord * factor, factor, factor)

    qp.setPen(Qt.black)
    for index in range(field.size * field.size):
        x_coord = index % field.size
        y_coord = index // field.size
        cell = field.cells[y_coord][x_coord]
        if cell:
            set_current_color(cell, qp)
            qp.drawEllipse(x_coord * factor + factor * (1 - correction) / 2,
                           y_coord * factor + factor * (1 - correction) / 2,
                           factor * correction, factor * correction)
            if cell < 0:
                for coefficient in range(5):
                    coeff = 1 - (coefficient + 1) / 5
                    print(coeff)
                    qp.drawEllipse(x_coord * factor + factor * (1 - correction * coeff) / 2,
                                   y_coord * factor + factor * (1 - correction * coeff) / 2,
                                   factor * correction * coeff, factor * correction * coeff)

