from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen

from logic import LEFT_PLAYER, RIGHT_PLAYER, BOTTOM_PLAYER, TOP_PLAYER

VERTY_DARK_BROWN = QColor(120, 33, 0)
DARK_BROWN = QColor(150, 53, 0)
LIGHT_BROWN = QColor(255, 209, 71)


def set_current_color(player, qp):
    if abs(player) == BOTTOM_PLAYER:
        qp.setBrush(Qt.red)
    elif abs(player) == LEFT_PLAYER:
        qp.setBrush(Qt.green)
    elif abs(player) == TOP_PLAYER:
        qp.setBrush(Qt.blue)
    elif abs(player) == RIGHT_PLAYER:
        qp.setBrush(Qt.yellow)


def draw_status_bar(qp, game, width, height, factor, correction):
    qp.setBrush(VERTY_DARK_BROWN)
    qp.drawRect(height, 0, height, height)
    qp.setPen(LIGHT_BROWN)
    qp.setFont(QFont('Times new roman', 25))
    qp.drawText(height - 30, 0, 200, 60, Qt.AlignCenter, "Player:")
    qp.setPen(Qt.black)
    set_current_color(game.current_player, qp)
    qp.drawEllipse(height + 130, 15, factor * correction, factor * correction)


def draw_field(qp, field, width, height, factor):
    qp.setBrush(DARK_BROWN)
    qp.drawRect(0, 0, width, height)
    qp.setPen(Qt.black)
    for index in range(field.size ** 2):
        x_coord = index % field.size
        y_coord = index // field.size
        if (index + y_coord + 1) % 2:
            qp.setBrush(LIGHT_BROWN)
            qp.drawRect(x_coord * factor, y_coord * factor, factor, factor)


def draw_active_cells(qp, game, factor):
    pen = QPen(Qt.green, 5, Qt.SolidLine)
    qp.setPen(pen)
    qp.setBrush(DARK_BROWN)
    for selected_cell in game.selected_cells:
        x_coord, y_coord = selected_cell
        qp.drawRect(x_coord * factor, y_coord * factor, factor, factor)
    if game.active_cell is not None:
        x_coord, y_coord = game.active_cell
        qp.drawRect(x_coord * factor, y_coord * factor, factor, factor)


def draw_cells(qp, field, factor, correction=0.8):
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
                    qp.drawEllipse(x_coord * factor + factor * (1 - correction * coeff) / 2,
                                   y_coord * factor + factor * (1 - correction * coeff) / 2,
                                   factor * correction * coeff, factor * correction * coeff)


def draw_game(qp, game, width, height, factor, correction=0.8):
    field = game.field
    draw_field(qp, field, width, height, factor)
    draw_status_bar(qp, game, width, height, factor, correction)
    draw_active_cells(qp, game, factor)
    draw_cells(qp, field, factor, correction)


