from __future__ import print_function
import sys
from copy import deepcopy

# kills the program when you hit Cntl+C from the command line
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from six import string_types

from qtpy import QtGui
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget, QAbstractItemView, QVBoxLayout, QPushButton, QApplication,
    QComboBox, QLabel, QHBoxLayout, QMessageBox, QGroupBox)
from gui_utils.utils.qtreeview2 import QTreeView2
from gui_utils.utils.results_window import ResultsWindow
import gui_utils.vsp_g as vsp


class Sidebar(QWidget):
    """
    +----------------------+
    |        Results       |
    +======================+
    |                      |
    |  Name = Main         |
    |                      |
    |  +----------------+  |
    |  | ResultsWindow  |  |
    |  +----------------+  |
    |  |                |  |
    |  |  +----------+  |  |
    |  |  | - a      |  |  |
    |  |  |  - b1    |  |  |
    |  |  |  - b2    |  |  |
    |  |  |  - b3    |  |  |
    |  |  +----------+  |  |
    |  |                |  |
    |  +----------------+  |
    |                      |
    |                      |
    |         Add          |
    |         Cut          |
    |         Copy         |
    |         Delete       |
    +----------------------+
    """
    def __init__(self, parent, debug=False, data=None, clear_data=True):
        """creates the buttons in the Sidebar, not the actual layout"""
        QWidget.__init__(self)
        self.parent = parent
        self.debug = debug

        name = 'main'

        choices = ['keys2', 'purse2', 'cellphone2', 'credit_card2', 'money2']
        if data is None:
            data = []

        self.result_case_window = ResultsWindow(self, 'Components', data, choices)

        data = [
            ('A', 1, []),
            #('B', 2, []),
            #('C', 3, []),
        ]
        self.result_data_window = ResultsWindow(self, 'Method', data, choices)
        self.result_data_window.setVisible(False)

        self.show_pulldown = False
        if self.show_pulldown:
            combo_options = ['a1', 'a2', 'a3']
            self.pulldown = QComboBox()
            self.pulldown.addItems(choices)
            self.pulldown.activated[str].connect(self.on_pulldown)

        #self.apply_button = QPushButton('Apply', self)
        self.add_button = QPushButton('Add', self)
        self.edit_button = QPushButton('Edit', self)
        self.copy_button = QPushButton('Copy', self)
        self.cut_button = QPushButton('Cut', self)
        self.paste_button = QPushButton('Paste', self)
        self.delete_button = QPushButton('Delete', self)
        #self.apply_button.clicked.connect(self.on_apply)

        self.name = str(name)
        self.names = [name]
        self.name_label = QLabel("Name:")
        self.name_pulldown = QComboBox()
        #names = [
            #'Pod', 'Fuselage', 'Wing', 'Stack', 'Blank',
            #'Ellipsoid', 'Body of Revolution', 'Prop',
            #'Hinge', #'Conformal',
        #]
        names = vsp.GetGeomTypes()
        for name in names:
            self.name_pulldown.addItem(name)
        #self.name_pulldown.setDisabled(True)
        #self.name_pulldown.currentIndexChanged.connect(self.on_update_name)

        self.setup_layout(clear_data=clear_data)
        self.set_connections()

    def set_connections(self):
        self.add_button.clicked.connect(self.on_add)

    def on_add(self):
        text = str(self.name_pulldown.currentText())
        self.set_enabled(True)
        self.parent.on_add_menu(text)

    def setup_layout(self, clear_data=True):
        """creates the sidebar visual layout"""
        vbox = QVBoxLayout()
        hbox_name = QHBoxLayout()
        hbox_add_edit = QHBoxLayout()

        hbox_name.addWidget(self.name_label)
        hbox_name.addWidget(self.name_pulldown)
        vbox.addLayout(hbox_name)
        vbox.addLayout(hbox_add_edit)
        vbox.addWidget(self.result_case_window)
        vbox.addWidget(self.result_data_window)
        if self.show_pulldown:
            vbox.addWidget(self.pulldown)
        #vbox.addWidget(self.apply_button)
        hbox_add_edit.addWidget(self.add_button)
        hbox_add_edit.addWidget(self.edit_button)

        group_name_clipboard = QGroupBox('Clipboard')
        clipboard_vbox = QVBoxLayout()
        clipboard_vbox.addWidget(self.copy_button)
        clipboard_vbox.addWidget(self.cut_button)
        clipboard_vbox.addWidget(self.paste_button)
        group_name_clipboard.setLayout(clipboard_vbox)

        vbox.addWidget(group_name_clipboard)
        vbox.addWidget(self.delete_button)
        self.setLayout(vbox)

        if clear_data:
            self.clear_data()

    def update_method(self, method):
        if isinstance(method, string_types):
            datai = self.result_data_window.data[0]
            self.result_data_window.data[0] = (method, datai[1], datai[2])
            #print('method=%s datai=%s' % (method, datai))
            self.result_data_window.update_data(self.result_data_window.data)
        else:
            return
             # pragma: no cover
            #datai = self.result_data_window.data[0]

    def get_form(self):
        """
        TODO: At this point, we should clear out the data block and refresh it
        """
        return self.result_case_window.data

    def update_results(self, data, name):
        """
        Updates the sidebar

        Parameters
        ----------
        data : List[tuple]
            the form data
        name : str
            the name that goes at the side
        """
        name = str(name)
        if name in self.names:
            i = self.names.index(name)
            self.name_pulldown.setCurrentIndex(i)
        else:
            self.name_pulldown.addItem(name)
            self.names.append(name)
        if len(self.names) >= 2:
            self.name_pulldown.setEnabled(True)
        self.name = name

        self.result_case_window.update_data(data)
        self.apply_button.setEnabled(True)

    def update_methods(self, data):
        """the methods is a hidden box"""
        self.result_data_window.update_data(data)
        #self.apply_button.setEnabled(True)
        #self.add_button.setEnabled(True)
        self.set_enabled(True)

    def set_enabled(self, is_enabled):
        self.edit_button.setEnabled(is_enabled)
        self.copy_button.setEnabled(is_enabled)
        self.cut_button.setEnabled(is_enabled)
        self.paste_button.setEnabled(is_enabled)
        self.delete_button.setEnabled(is_enabled)

    def clear_data(self):
        self.result_case_window.clear_data()
        self.result_data_window.clear_data()
        #self.apply_button.setEnabled(False)
        #self.add_button.setEnabled(False)
        self.set_enabled(False)

    def on_pulldown(self, event):
        print('pulldown...')

    def on_update_name(self, event):
        """user clicked the pulldown"""
        name = str(self.name_pulldown.currentText())
        data = self.parent._get_sidebar_data(name)
        #self.result_case_window.update_data(data)
        #self.result_case_window.update_data(data)
        #self.result_case_window.update_data(data)
        #self.result_case_window.update_data(data)
        #self.result_case_window.update_data(data)

    def on_apply(self, event):
        data = self.result_case_window.data
        valid_a, keys_a = self.result_case_window.treeView.get_row()

        data = self.result_data_window.data
        valid_b, keys_b = self.result_data_window.treeView.get_row()
        if valid_a and valid_b:
            if self.debug:  # pragma: no cover
                print('  rows1 = %s' % self.result_case_window.treeView.old_rows)
                print('        = %s' % str(keys_a))
                print('  rows2 = %s' % self.result_data_window.treeView.old_rows)
                print('        = %s' % str(keys_b))
            else:
                self.update_vtk_window(keys_a, keys_b)

    def update_vtk_window(self, keys_a, keys_b):
        if 0:  # pragma: no cover
            print('keys_a = %s' % str(keys_a))
            for i, key in enumerate(self.parent.case_keys):
                if key[1] == keys_a[0]:
                    break
            print('*i=%s key=%s' % (i, str(key)))
            #self.parent.update_vtk_window_by_key(i)
            result_name = key[1]
            #self.parent.cycle_results_explicit(result_name=result_name, explicit=True)
            #j = self.parent._get_icase(result_name)
            #j = i
        i = keys_a
        result_name = None
        self.parent._set_case(result_name, i, explicit=True)


def get_many_cases(data):
    """
    Get the result case ids that are a subset of the data/form list

    data = [
        (u'Element Checks', None, [
            (u'ElementDim', 5, []),
            (u'Min Edge Length', 6, []),
            (u'Min Interior Angle', 7, []),
            (u'Max Interior Angle', 8, [])],
        ),
    ]
    >>> get_many_cases(data)
    [5, 6, 7, 8]

    >>> data = [(u'Max Interior Angle', 8, [])]
    [8]
    """
    name, case, rows = data
    if case is None:
        # remove many results
        # (Geometry, None, [results...])
        cases = []
        for irow, row in enumerate(rows):
            name, row_id, data2 = row
            cases += get_many_cases(row)
    else:
        cases = [case]
    return cases

def main():  # pragma: no cover
    app = QApplication(sys.argv)

    form = [
        [u'Geometry', None, [
            (u'NodeID', 0, []),
            (u'ElementID', 1, []),
            (u'PropertyID', 2, []),
            (u'MaterialID', 3, []),
            (u'E', 4, []),
            (u'Element Checks', None, [
                (u'ElementDim', 5, []),
                (u'Min Edge Length', 6, []),
                (u'Min Interior Angle', 7, []),
                (u'Max Interior Angle', 8, [])],
             ),],
         ],
    ]
    #form = []
    res_widget = Sidebar(app, data=form, clear_data=False, debug=True)

    name = 'name'
    #res_widget.update_results(form, name)

    res_widget.show()


    sys.exit(app.exec_())

if __name__ == "__main__":  # pragma: no cover
    main()

