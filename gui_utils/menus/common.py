from __future__ import print_function, division
from qtpy import QtCore, QtGui
from qtpy.QtGui import QFocusEvent, QFont
from qtpy.QtWidgets import QDialog, QLineEdit, QPushButton, QColorDialog
from qtpy.QtCore import Qt


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
