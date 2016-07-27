import collections
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import time
import pyqtgraph as pg

class Grapher:
    
    def initializeGraph(self):
        self.p.setRange(yRange=[-20,32])
        self.p.setTitle('Temp vs. Time')
        self.p.setLabel(axis = 'left', text = 'Temperature (C)')
        self.p.setLabel(axis = 'bottom', text = "Hours since %s"%self.Program_Start_Time) 
        self.p.showGrid(x=True, y=True, alpha=None)
    
    def __init__(self, ProgramStartTime = time.strftime("%Y%m%dT%H%M%S")):
        self.xData = collections.deque(maxlen=8640)
        self.yData = collections.deque(maxlen=8640)
        self.Program_Start_Time = ProgramStartTime
        
        self.app = QtGui.QApplication([])
        self.p = pg.plot()
        self.curve = self.p.plot(pen=pg.mkPen('b'))#pen=None, symbol='o')#pen=pg.mkPen('r'))       
        
        self.initializeGraph() #CHECK OUT IF NOT WORKING
    
    


    def plotData(self,x,y):
        global curve, xData, yData
        self.xData.append(x)
        self.yData.append(y)
        curve.setData(list(self.xData),list(self.yData))
        app.processEvents()   