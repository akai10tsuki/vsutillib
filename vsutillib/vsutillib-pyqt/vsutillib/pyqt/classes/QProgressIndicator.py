"""
QProgressIndicator

Returns:
    [type]: [description]
"""

import sys

from PySide2.QtCore import Qt, QSize, Property
from PySide2.QtGui import QPainter, QColor
from PySide2.QtWidgets import QWidget, QApplication, QSizePolicy


class QProgressIndicator(QWidget):
    """
    QProgressIndicator show progress animation
    """
    def __init__(self, parent):
        # Call parent class constructor first
        super(QProgressIndicator, self).__init__(parent)

        # Initialize Qt Properties
        self.setProperties()

        # Initialize instance variables
        self.angle = 0
        self.timerId = -1
        self.delay = 40
        self.displayedWhenStopped = False
        self.color = Qt.black
        self.displayedWhenStopped = None

        # Set size and focus policy
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.NoFocus)

        # Show the widget
        self.show()

    def animationDelay(self):
        return self.delay

    def isAnimated(self):
        return self.timerId != -1

    def isDisplayedWhenStopped(self):
        return self.displayedWhenStopped

    def getColor(self):
        return self.color

    def sizeHint(self):
        return QSize(20, 20)

    def startAnimation(self):
        self.angle = 0

        if self.timerId == -1:
            self.timerId = self.startTimer(self.delay)

    def stopAnimation(self):
        if self.timerId != -1:
            self.killTimer(self.timerId)

        self.timerId = -1
        self.update()

    def setAnimationDelay(self, delay):
        if self.timerId != -1:
            self.killTimer(self.timerId)

        self.delay = delay

        if self.timerId != -1:
            self.timerId = self.startTimer(self.delay)

    def setDisplayedWhenStopped(self, state):
        self.displayedWhenStopped = state
        self.update()

    def setColor(self, color):
        self.color = color
        self.update()

    def timerEvent(self, event):
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        if (not self.displayedWhenStopped) and (not self.isAnimated()):
            return

        width = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        outerRadius = (width - 1) * 0.5
        innerRadius = (width - 1) * 0.5 * 0.38

        capsuleHeight = outerRadius - innerRadius
        capsuleWidth = capsuleHeight * 0.23 if (width > 32) else capsuleHeight * 0.35
        capsuleRadius = capsuleWidth / 2

        for i in range(0, 12):
            color = QColor(self.color)

            if self.isAnimated():
                color.setAlphaF(1.0 - (i / 12.0))
            else:
                color.setAlphaF(0.2)

            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.save()
            painter.translate(self.rect().center())
            painter.rotate(self.angle - (i * 30.0))
            painter.drawRoundedRect(
                capsuleWidth * -0.5,
                (innerRadius + capsuleHeight) * -1,
                capsuleWidth,
                capsuleHeight,
                capsuleRadius,
                capsuleRadius,
            )
            painter.restore()

    def setProperties(self):
        self.delay = Property(int, self.animationDelay, self.setAnimationDelay)
        self.displayedWhenStopped = Property(
            bool, self.isDisplayedWhenStopped, self.setDisplayedWhenStopped
        )
        self.color = Property(QColor, self.getColor, self.setColor)


def TestProgressIndicator():
    app = QApplication(sys.argv)
    progress = QProgressIndicator(None)
    progress.setAnimationDelay(70)
    progress.startAnimation()

    # Execute the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    TestProgressIndicator()
