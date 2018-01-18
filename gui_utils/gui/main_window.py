"""
defines the MainWindow class
"""
# coding: utf-8
# pylint: disable=C0111
from __future__ import division, unicode_literals, print_function

# standard library
import sys
import os.path
#import traceback
#import webbrowser
#webbrowser.open("http://xkcd.com/353/")

#from six import string_types, iteritems
from six.moves import range


from pyNastran.gui.qt_version import qt_version
from qtpy import QtCore
from qtpy.QtWidgets import QMessageBox, qApp

# 3rd party
import vtk

import gui_utils
import pyNastran
#from pyNastran.gui.gui_utils.utils import check_for_newer_version


# pyNastran
#from pyNastran.utils import print_bad_path
from pyNastran.gui.formats import (
    Cart3dIO, STL_IO,
)
from gui_utils.gui.gui_common import GuiCommon2
from gui_utils.menus.wing_menu import WingWindow

try:
    pkg_path = sys._MEIPASS #@UndefinedVariable
    script_path = os.path.join(pkg_path, 'scripts')
    icon_path = os.path.join(pkg_path, 'icons')
except:
    pkg_path = pyNastran.__path__[0]
    script_path = os.path.join(pkg_path, 'gui', 'scripts')
    icon_path = os.path.join(pkg_path, 'gui', 'icons')


class MainWindow(GuiCommon2, Cart3dIO, STL_IO,):
    """
    MainWindow -> GuiCommon2 -> GuiCommon
    gui.py     -> gui_common -> gui_qt_common
    """
    def __init__(self, inputs, **kwds):
        """
        inputs=None
        """
        html_logging = True
        fmt_order = [
            # results
            'cart3d',

            # no results
            'stl',
        ]
        kwds['inputs'] = inputs
        kwds['fmt_order'] = fmt_order
        kwds['html_logging'] = html_logging
        super(MainWindow, self).__init__(**kwds)
        #fmt_order=fmt_order, inputs=inputs,
        #html_logging=html_logging,

        if qt_version in [4, 5]:
            Cart3dIO.__init__(self)
            STL_IO.__init__(self)

        self.build_fmts(fmt_order, stop_on_failure=False)

        logo = os.path.join(icon_path, 'logo.png')
        self.logo = logo
        self.set_script_path(script_path)
        self.set_icon_path(icon_path)

        self.setup_gui()
        self.setup_post(inputs)

        #self._check_for_latest_version(inputs['no_update'])

    def _check_for_latest_version(self, check=True):
        """
        checks the website for information regarding the latest gui version

        Looks for:
            ## pyNastran v0.7.2 has been Released (4/25/2015)
        """
        import time
        time0 = time.time()
        version_latest, version_current, is_newer = check_for_newer_version()
        if is_newer:
            url = pyNastran.__website__
            from pyNastran.gui.menus.download import DownloadWindow
            win = DownloadWindow(url, version_latest, win_parent=self)
            win.show()
        dt = time.time() - time0
        #print('dt_version_check = %.2f' % dt)

    def mousePressEvent(self, ev):
        if not self.run_vtk:
            return
        #print('press x,y = (%s, %s)' % (ev.x(), ev.y()))
        if self.is_pick:
            #self.___saveX = ev.x()
            #self.___saveY = ev.y()
            pass
        else:
            self.iren.mousePressEvent(ev)

    #def LeftButtonPressEvent(self, ev):

    def mouseReleaseEvent(self, ev):
        #print('release x,y = (%s, %s)' % (ev.x(), ev.y()))
        if self.is_pick:
            pass
        else:
            self.iren.mousePressEvent(ev)

    def about_dialog(self):
        """ Display about dialog """
        copyright = gui_utils.__copyright__
        if qt_version == 'pyside':
            word = 'PySide'
            copyright_qt = gui_utils.__pyside_copyright__
        else:
            word = 'PyQt'
            copyright_qt = gui_utils.__pyqt_copyright__

        about = [
            'pyNastran %s GUI' % word,
            '',
            'pyNastran v%s' % gui_utils.__version__,
            copyright,
            copyright_qt,
            gui_utils.__author__,
            '',
            '%s' % gui_utils.__website__,
            '',
            'Mouse',
            'Left Click - Rotate',
            'Middle Click - Pan/Recenter Rotation Point',
            'Shift + Left Click - Pan/Recenter Rotation Point',
            'Right Mouse / Wheel - Zoom',
            '',
            'Keyboard Controls',
            #'r   - reset camera view',
            #'X/x - snap to x axis',
            #'Y/y - snap to y axis',
            #'Z/z - snap to z axis',
            #'',
            #'h   - show/hide legend & info',
            'CTRL+I - take a screenshot (image)',
            'CTRL+L - cycle the results forwards',
            'CTRL+K - cycle the results backwards',
            #'m/M    - scale up/scale down by 1.1 times',
            #'o/O    - rotate counter-clockwise/clockwise 5 degrees',
            'p      - pick node/element',
            's      - view model as a surface',
            'w      - view model as a wireframe',
            'f      - set rotation center (zoom out when picking',
            '         to disable clipping)',
            'e      - view model edges',
            'b      - change edge color from scalar/black',
            '',
            'Reload Model:  using the same filename, reload the model',
        ]

        #message_box = QMessageBox()
        #message_box.setStyleSheet(
            #'QMessageBox {background-color: #2b5b84; color: white;}\n'
            #'QPushButton{color: white; font-size: 16px; background-color: #1d1d1d; '
            #'border-radius: 10px; padding: 10px; text-align: center;}\n'
            #' QPushButton:hover{color: #2b5b84;}')
        #message_box.setFont(self.font())
        QMessageBox.about(self, "About pyNastran GUI", "\n".join(about))

    def closeEvent(self, event):
        """
        Handling saving state before application when application is
        being closed.
        """
        settings = QtCore.QSettings()
        settings.clear()
        self.settings.save(settings)
        qApp.quit()
