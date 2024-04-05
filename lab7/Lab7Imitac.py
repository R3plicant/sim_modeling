import sys
import random
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


y = [random.randint(0, 10) for _ in range(1)]
class LiveGraph(QMainWindow):
    population = 200000
    lastPrice = 500
    lastAdv = 1
    lastProfits = 0
    equipmentStart = 100000
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

    def tick(self):
        
        materialPrice = random.randint(50,100)
        averageTime = random.randint(1,8)
        averageDifficulty = random.randint(1,5)
    
        averagePrice = 450*averageTime + materialPrice * (1 +  averageTime/8) * (1 + averageDifficulty/5) ##
        popularity = ((self.lastPrice - averagePrice)/averagePrice + self.lastAdv/self.population) % 1
        clients = self.population * popularity
        workers = 1
        haircuts = int((clients * 1.5) % ((8 / averageTime)*22*workers))
        revenue = haircuts * averagePrice
        
        paychecks = 156.25 * haircuts * averageTime + 20000
        equipmentMaintenance = self.equipmentStart * (1/12)
        taxes = revenue * 0.13
        self.lastAdv = 0.05 * self.lastProfits
               

        profits = revenue - paychecks - self.equipmentStart - equipmentMaintenance - self.lastAdv - taxes
        print("")
        print("avg price ", averagePrice)
        print("N ", haircuts)
        print("Revenue ", revenue)
        print("paychecks ", paychecks)
        print("profit ", profits)
        print("popularity ", popularity)
        self.lastProfits = profits 

        return profits



    def timerEvent(self, event):
        global y
        if(len(y) == 100):
            y = y[1:]
            y.append(self.tick())
            x = np.arange(0, len(y))
        else:            
            y.append(self.tick())
            x = np.arange(0, len(y))
        self.ax.clear()
        self.ax.plot(x, y)
        self.canvas.draw()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LiveGraph()
    window.show()
    sys.exit(app.exec_())