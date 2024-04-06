import sys
import random
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


y = []
class LiveGraph(QMainWindow):
    population = 200000
    lastPrice = 500
    lastAdv = 1
    lastProfits = 0
    lastPopularity = 0.01
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

        self.timer = self.startTimer(100)  # Обновление в милисекундах

    def tick(self):
        
        materialPrice = random.randint(150,600)
        averageTime = 1 + np.random.binomial(7, 0.5)
        averageDifficulty = 1 + np.random.binomial(4, 0.5)
        promotions = 1 + random.randint(1, 20)/100
        
        averagePrice = (materialPrice + (np.log10(averageTime*averageDifficulty)*650))*(1+self.lastPopularity)
        popularity = self.lastPopularity * (self.lastPrice / (averagePrice - np.sqrt(self.lastAdv) * promotions)) - np.square(self.lastPopularity)*0.25
        if popularity < 0.001: popularity = 0.001
        clients = self.population * np.sqrt(popularity) // 12
        workers = 2
        haircuts = (clients * (1+np.log2(workers))) // ((8 / averageTime)*22)
        revenue = haircuts * averagePrice
        
        paychecks = (15.25 * haircuts * averageTime + 20000)
        equipmentMaintenance = self.equipmentStart * (1/(12*3))
        taxes = revenue * 0.30
        if self.lastProfits > 0:    
            self.lastAdv = 1000 + 0.05 * self.lastProfits
        else:
            self.lastAdv = 1000
               

        profits = revenue - paychecks - self.equipmentStart - equipmentMaintenance - self.lastAdv - taxes
        print("")
        print("clients ", clients)
        print("avg price ", averagePrice)
        print("N ", haircuts)
        print("Revenue ", revenue)
        print("paychecks ", paychecks)
        print("profit ", profits)
        print("popularity ", popularity)
        self.lastProfits = profits 
        self.lastPopularity = popularity
        self.lastPrice = averagePrice 
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