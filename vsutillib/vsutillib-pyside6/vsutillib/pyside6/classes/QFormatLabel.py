"""
Job info widget

format is Jobs: {:3d} Current Job: {:3d} File: {:3d} of {:3d} Errors: {:3d}

Jobs: total jobs
jobID: current running job
file: file number been work on current job
totalFiles: total files on current job
errors: total errors on current job
align:
    Qt.Horizontal - Horizontal layout the default
    Qt.Vertical - Vertical layout
"""

import random


from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Slot, Signal


class QFormatLabel(QLabel):
    """
    Dual QProgressBar for unit and total progress

    param align - Set alignment Qt.Horizontal or Qt.Vertical
    type align - Qt.AlignmentFlags
    """

    setTemplateSignal = Signal(str)
    setValueSignal = Signal(int, object)
    setValuesSignal = Signal(list)

    def __init__(self, *args: str, **kwargs: list[object]) -> None:

        template = kwargs.pop("template", None)
        initValues = kwargs.pop("init", None)

        if (args) or (template is not None):
            if initValues is None:
                raise KeyError("init= not specified")

            if args:
                if isinstance(args[0], str):
                    template = args[0]
                    args = args[1:]

        if initValues is None:
            initValues = []

        super().__init__(*args, **kwargs)

        self.setTemplateSignal.connect(self.setTemplate)
        self.setValueSignal.connect(self.setValue)
        self.setValuesSignal.connect(self.setValues)

        if template is None:
            self._template = (
                "Job(s): {0:3d} Running: {1:3d} File: {2:3d} of {3:3d} Errors: {4:3d}"
            )
            initValues = [0, 0, 0, 0, 0]
        else:
            self._template = template

        self._values = initValues
        self._refresh()

    def __getitem__(self, index: int) -> int:
        return self._values[index]

    def __setitem__(self, index: int, value: object):
        self.setValueSignal.emit(index, value)

    def _refresh(self) -> None:

        strTmp = self._template
        strTmp = strTmp.format(*self._values)
        super().setText(strTmp)

    @property
    def template(self) -> str:
        return self._template

    @template.setter
    def template(self, value: str) -> None:

        if isinstance(value, str):
            self._template = value
            self._refresh()

    @Slot(str)
    def setTemplate(self, value: str) -> None:

        if isinstance(value, str):
            self._template = value
            self._refresh()

    @Slot(list)
    def setValues(self, args: list[object]) -> None:
        """
        Set Values

        :param args: set values
        :type args: list
        """

        self._values = list(args)
        self._refresh()

    @Slot(int, object)
    def setValue(self, index: int, value: object) -> None:
        """
        Set value index based

        :param index: index position
        :type index: int
        :param value: value to set
        :type value: object
        """

        self._values[index] = value
        self._refresh()

    @property
    def values(self) -> list[object]:
        """return current positional values"""

        return self._values

    def valuesConnect(self, signal: Signal) -> None:
        """make connection to setValues Slot"""

        signal.connect(self.setValues)

    def valueConnect(self, signal: Signal) -> None:
        """make connection to setValues Slot"""

        signal.connect(self.setValue)


if __name__ == "__main__":

    import sys

    from PySide2.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton

    class MainWindow(QMainWindow):
        """Test the progress bars"""

        def __init__(self) -> None:
            super().__init__()

            l = QGridLayout()

            self.jobInfo = QFormatLabel()
            self.formatLabel = QFormatLabel(
                "Random 1 = {0:>3d} -- Random 2 = {1:3d}", init=[10, 20]
            )

            b = QPushButton("Test 1")
            b.pressed.connect(self.test)
            b1 = QPushButton("Test 2")
            b1.pressed.connect(self.test1)
            l.addWidget(self.jobInfo, 0, 0)
            l.addWidget(self.formatLabel, 1, 0)
            l.addWidget(b, 4, 0)
            l.addWidget(b1, 5, 0)

            w = QWidget()
            w.setLayout(l)

            self.setCentralWidget(w)

            self.show()

        def test(self) -> None:
            """Test"""

            r = random.randint

            self.jobInfo.setValues(
                (r(1, 1001), r(1, 1001), r(1, 1001), r(1, 1001), r(1, 1001))
            )

        def test1(self) -> None:
            """Test FormatLabel"""
            r = random.randint

            self.formatLabel[0] = r(1, 1001)
            self.formatLabel[1] = r(1, 1001)

    # pylint: disable=C0103
    # variables use to construct application not constants
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
