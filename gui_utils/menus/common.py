from __future__ import print_function

from qtpy import QtCore, QtGui
from qtpy.QtGui import QFocusEvent, QFont
from qtpy.QtWidgets import QDialog, QLineEdit, QPushButton

class QPushButtonColor(QPushButton):
    """Creates a QPushButton with a face color"""
    def __init__(self, labelcolor_int):
        QPushButton.__init__(self)

        qcolor = QtGui.QColor()
        #self.color_edit.setFlat(True)
        qcolor.setRgb(*labelcolor_int)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor('blue'))
        self.setPalette(palette)
        self.setStyleSheet(
            "QPushButton {"
            "background-color: rgb(%s, %s, %s);" % tuple(labelcolor_int) +
            #"border:1px solid rgb(255, 170, 255); "
            "}")


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
