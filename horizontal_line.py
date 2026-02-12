import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor

class HorizontalLine(QWidget):
    def __init__(self):
        super().__init__()
        # Настройки окна: прозрачность, поверх всех окон, без рамок
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Начальные параметры линии
        self.line_width = 400
        self.line_thickness = 5
        self.setGeometry(100, 100, self.line_width, self.line_thickness + 20)
        
        self.dragging = False
        self.resizing = False
        self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0, 200)) # Красный цвет с небольшой прозрачностью
        pen.setWidth(self.line_thickness)
        painter.setPen(pen)
        painter.drawLine(0, self.height() // 2, self.width(), self.height() // 2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Если кликаем в правой части линии — меняем ширину, иначе — двигаем
            if event.x() > self.width() - 20:
                self.resizing = True
            else:
                self.dragging = True
                self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToGlobal(event.pos() - self.offset))
        elif self.resizing:
            new_width = max(50, event.x())
            self.resize(new_width, self.height())

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.resizing = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    line = HorizontalLine()
    line.show()
    print("Управление:\n- ЛКМ за левую часть: Перемещение\n- ЛКМ за правый край: Изменение ширины\n- ESC: Выход")
    sys.exit(app.exec_())

