"""

The MIT License (MIT)

Copyright (c) 2011 Morgan Leborgne

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


QProgressIndicator

Returns:
    [type]: [description]

https://github.com/mojocorp/QProgressIndicator

https://github.com/z3ntu/QtWaitingSpinner
https://stackoverflow.com/questions/52313073/making-an-invisible-layer-in-pyqt-which-covers-the-whole-dialog/52316134#52316134


import math
from PyQt5 import QtCore, QtGui, QtWidgets


class QtWaitingSpinner(QtWidgets.QWidget):
    def __init__(self, parent=None, centerOnParent=True, disableParentWhenSpinning=False, modality=QtCore.Qt.NonModal):
        super().__init__(parent, flags=QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning

        # WAS IN initialize()
        self._color = QtGui.QColor(QtCore.Qt.black)
        self._roundness = 100.0
        self._minimumTrailOpacity = 3.14159265358979323846
        self._trailFadePercentage = 80.0
        self._revolutionsPerSecond = 1.57079632679489661923
        self._numberOfLines = 20
        self._lineLength = 10
        self._lineWidth = 2
        self._innerRadius = 10
        self._currentCounter = 0
        self._isSpinning = False

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()
        self.hide()
        # END initialize()

        self.setWindowModality(modality)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def paintEvent(self, QPaintEvent):
        self.updatePosition()
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(QtCore.Qt.NoPen)
        for i in range(0, self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength, self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(i, self._currentCounter, self._numberOfLines)
            color = self.currentLineColor(distance, self._numberOfLines, self._trailFadePercentage,
                                          self._minimumTrailOpacity, self._color)
            painter.setBrush(color)
            painter.drawRoundedRect(QtCore.QRect(0, -self._lineWidth / 2, self._lineLength, self._lineWidth), self._roundness,
                                    self._roundness, QtCore.Qt.RelativeSize)
            painter.restore()

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength(self, length):
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.updateSize()

    def color(self):
        return self._color

    def roundness(self):
        return self._roundness

    def minimumTrailOpacity(self):
        return self._minimumTrailOpacity

    def trailFadePercentage(self):
        return self._trailFadePercentage

    def revolutionsPersSecond(self):
        return self._revolutionsPerSecond

    def numberOfLines(self):
        return self._numberOfLines

    def lineLength(self):
        return self._lineLength

    def lineWidth(self):
        return self._lineWidth

    def innerRadius(self):
        return self._innerRadius

    def isSpinning(self):
        return self._isSpinning

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color=QtCore.Qt.black):
        self._color = QColor(color)

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minimumTrailOpacity = minimumTrailOpacity

    def rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def updateSize(self):
        size = (self._innerRadius + self._lineLength) * 2
        self.setFixedSize(size, size)

    def updateTimer(self):
        self._timer.setInterval(1000 / (self._numberOfLines * self._revolutionsPerSecond))

    def updatePosition(self):
        if self.parentWidget() and self._centerOnParent:
            parentRect = QtCore.QRect(self.parentWidget().mapToGlobal(QtCore.QPoint(0, 0)), self.parentWidget().size())
            self.move(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.size(), parentRect).topLeft())


    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, colorinput):
        color = QtGui.QColor(colorinput)
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int(math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0))
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color

"""

import sys

from PySide6.QtCore import Qt, QSize, QTimerEvent, Signal, Slot
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget, QApplication, QSizePolicy


class QProgressIndicator(QWidget):
    """
    ProgressIndicator show progress animation
    """

    startAnimationSignal = Signal()
    stopAnimationSignal = Signal()

    def __init__(self, parent: QWidget) -> None:
        # Call parent class constructor first
        super(QProgressIndicator, self).__init__(parent)

        # Initialize instance variables
        self.angle = 0
        self.timerId = -1

        self.__delay = 40
        self.__displayedWhenStopped = False
        self.__color = QColor(0, 0, 0)

        # Set size and focus policy
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.NoFocus)

        self.startAnimationSignal.connect(self.startAnimation)
        self.stopAnimationSignal.connect(self.stopAnimation)

        # Show the widget
        self.show()

    @property
    def color(self) -> QColor:
        return self.__color

    @color.setter
    def color(self, value: QColor) -> None:
        self.__color = value
        self.update()

    @property
    def delay(self) -> int:
        return self.__delay

    @delay.setter
    def delay(self, value: int) -> None:
        self.__delay = value
        if self.timerId != -1:
            self.killTimer(self.timerId)
            self.timerId = self.startTimer(self.__delay)

    @property
    def displayedWhenStopped(self) -> bool:
        return self.__displayedWhenStopped

    @displayedWhenStopped.setter
    def displayedWhenStopped(self, value: bool) -> None:
        self.__displayedWhenStopped = value
        self.update()

    def heightForWidth(self, w: int) -> int:
        return w

    def sizeHint(self) -> QSize:
        return QSize(30, 30)

    def timerEvent(self, event: QTimerEvent) -> None:
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # pylint: disable=unused-argument
        if (not self.displayedWhenStopped) and (not self.isAnimated()):
            return None

        width = min(self.width(), self.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        outerRadius = (width - 1) * 0.5
        innerRadius = (width - 1) * 0.5 * 0.38

        capsuleHeight = outerRadius - innerRadius
        capsuleWidth = capsuleHeight * 0.23 if (width > 32) else capsuleHeight * 0.35
        capsuleRadius = capsuleWidth / 2

        for i in range(0, 12):
            color = QColor(self.color)

            color.setAlphaF(1.0 - (i / 12.0))

            p.setPen(Qt.NoPen)
            p.setBrush(color)
            p.save()
            p.translate(self.rect().center())
            p.rotate(self.angle - (i * 30.0))
            p.drawRoundedRect(
                -capsuleWidth * 0.5,
                -(innerRadius + capsuleHeight),
                capsuleWidth,
                capsuleHeight,
                capsuleRadius,
                capsuleRadius,
            )
            p.restore()

    def isAnimated(self) -> bool:
        return bool(self.timerId != -1)

    @Slot()
    def startAnimation(self) -> None:
        self.angle = 0
        if self.timerId == -1:
            self.timerId = self.startTimer(self.delay)

    @Slot()
    def stopAnimation(self) -> None:
        if self.timerId != -1:
            self.killTimer(self.timerId)

        self.angle = 0
        self.timerId = -1
        self.update()


if __name__ == "__main__":

    from PySide2.QtWidgets import QGridLayout, QMainWindow, QPushButton

    class MainWindow(QMainWindow):
        """Test the progress bars"""

        def __init__(self, *args, **kwargs):
            super(MainWindow, self).__init__(*args, **kwargs)

            l = QGridLayout()

            self.pi = QProgressIndicator(self)
            self.pi.displayedWhenStopped = True

            a = QPushButton("Animate")
            a.pressed.connect(self.animate)
            s = QPushButton("Stop Animation")
            s.pressed.connect(self.stopAnimation)

            l.addWidget(self.pi, 0, 0, Qt.AlignCenter)
            l.addWidget(a, 1, 0)
            l.addWidget(s, 2, 0)

            w = QWidget()
            w.setLayout(l)

            self.setCentralWidget(w)

            self.show()

        def animate(self):
            self.pi.startAnimation()

        def stopAnimation(self):
            self.pi.stopAnimation()

    # pylint: disable=invalid-name
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
