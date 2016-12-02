import sys
from graphics import draw_game
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from game import Game
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QBasicTimer

width = 800
height = 800


class Example(QWidget):
    def __init__(self, resolution):
        super().__init__()
        res_width, res_height = resolution.width(), resolution.height()
        self.res_width = res_width
        self.timer = QBasicTimer()
        self.res_height = res_height
        self.game = Game(14)
        self.factor = width // self.game.field.size
        self.init_ui()

    def init_ui(self):
        self.setGeometry((self.res_width - width) // 2,
                         (self.res_height - height) // 2, width, height)
        self.setWindowTitle('Giveaway')
        self.show()

    def mousePressEvent(self, event):
        x_coord = event.pos().x() // self.factor
        y_coord = event.pos().y() // self.factor
        self.game.click(x_coord, y_coord)
        print(self.game.current_player)
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        draw_game(qp, self.game, self.width(), self.height(), self.factor)
        qp.end()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example(app.desktop().screenGeometry())
    sys.exit(app.exec_())
