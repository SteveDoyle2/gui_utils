from __future__ import print_function
#import sys
#from copy import deepcopy

# kills the program when you hit Cntl+C from the command line
#import signal
#signal.signal(signal.SIGINT, signal.SIG_DFL)

from six import string_types

from qtpy import QtGui
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QTreeView, QMessageBox, QMenu


class QTreeView2(QTreeView):
    """
    creates a QTreeView with:
     - a nice-ish way to extract the location in the tree
     - key press delete support
    """
    def __init__(self, parent, data, choices):
        self.parent = parent
        self.old_rows = []
        self.data = data
        self.cases_deleted = set([])
        self.choices = choices
        self.single = False
        QTreeView.__init__(self)
        #self.setAlternatingRowColors(True)

    def keyPressEvent(self, event): #Reimplement the event here, in your case, do nothing
        #if event.key() == QtCore.Qt.Key_Escape:
            #self.close()
        #return
        key = event.key()
        if key == Qt.Key_Delete:
            self.on_delete()
        else:
            QTreeView.keyPressEvent(self, event)

    def remove_rows(self, rows):
        """
        We just hide the row to delete things to prevent refreshing
        the window and changing which items have been expanded

        Parameters
        ----------
        rows : List[int]
            the trace on the data/form block

        form = [
            ['Geometry', None, [
                ('NodeID', 0, []),
                ('ElementID', 1, []),
                ('PropertyID', 2, []),
                ('MaterialID', 3, []),
                ('E', 4, []),
                ('Element Checks', None, [
                    ('ElementDim', 5, []),
                    ('Min Edge Length', 6, []),
                    ('Min Interior Angle', 7, []),
                    ('Max Interior Angle', 8, [])],
                 ),],
             ],
        ]

        # delete Geometry
        data[0] = ('Geometry', None, [...])
        >>> remove_rows([0])

        # delete MaterialID
        data[0][3] = ('MaterialID', 3, [])
        >>> remove_rows([0, 3])

        # delete ElementChecks
        data[0][5] = ('Element Checks', None, [...])
        >>> remove_rows([0, 5])

        # delete Min Edge Length
        data[0][5][1] = ('Min Edge Length', 6, [])
        >>> remove_rows([0, 5, 1])
        """
        # find the row the user wants to delete
        data = self.data
        for row in rows[:-1]:
            data = data[row][2]

        # we got our data block
        # now we need to get 1+ results
        last_row = rows[-1]
        cases_to_delete = get_many_cases(data[last_row])

        cases_to_delete = list(set(cases_to_delete) - self.cases_deleted)
        cases_to_delete.sort()
        if len(cases_to_delete) == 0: # can this happen?
            # this happens when you cleared out a data block by
            # deleting to entries, but not the parent
            #
            # we'll just hide the row now
            msg = ''
            return
        elif len(cases_to_delete) == 1:
            msg = 'Are you sure you want to delete 1 result case load_case=%s' % cases_to_delete[0]
        else:
            msg = 'Are you sure you want to delete %s result cases %s' % (
                len(cases_to_delete), str(cases_to_delete))

        if msg:
            widget = QMessageBox()
            title = 'Delete Cases'
            result = QMessageBox.question(widget, title, msg,
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if result != QMessageBox.Yes:
                return

            self.cases_deleted.update(set(cases_to_delete))
            self.on_delete_parent_cases(cases_to_delete)

        # hide the line the user wants to delete
        row = rows[-1]
        indexes = self.selectedIndexes()
        self.setRowHidden(row, indexes[-1].parent(), True)
        self.update()

    def on_delete_parent_cases(self, cases_to_delete):
        """delete cases from the parent"""
        sidebar = self.parent.parent
        if hasattr(sidebar.parent, 'delete_cases'):
            gui = sidebar.parent
            gui.delete_cases(cases_to_delete, ask=False)

    def find_list_index(self):
        """trace the tree to find the selected item"""
        indexes = self.selectedIndexes()

        rows = []
        for index in indexes:
            row = index.row()
            rows.append(row)
            level = 0
            while index.parent().isValid():
                index = index.parent()
                row = index.row()
                rows.append(row)
                level += 1
        rows.reverse()
        return rows

    def mousePressEvent(self, event):
        """called when you click a result"""
        QTreeView.mousePressEvent(self, event)
        if event.button() == Qt.LeftButton:
            self.on_left_mouse_button()
        elif event.button() == Qt.RightButton:
            self.on_right_mouse_button()
        else:
            print('dunno???')

    def on_left_mouse_button(self):
        # trace the tree to find the selected item
        rows = self.find_list_index()

        # TODO: what is this for???
        if rows != self.old_rows:
            self.old_rows = rows
        valid, keys = self.get_row()
        if not valid:
            print('invalid=%s keys=%s' % (valid, keys))
        else:
            print('valid=%s keys=%s' % (valid, keys))
            #print('choice =', self.choices[keys])

    def on_right_mouse_button(self):
        pass

    def on_delete(self):
        """interface for deleting rows"""
        rows = self.find_list_index()
        self.remove_rows(rows)
        #self.model().removeRow(row)
        #self.parent().on_delete(index.row())

        #del self.data[row]
        #self.model().change_data(self.data)

    def get_row(self):
        """
        gets the row

        Returns
        -------
        is_valid : bool
            is this case valid
        row : None or tuple
            None : invalid case
            tuple : valid case
                ('centroid', None, [])
                0 - the location (e.g. node, centroid)
                1 - iCase
                2 - []
        """
        # if there's only 1 data member, we don't need to extract the data id
        if self.single:
            return True, self.data[0]

        irow = 0

        # TODO: what is this for???
        #     crashes some PyQt4 cases when clicking on the first
        #     non-results level of the sidebar
        #data = deepcopy(self.data)
        data = self.data
        for row in self.old_rows:
            try:
                key = data[row][0]
            except IndexError:
                return False, irow
            irow = data[row][1]
            data = data[row][2]

        if data:
            return False, None
        return True, irow

    def set_single(self, single):
        self.single = single
        self.old_rows = [0]


class RightClickTreeView(QTreeView2):
    """
    creates a QTreeView with:
     - all the features of QTreeView2
     - a right click context menu with:
       - Edit - TODO
       - Cut - TODO
       - Copy - TODO
       - Rename - TODO
       - Delete
    """
    def __init__(self, parent, data, choices):
        QTreeView2.__init__(self, parent, data, choices)

        self.right_click_menu = QMenu()
        edit = self.right_click_menu.addAction("Edit...")
        cut = self.right_click_menu.addAction("Cut...")
        copy = self.right_click_menu.addAction("Copy...")
        paste = self.right_click_menu.addAction("Paste...")
        rename = self.right_click_menu.addAction("Rename...")
        delete = self.right_click_menu.addAction("Delete...")

        edit.triggered.connect(self.on_edit)
        cut.triggered.connect(self.on_cut)
        copy.triggered.connect(self.on_copy)
        paste.triggered.connect(self.on_paste)
        rename.triggered.connect(self.on_rename)
        delete.triggered.connect(self.on_delete)

    def on_edit(self):
        rows = self.find_list_index()
        print('edit...rows=%s' % rows)
    def on_cut(self):
        pass
    def on_copy(self):
        pass
    def on_paste(self):
        pass
    def on_rename(self):
        rows = self.find_list_index()
        list_data = self.data
        for row in rows[:-1]:
            list_datai = list_data[row]
            list_data = list_datai[2]

        list_datai = list_data[rows[-1]]
        list_data = list_datai[0]
        print('list_datai* = ', list_datai)
        #print('list_data2* = %r' % list_data)
        list_datai[0] = 'cat'
        self.parent.update_data(self.data)
        #self.update()

    #def on_delete(self):
        #pass

    def on_right_mouse_button(self):
        self.right_click_menu.popup(QtGui.QCursor.pos())



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


#for subcase in subcases:
#    for time in times:
#        disp
#        stress
#        load
