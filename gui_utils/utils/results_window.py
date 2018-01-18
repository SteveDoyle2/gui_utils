from __future__ import print_function
#import sys
#from copy import deepcopy

# kills the program when you hit Cntl+C from the command line
#import signal
#signal.signal(signal.SIGINT, signal.SIG_DFL)

from qtpy import QtGui
#from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget, QVBoxLayout, QAbstractItemView,
    #QPushButton, QApplication,
    #QComboBox, QLabel, QHBoxLayout, QMessageBox
)
from gui_utils.utils.qtreeview2 import QTreeView2

class ResultsWindow(QWidget):
    """
    A ResultsWindow creates the box where we actually select our
    results case.  It does not have an apply button.
    """
    def __init__(self, parent, name, data, choices):
        QWidget.__init__(self)
        self.name = name
        self.data = data
        self.choices = choices
        self.parent = parent
        self.treeView = QTreeView2(self, self.data, choices)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.model = QtGui.QStandardItemModel()
        is_single = self.addItems(self.model, data)
        self.treeView.setModel(self.model)
        self.treeView.set_single(is_single)

        self.model.setHorizontalHeaderLabels([self.tr(self.name)])

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)

    def update_data(self, data):
        self.clear_data()
        self.data = data
        try:
            self.addItems(self.model, data)
        except:
            raise RuntimeError('cannot add data=\n%s' % data)
            #if isinstance(data, string_types):
                #self.addItems(self.model, data)
            #else:
                #self.addItems(self.model, *tuple(data))
        self.treeView.data = data
        #layout = QVBoxLayout()
        #layout.addWidget(self.treeView)
        #self.setLayout(layout)

    def clear_data(self):
        self.model.clear()
        self.treeView.data = []
        self.model.setHorizontalHeaderLabels([self.tr(self.name)])

    def addItems(self, parent, elements, level=0, count_check=False):
        nelements = len(elements)
        redo = False
        #print(elements[0])
        try:
            #if len(elements):
                #assert len(elements[0]) == 3, 'len=%s elements[0]=%s\nelements=\n%s\n' % (
                    #len(elements[0]), elements[0], elements)
            for element in elements:
                #if isinstance(element, str):
                    #print('elements = %r' % str(elements))

                #print('element = %r' % str(element))
                if not len(element) == 3:
                    print('element = %r' % str(element))
                text, i, children = element
                nchildren = len(children)
                #print('text=%r' % text)
                item = QtGui.QStandardItem(text)
                parent.appendRow(item)

                # TODO: count_check and ???
                if nelements == 1 and nchildren == 0 and level == 0:
                    #self.result_data_window.setEnabled(False)
                    item.setEnabled(False)
                    #print(dir(self.treeView))
                    #self.treeView.setCurrentItem(self, 0)
                    #item.mousePressEvent(None)
                    redo = True
                #else:
                    #pass
                    #print('item=%s count_check=%s nelements=%s nchildren=%s' % (
                        #text, count_check, nelements, nchildren))
                if children:
                    assert isinstance(children, list), children
                    self.addItems(item, children, level + 1, count_check=count_check)
            is_single = redo
            return is_single
        except ValueError:
            print()
            print('elements =', elements)
            print('element =', element)
            print('len(elements)=%s' % len(elements))
            for e in elements:
                print('  e = %s' % str(e))
            raise
        #if redo:
        #    data = [
        #        ('A', []),
        #        ('B', []),
        #    ]
        #    self.update_data(data)
