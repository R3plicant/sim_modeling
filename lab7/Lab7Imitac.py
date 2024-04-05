import sys
import random
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


y = [random.randint(0, 10) for _ in range(1)]
class LiveGraph(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Live Graph')
        self.setGeometry(100, 100, 800, 600)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(0, 200)
        self.ax.set_ylim(0, 200)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.timer = self.startTimer(1000)  # Обновление каждую секунду

    def timerEvent(self, event):
        global y
        if(len(y) == 10):
            y = y[1:]
            y.append(random.randint(0,10))
            x = np.arange(0, len(y))
        else:            
            y.append(random.randint(0,10))
            x = np.arange(0, len(y))
        print(x)
        print(y)
        self.ax.clear()
        self.ax.plot(x, y)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LiveGraph()
    window.show()
    sys.exit(app.exec_())