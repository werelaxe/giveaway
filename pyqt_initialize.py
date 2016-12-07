import sys
from graphics import draw_game
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from game import Game
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QBasicTimer
from ai import do_first_possible_step, do_smart_step



class Example(QWidget):
    def __init__(self, resolution):
        super().__init__()
        res_width, res_height = resolution.width(), resolution.height()

        self.res_width = res_width
        self.timer = QBasicTimer()
        self.res_height = res_height
        self.game = Game(14)
        self.factor = (res_height - 100) / self.game.field.size
        self.init_ui()

    def init_ui(self):
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
        print(x_coord, y_coord)
        if x_coord >= self.game.field.size:
            return
        if event.button() == Qt.LeftButton:
            self.game.click((x_coord, y_coord))
        if event.button() == Qt.RightButton:
            self.game.change_cell((x_coord, y_coord))
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
            do_smart_step(self.game)
            self.update()

    def timerEvent(self, e):
        if self.game.current_player != 1:
            do_first_possible_step(self.game)
        else:
            return
        if self.game.over:
            self.close()
        self.update()

    def update(self, *__args):
        self.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    resolution = app.desktop().screenGeometry()
    ex = Example(resolution)
    sys.exit(app.exec_())
