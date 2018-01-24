from __future__ import print_function, division
from qtpy import QtCore, QtGui
from qtpy.QtGui import QFocusEvent, QFont
from qtpy.QtWidgets import QDialog, QLineEdit, QPushButton, QColorDialog
from qtpy.QtCore import Qt


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


