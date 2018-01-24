"""
per https://stackoverflow.com/questions/11132597/qslider-mouse-direct-jump
"""
from __future__ import print_function, division
from qtpy import QtCore, QtGui
from qtpy.QtWidgets import QSlider, QStyle
from qtpy.QtCore import Qt


class QJumpSlider(QSlider):
    """
    Creates a Slider that jumps to the clicked position instead of
    the end, which seems like a bug.
    """
    def __init__(self, *args, **kwargs):
        #super(QJumpSlider, self).__init__(self, *args, **kwargs)
        QSlider.__init__(self, *args, **kwargs)
        self.is_forward_obj = False
        #self.is_backward_obj = False #  two way connection
        self.debug = False
        self.dtype = None
        self.forward_obj = None

    def mousePressEvent(self, event):
        """Jump to click position"""
        minimum = self.minimum()
        maximum = self.maximum()
        if self.orientation() == Qt.Vertical:
            y = event.y()
            height = self.height()
            vala = QStyle.sliderValueFromPosition(minimum, maximum, y, height)
            val = minimum + ((maximum - minimum + 1) * (height - y)) / height
        else:
            x = event.x()
            width = self.width()
            vala = QStyle.sliderValueFromPosition(minimum, maximum, x, width)
            val = minimum + ((maximum - minimum + 1) * x) / width
        self.setValue(val)
        self._propogate_forward(val)

    def mouseMoveEvent(self, event):
        """Jump to pointer position while moving"""
        minimum = self.minimum()
        maximum = self.maximum()

        if self.orientation() == Qt.Vertical:
            y = event.y()
            height = self.height()
            self.setValue(QStyle.sliderValueFromPosition(minimum, maximum, y, height))
            val = minimum + ((maximum - minimum) * (height - y)) / height
        else:
            x = event.x()
            width = self.width()
            self.setValue(QStyle.sliderValueFromPosition(minimum, maximum, x, width))
            val = minimum + ((maximum - minimum) * x) / width

        self._propogate_forward(val)

    def _propogate_forward(self, val):
        """send the value to a text box"""
        if val > self.maximum():
            val = self.maximum()
        elif val < self.minimum():
            val = self.minimum()

        if self.is_forward_obj:
            val_set = self.dtype(val)
            if isinstance(val_set, str):
                self.forward_obj.setText(val_set)
            else:
                self.forward_obj.setValue(val_set)
        if self.debug:
            print(val)

    def set_forward_connection(self, forward_obj, dtype=str):
        """
        Connects to a secondary object (e.g., QLineEdit, QSpinner)

        Parameters
        ----------
        forward_obj : QLineEdit, QSpinner
            QLineEdit : dtype must be str
            QSpinner : dtype must be int
            etc.
        dtype : type/function
            the type of the value going into forward_obj
            str, int, float

        Example
        -------
        **QLineEdit example**
        >>> slider = QJumpSlider()
        >>> line_edit = QLineEdit()
        >>> slider.set_forward_connection(line_edit, str)

        **QLineEdit example with rounding**
        >>> slider = QJumpSlider()
        >>> line_edit = QLineEdit()
        >>> def round_val(val):
        >>>     return str(round(val, 3))
        >>> slider.set_forward_connection(line_edit, round_val)

        **QSpinner example**
        >>> slider = QJumpSlider()
        >>> spinner = QSpinner()
        >>> slider.set_forward_connection(spinner, int)
        """
        self.is_forward_obj = True
        #if isinstance(forward_obj, QLineEdit):
            #self.dtype = str
        #else:
        self.forward_obj = forward_obj
        self.dtype = dtype


if __name__ == "__main__":
    import sys

    # kills the program when you hit Cntl+C from the command line
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from qtpy.QtWidgets import QApplication
    def echo(value):
        print(value)
    app = QApplication(sys.argv)
    slider = QJumpSlider(Qt.Horizontal)
    slider.setMinimum(1)
    slider.setMaximum(11)
    #slider.setLow(0)
    #slider.setHigh(10000)
    slider.setTickPosition(QSlider.TicksBelow)
    #slider.connect(QtCore.SIGNAL('sliderMoved(int)'), echo)
    slider.sliderMoved.connect(echo)
    slider.show()
    slider.raise_()
    app.exec_()
