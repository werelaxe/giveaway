import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QVBoxLayout

from graphics import draw_game
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from game import Game
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QBasicTimer
from ai import do_first_possible_step, do_smart_step, do_very_smart_step
import ai

LABELS = {"CPU easy": 0, "CPU medium": 1, "CPU hard": 2, "human": 3}


class Giveaway(QWidget):
    def __init__(self, resolution):
        super().__init__()
        res_width, res_height = resolution.width(), resolution.height()
        self.res_width = res_width
        self.timer = QBasicTimer()
        self.res_height = res_height
        self.game = Game(12)
        self.factor = (res_height - 100) / self.game.field.size
        self.is_waiting = False
        # self.init_ui()

    def init_ui(self, params):
        self.game.players = params
        print(params)
        height = self.res_height - 100
        self.setGeometry((self.res_width - height - 200) / 2,
                         100 / 2, height + 200, height)
        self.timer = QBasicTimer()
        self.timer.start(0, self)
        self.setWindowTitle('Giveaway')
        self.show()

    def mousePressEvent(self, event):
        if not self.is_waiting:
            return
        x_coord = int(event.pos().x() / self.factor)
        y_coord = int(event.pos().y() / self.factor)
        if x_coord >= self.game.field.size:
            return
        if event.button() == Qt.LeftButton:
            self.game.click((x_coord, y_coord))
        if event.button() == Qt.RightButton:
            self.game.change_cell((x_coord, y_coord))
        if event.button() == Qt.MiddleButton:
            pass
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        draw_game(qp, self.game, self.width(), self.height(), self.factor)
        qp.end()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Control:
            # do_first_possible_step(self.game)
            # do_smart_step(self.game)
            do_very_smart_step(self.game)
            self.update()
        if event.key() == Qt.Key_Space:
            pass

    def timerEvent(self, e):
        if self.game.players[self.game.current_player - 1] == 0:
            do_first_possible_step(self.game)
        elif self.game.players[self.game.current_player - 1] == 1:
            do_smart_step(self.game)
        elif self.game.players[self.game.current_player - 1] == 2:
            do_very_smart_step(self.game)
        else:
            self.is_waiting = True

        if self.game.over:
            # self.close()
            print("Game over!")
            self.timer.stop()
        self.update()

    def update(self, *__args):
        self.repaint()

    def closeEvent(self, event):
        self.close()


def add_field(player_combo_box):
    player_combo_box.setFont(QFont('SansSerif', 40))
    player_combo_box.addItem("human")
    player_combo_box.addItem("CPU easy")
    player_combo_box.addItem("CPU medium")
    player_combo_box.addItem("CPU hard")


class StartMenu(QWidget):
    def __init__(self, resolution, start_event):
        self.start_event = start_event
        super().__init__()
        self.resolution = resolution
        res_width, res_height = resolution.width(), resolution.height()
        self.res_width = res_width
        self.res_height = res_height
        self.buttons = {}
        self.init_ui()

    def init_ui(self):
        height = self.res_height - 100
        self.setGeometry((self.res_width - height - 200) / 2,
                         100 / 2, height + 200, height)
        btn = QPushButton('Start game', self)
        btn.setFont(QFont('SansSerif', 40))
        btn.resize(btn.sizeHint())

        btn.clicked.connect(self.start_game)
        layout = QVBoxLayout()  # layout for the central widget
        widget = QWidget()  # central widget

        self.first_player = QtWidgets.QComboBox(widget)
        add_field(self.first_player)
        layout.addWidget(self.first_player)

        self.second_player = QtWidgets.QComboBox(widget)
        add_field(self.second_player)
        layout.addWidget(self.second_player)

        self.third_player= QtWidgets.QComboBox(widget)
        add_field(self.third_player)
        layout.addWidget(self.third_player)

        self.fourth_player = QtWidgets.QComboBox(widget)
        add_field(self.fourth_player)
        layout.addWidget(self.fourth_player)

        layout.addWidget(btn)
        widget.setLayout(layout)


        self.setLayout(layout)
        self.setWindowTitle('Giveaway')
        self.show()

    def start_game(self):
        self.close()
        difficulty = [0] * 4
        difficulty[0] = LABELS[self.first_player.currentText()]
        difficulty[1] = LABELS[self.second_player.currentText()]
        difficulty[2] = LABELS[self.third_player.currentText()]
        difficulty[3] = LABELS[self.fourth_player.currentText()]
        self.start_event(difficulty)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


def new_game():
    app = QApplication(sys.argv)
    resolution = app.desktop().screenGeometry()
    form = Giveaway(resolution)
    menu = StartMenu(resolution, form.init_ui)
    sys.exit(app.exec_())

