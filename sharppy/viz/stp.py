import numpy as np
import os
from PySide import QtGui, QtCore
import sharppy.sharptab as tab
from scipy.misc import bytescale
from sharppy.sharptab.constants import *

## routine written by Kelton Halbert
## keltonhalbert@ou.edu

__all__ = ['backgroundSTP', 'plotSTP']

class backgroundSTP(QtGui.QFrame):
    '''
    Draw the background frame and lines for the Theta-E plot frame
    '''
    def __init__(self):
        super(backgroundSTP, self).__init__()
        self.initUI()


    def initUI(self):
        ## window configuration settings,
        ## sich as padding, width, height, and
        ## min/max plot axes
        self.setStyleSheet("QFrame {"
            "  background-color: rgb(0, 0, 0);"
            "  border-width: 1px;"
            "  border-style: solid;"
            "  border-color: #3399CC;}")
        self.plot_font = QtGui.QFont('Helvetica', 11)
        self.box_font = QtGui.QFont('Helvetica', 9)
        self.plot_metrics = QtGui.QFontMetrics( self.plot_font )
        self.box_metrics = QtGui.QFontMetrics(self.box_font)
        self.plot_height = self.plot_metrics.height()
        self.box_height = self.box_metrics.height()
        self.lpad = 0.; self.rpad = 0.
        self.tpad = 15.; self.bpad = 15.
        self.wid = self.size().width() - self.rpad
        self.hgt = self.size().height() - self.bpad
        self.tlx = self.rpad; self.tly = self.tpad
        self.brx = self.wid; self.bry = self.hgt
        self.stpmax = 11.; self.stpmin = 0.
        self.plotBitMap = QtGui.QPixmap(self.width()-1, self.height()-1)
        self.plotBitMap.fill(QtCore.Qt.black)
        self.plotBackground()

    def resizeEvent(self, e):
        '''
        Handles the event the window is resized
        '''
        self.initUI()
    
    def plotBackground(self):
        '''
        Handles painting the frame.
        '''
        ## initialize a painter object and draw the frame
        qp = QtGui.QPainter()
        qp.begin(self.plotBitMap)
        qp.setRenderHint(qp.Antialiasing)
        qp.setRenderHint(qp.TextAntialiasing)
        self.draw_frame(qp)
        qp.end()

    def draw_frame(self, qp):
        '''
        Draw the background frame.
        qp: QtGui.QPainter object
        '''
        ## set a new pen to draw with
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(self.plot_font)
        rect1 = QtCore.QRectF(1.5,1.5, self.brx, self.plot_height)
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter,
            'Effective Layer STP (with CIN)')

        pen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.DashLine)
        qp.setPen(pen)
        spacing = self.bry / 12.

        ytick_fontsize = 10
        y_ticks_font = QtGui.QFont('Helvetica', ytick_fontsize)
        qp.setFont(y_ticks_font)
        texts = ['11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0', ' ']
        y_ticks = np.arange(self.tpad, self.bry+spacing, spacing)
        for i in range(len(y_ticks)):
            pen = QtGui.QPen(QtGui.QColor("#0080FF"), 1, QtCore.Qt.DashLine)
            qp.setPen(pen)
            qp.drawLine(self.tlx, y_ticks[i], self.brx, y_ticks[i])
            color = QtGui.QColor('#000000')
            pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            ypos = spacing*(i+1) - (spacing/4.)
            rect = QtCore.QRect(self.tlx, ypos, 20, ytick_fontsize)
            pen = QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawText(rect, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, texts[i])

        ef = [[1.2, 2.6, 5.3, 8.3, 11.0], #ef4
              [0.2, 1.0, 2.4, 4.5, 8.4], #ef3
              [0.0, 0.6, 1.7, 3.7, 5.6], #ef2
              [0.0, 0.3, 1.2, 2.6, 4.5], #ef1
              [0.0, 0.1, 0.8, 2.0, 3.7], # ef-0
              [0.0, 0.0, 0.2, 0.7, 1.7]] #nontor
        ef = np.array(ef)
        width = self.brx / 14
        spacing = self.brx / 7
        center = np.arange(spacing, self.brx, spacing)
        texts = ['EF4+', 'EF3', 'EF2', 'EF1', 'EF0', 'NONTOR']
        ef = self.stp_to_pix(ef)
        qp.setFont(QtGui.QFont('Helvetica', 8))
        for i in range(ef.shape[0]):
            # Set green pen to draw box and whisker plots 
            pen = QtGui.QPen(QtCore.Qt.green, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            # Draw lower whisker
            qp.drawLine(center[i], ef[i,0], center[i], ef[i,1])
            # Draw box
            qp.drawLine(center[i] - width/2., ef[i,3], center[i] + width/2., ef[i,3])
            qp.drawLine(center[i] - width/2., ef[i,1], center[i] + width/2., ef[i,1])
            qp.drawLine(center[i] - width/2., ef[i,1], center[i] - width/2., ef[i,3])
            qp.drawLine(center[i] + width/2., ef[i,1], center[i] + width/2., ef[i,3])
            # Draw median
            qp.drawLine(center[i] - width/2., ef[i,2], center[i] + width/2., ef[i,2])
            # Draw upper whisker
            qp.drawLine(center[i], ef[i,3], center[i], ef[i,4])
            # Set black transparent pen to draw a rectangle
            color = QtGui.QColor('#000000')
            color.setAlpha(0)
            pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
            rect = QtCore.QRectF(center[i] - width/2., self.stp_to_pix(-.5), width, 4)
            # Change to a white pen to draw the text below the box and whisker plot
            pen = QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawText(rect, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, texts[i])

    def stp_to_pix(self, stp):
        scl1 = self.stpmax - self.stpmin
        scl2 = self.stpmin + stp
        return self.bry - (scl2 / scl1) * (self.bry - self.tpad)


class plotSTP(backgroundSTP):
    '''
    Plot the data on the frame. Inherits the background class that
    plots the frame.
    '''
    def __init__(self, prof):
        super(plotSTP, self).__init__()
        self.stp_cin = prof.stp_cin

    def resizeEvent(self, e):
        '''
        Handles when the window is resized
        '''
        super(plotSTP, self).resizeEvent(e)
        self.plotData()
    
    def paintEvent(self, e):
        super(plotSTP, self).paintEvent(e)
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawPixmap(1, 1, self.plotBitMap)
        qp.end()
    
    def plotData(self):
        '''
        Handles painting on the frame
        '''
        ## this function handles painting the plot
        ## create a new painter obkect
        qp = QtGui.QPainter()
        self.draw_stp(qp)
        self.draw_box(qp)

    def draw_stp(self, qp):
        qp.begin(self.plotBitMap)
        qp.setRenderHint(qp.Antialiasing)
        qp.setRenderHint(qp.TextAntialiasing)
        if self.stp_cin < 0:
            self.stp_cin = 0
        elif self.stp_cin > 11.:
            self.stp_cin = 11.
        if self.stp_cin < 3:
            color = QtGui.QColor('#996600')
        else:
            color = QtGui.QColor('#FF0000')
        ef = self.stp_to_pix(self.stp_cin)
        pen = QtGui.QPen(color, 1.5, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, ef, self.wid, ef)
        qp.end()

    def draw_box(self, qp):
        qp.begin(self.plotBitMap)
        width = self.brx / 14.
        left_x = width * 7
        right_x = self.brx - 5.
        top_y = self.stp_to_pix(11.)
        bot_y = top_y + (self.box_height + 1)*8
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine( left_x, top_y, right_x, top_y )
        qp.drawLine( left_x, bot_y, right_x, bot_y )
        qp.drawLine( left_x, top_y, left_x, bot_y )
        qp.drawLine( right_x, top_y, right_x, bot_y)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        pen = QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(left_x + 1., top_y + 1, right_x - left_x - 3, bot_y - top_y - 3)
        qp.setFont(self.box_font)
        pen = QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        rect1 = QtCore.QRectF(left_x+3,top_y + 2, right_x - left_x - 3, self.box_height)
        rect2 = QtCore.QRectF(left_x+3, top_y + self.box_height + 1, right_x - left_x - 3, self.box_height)
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft,
            'Prob EF2+ torn with supercell')
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft,
            'Sample CLIMO = .xx sigtor')
        qp.drawLine(left_x, top_y + self.box_height*2, right_x, top_y + self.box_height*2 )
        rect1 = QtCore.QRectF(left_x+3, top_y + (self.box_height + 1)*2, right_x - left_x - 3, self.box_height)
        rect2 = QtCore.QRectF(left_x+3, top_y + (self.box_height + 1)*3, right_x - left_x - 3, self.box_height)
        rect3 = QtCore.QRectF(left_x+3, top_y + (self.box_height + 1)*4, right_x - left_x - 3, self.box_height)
        rect4 = QtCore.QRectF(left_x+3, top_y + (self.box_height + 1)*5, right_x - left_x - 3, self.box_height)
        rect5 = QtCore.QRectF(left_x+3, top_y + (self.box_height + 1)*6, right_x - left_x - 3, self.box_height)
        rect6 = QtCore.QRectF(left_x+3, top_y + (self.box_height + 1)*7, right_x - left_x - 3, self.box_height)
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'based on CAPE: ')
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'based on LCL:')
        qp.drawText(rect3, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'based on ESRH:')
        qp.drawText(rect4, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'based on EBWD:')
        qp.drawText(rect5, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'based on STPC:')
        qp.drawText(rect6, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'based on SPC_fixed:')
        qp.end()

