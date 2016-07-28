import collections
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import time
import pyqtgraph as pg

class Grapher:
    def __init__(self, ProgramStartTime = time.strftime("%Y%m%dT%H%M%S")):
        self.xData = collections.deque(maxlen=8640) #Capable of holding 24 hours of data recorded every 10 seconds. For plotting.
        self.yData = collections.deque(maxlen=8640) #After 8640, starts replacing the oldest data.
        self.Program_Start_Time = ProgramStartTime  
        self.app = QtGui.QApplication([])
        self.p = pg.plot()
        self.curve = self.p.plot(pen=pg.mkPen('b'))#pen=None, symbol='o')#pen=pg.mkPen('r'))       
        self.initializeGraph() #Setting how the plot looks
        
    def initializeGraph(self): #Setting how the plot looks
        self.p.setRange(yRange=[-20,32])
        self.p.setTitle('Temp vs. Time')
        self.p.setLabel(axis = 'left', text = 'Temperature (C)')
        self.p.setLabel(axis = 'bottom', text = "Hours since %s"%self.Program_Start_Time) 
        self.p.showGrid(x=True, y=True, alpha=None)

    def plotData(self,x,y):
        self.xData.append(x) #Appends. If full, replaces first element
        self.yData.append(y)
        self.curve.setData(list(self.xData),list(self.yData)) #Plotting the data
        self.app.processEvents()   