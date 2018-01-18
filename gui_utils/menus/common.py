from __future__ import print_function, division
from qtpy import QtCore, QtGui
from qtpy.QtGui import QFocusEvent, QFont
from qtpy.QtWidgets import QDialog, QLineEdit, QPushButton, QSlider, QColorDialog
from qtpy.QtCore import Qt

class QJumpSlider(QSlider):
    """
    Creates a Slider that jumps to the clicked position instead of
    the end, which seems like a bug.

    It of course creates a new bug, which is dragging the slider doesn't work.
    """
    def __init__(self, *args, **kwargs):
        #super(QJumpSlider, self).__init__(self, *args, **kwargs)
        QSlider.__init__(self, *args, **kwargs)
        self.is_forward_obj = False
        #self.is_backward_obj = False #  two way connection

    def mousePressEvent(self, event):
        """
        The callback that overloads QSlider.

        This takes advantage of Python 3-style integer division returning a float.
        """
        if event.button() == Qt.LeftButton:
            if self.orientation() == Qt.Vertical:
                val = self.minimum() + ((self.maximum()-self.minimum()) * (self.height() - event.y())) / self.height()
            else:
                val = self.minimum() + ((self.maximum()-self.minimum()) * event.x()) / self.width()

            if self.is_forward_obj:
                if self.dtype == str:
                    self.forward_obj.setText(str(val))
                else:
                    self.forward_obj.setValue(self.dtype(val))
                #self.forward_obj.setValue(val)

            #self.setValue(int(round(val)))
            self.setValue(int(round(val)))
            event.accept()
        super(QSlider, self).mousePressEvent(event)

    def set_forward_connection(self, forward_obj, dtype=str):
        """connects to a QLineEdit"""
        self.is_forward_obj = True
        #if isinstance(forward_obj, QLineEdit):
            #self.dtype = str
        #else:
        self.forward_obj = forward_obj
        self.dtype = dtype

class QPushButtonColor(QPushButton):
    """Creates a QPushButton with a face color"""
    def __init__(self, rgb_color_ints, title, parent):
        QPushButton.__init__(self)
        self.title = title
        self.parent = parent
        self.rgb_color_ints = rgb_color_ints

        qcolor = QtGui.QColor()
        #self.color_edit.setFlat(True)
        qcolor.setRgb(*self.rgb_color_ints)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor('red'))
        self.setPalette(palette)
        self.setStyleSheet(
            "QPushButton {"
            "background-color: rgb(%s, %s, %s);" % tuple(self.rgb_color_ints) +
            #"border:1px solid rgb(255, 170, 255); "
            "}")
        self.clicked.connect(self.on_color)

    def on_color(self):
        """pops a color dialog"""
        #rgb_color_ints, title
        color = QColorDialog.getColor(
            QtGui.QColor(*self.rgb_color_ints), self.parent, self.title)
        if not color.isValid():
            return False, self.rgb_color_ints, None

        color_float = color.getRgbF()[:3]  # floats
        color_int = [int(colori * 255) for colori in color_float]

        assert isinstance(color_float[0], float), color_float
        assert isinstance(color_int[0], int), color_int

        self.setStyleSheet(
            "QPushButton {"
            "background-color: rgb(%s, %s, %s);" % tuple(color_int) +
            #"border:1px solid rgb(255, 170, 255); "
            "}")
        self.rgb_color_ints = color_int

    def get_rgb_ints(self):
        """Gets the RGB values as a list of ints."""
        return self.rgb_color_ints

    def get_rgb_floats(self):
        """Gets the RGB values as a list of floats."""
        color_float = [int(colori / 255) for colori in self.get_rgb_ints()]
        return self.rgb_color_ints


class PyDialog(QDialog):
    """
    common class for QDialog so value checking & escape/close code
    is not repeated
    """
    def __init__(self, data, win_parent):
        QDialog.__init__(self, win_parent)
        self.out_data = data
        self.win_parent = win_parent
        self.font_size = None

    def set_font_size(self, font_size):
        """
        Updates the font size of all objects in the PyDialog

        Parameters
        ----------
        font_size : int
            the font size
        """
        if self.font_size == font_size:
            return
        self.font_size = font_size
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)

    def closeEvent(self, event):
        self.out_data['close'] = True
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.on_cancel()

    @staticmethod
    def check_int(cell):
        text = cell.text()
        try:
            value = int(text)
            cell.setStyleSheet("QLineEdit{background: white;}")
            return value, True
        except ValueError:
            cell.setStyleSheet("QLineEdit{background: red;}")
            return None, False

    @staticmethod
    def check_positive_int_or_blank(cell):
        text = str(cell.text()).strip()
        if len(text) == 0:
            return None, True
        try:
            value = int(text)
        except ValueError:
            cell.setStyleSheet("QLineEdit{background: red;}")
            return None, False

        if value < 1:
            cell.setStyleSheet("QLineEdit{background: red;}")
            return None, False

        cell.setStyleSheet("QLineEdit{background: white;}")
        return value, True

    @staticmethod
    def check_float(cell):
        text = cell.text()
        try:
            value = float(text)
            cell.setStyleSheet("QLineEdit{background: white;}")
            return value, True
        except ValueError:
            cell.setStyleSheet("QLineEdit{background: red;}")
            return None, False

    @staticmethod
    def check_format(cell):
        text = str(cell.text())

        is_valid = True
        if len(text) < 2:
            is_valid = False
        elif 's' in text.lower():
            is_valid = False
        elif '%' not in text[0]:
            is_valid = False
        elif text[-1].lower() not in ['g', 'f', 'i', 'e']:
            is_valid = False

        try:
            text % 1
            text % .2
            text % 1e3
            text % -5.
            text % -5
        except ValueError:
            is_valid = False

        try:
            text % 's'
            is_valid = False
        except TypeError:
            pass

        if is_valid:
            cell.setStyleSheet("QLineEdit{background: white;}")
            return text, True
        else:
            cell.setStyleSheet("QLineEdit{background: red;}")
            return None, False
