import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QToolTip
from PyQt5.QtWidgets import QVBoxLayout

from graphics import draw_game
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from game import Game
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QBasicTimer
from ai import do_first_possible_step, do_smart_step, do_very_smart_step
import ai


class Giveaway(QWidget):
    def __init__(self, resolution):
        super().__init__()
        res_width, res_height = resolution.width(), resolution.height()
        self.res_width = res_width
        self.timer = QBasicTimer()
        self.res_height = res_height
        self.game = Game(12)
        self.factor = (res_height - 100) / self.game.field.size
        # self.init_ui()

    def init_ui(self, params):
        print(params)
        height = self.res_height - 100
        self.setGeometry((self.res_width - height - 200) / 2,
                         100 / 2, height + 200, height)
        self.timer = QBasicTimer()
        self.timer.start(0, self)
        self.setWindowTitle('Giveaway')
        self.show()

    def mousePressEvent(self, event):
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
        if self.game.current_player != -1:
            # do_smart_step(self.game)
            do_very_smart_step(self.game)
        else:
            return
        if self.game.over:
            # self.close()
            print("Game over!")
            self.timer.stop()
        self.update()

    def update(self, *__args):
        self.repaint()

    def closeEvent(self, event):
        self.close()


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
        btn.setFont(QFont('SansSerif', 20))
        btn.resize(btn.sizeHint())



        btn.clicked.connect(self.start_game)
        layout = QHBoxLayout()  # layout for the central widget
        layout.addWidget(btn)
        widget = QWidget()  # central widget
        widget.setLayout(layout)

        listWidget = QListWidget()
        listWidget.addItem(QListWidgetItem("easy"))
        listWidget.addItem(QListWidgetItem("medium"))
        listWidget.addItem(QListWidgetItem("hard"))
        listWidget.addItem(QListWidgetItem("human"))

        layout.addWidget(listWidget)

        self.setLayout(layout)
        self.setWindowTitle('Giveaway')
        self.show()

    def start_game(self):
        self.close()
        for indx in range(4):
            print(indx, self.buttons[("easy", indx)].isChecked())

        self.start_event(1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


def new_game():
    app = QApplication(sys.argv)
    resolution = app.desktop().screenGeometry()
    form = Giveaway(resolution)
    menu = StartMenu(resolution, form.init_ui)
    sys.exit(app.exec_())

