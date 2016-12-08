import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from graphics import draw_game
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from game import Game
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QBasicTimer
from ai import do_first_possible_step, do_smart_step, do_very_smart_step

LABELS = {"CPU easy": 0, "CPU medium": 1, "CPU hard": 2, "human": 3}


class Giveaway(QWidget):
    def __init__(self, resolution):
        super().__init__()
        res_width, res_height = resolution.width(), resolution.height()
        self.res_width = res_width
        self.timer = QBasicTimer()
        self.res_height = res_height
        self.is_waiting = False
        self.user_want_exit = False
        self.game = None
        self.factor = -1

    def init_ui(self, params):
        self.game = Game(params[0])
        self.factor = (self.res_height - 100) / self.game.field.size
        self.game.players = params[1]

        height = self.res_height - 100
        self.setGeometry((self.res_width - height - 200) / 2,
                         100 / 2, height + 200, height)
        self.timer = QBasicTimer()
        self.timer.start(0, self)
        self.setWindowTitle('Giveaway')
        self.show()

    def mousePressEvent(self, event):
        if not self.is_waiting or self.game.over:
            return
        x_coord = int(event.pos().x() / self.factor)
        y_coord = int(event.pos().y() / self.factor)
        if x_coord >= self.game.field.size:
            return
        if event.button() == Qt.LeftButton:
            self.game.click((x_coord, y_coord))
        if event.button() == Qt.RightButton:
            # self.game.change_cell((x_coord, y_coord))
            print(x_coord, y_coord)
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
            self.timer.stop()
        self.update()

    def update(self, *__args):
        if self.game.over:
            QMessageBox.question(self, 'GAME OVER', "{} wins!".format(
                self.game.winner), QMessageBox.Ok)
        self.repaint()

    def ask_closing(self, event):
        self.timer.stop()
        reply = QMessageBox.question(
            self, 'Confirm closing', "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.user_want_exit = True
            event.accept()
        else:
            event.ignore()
            self.timer.start(0, self)

    def closeEvent(self, event):
        if not self.user_want_exit:
            self.ask_closing(event)


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

        self.size_combo = QtWidgets.QComboBox(widget)
        for index in range(4, 21):
            self.size_combo.addItem(str(index * 2))
        self.size_combo.setCurrentText("14")
        self.size_combo.setFont(QFont('SansSerif', 40))
        self.setToolTip("Field size")
        layout.addWidget(self.size_combo)

        self.first_player = QtWidgets.QComboBox(widget)
        add_field(self.first_player)
        layout.addWidget(self.first_player)

        self.second_player = QtWidgets.QComboBox(widget)
        add_field(self.second_player)
        layout.addWidget(self.second_player)

        self.third_player = QtWidgets.QComboBox(widget)
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
        field_size = int(self.size_combo.currentText())
        self.start_event((field_size, difficulty))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


def new_game():
    app = QApplication(sys.argv)
    resolution = app.desktop().screenGeometry()
    form = Giveaway(resolution)
    menu = StartMenu(resolution, form.init_ui)
    sys.exit(app.exec_())
