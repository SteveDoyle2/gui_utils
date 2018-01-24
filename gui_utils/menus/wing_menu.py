"""
defines:
 - WingWindow
"""
from __future__ import print_function
#import os

from qtpy import QtCore
from qtpy.QtGui import QFont
from qtpy.QtWidgets import (
    QApplication, QLabel, QPushButton, QLineEdit, QComboBox, QWidget, QRadioButton,
    QButtonGroup, QGridLayout, QHBoxLayout, QVBoxLayout, QSlider, QCheckBox,
    QSpinBox, QGroupBox, QTabWidget)

from gui_utils.menus.common import PyDialog
from gui_utils.utils.qpush_button_color import QPushButtonColor
from gui_utils.utils.qjump_slider import QJumpSlider

from pyNastran.gui.qt_version import qt_version


class WingWindow(PyDialog):
    """
    +-------------------+
    | Legend Properties |
    +-----------------------+
    | Title  ______ Default |
    | Min    ______ Default |
    | Max    ______ Default |
    | Format ______ Default |
    | Scale  ______ Default |
    | Phase  ______ Default |
    | Number of Colors ____ |
    | Number of Labels ____ |
    | Label Size       ____ | (TODO)
    | ColorMap         ____ | (TODO)
    |                       |
    | x Min/Max (Blue->Red) |
    | o Max/Min (Red->Blue) |
    |                       |
    | x Vertical/Horizontal |
    | x Show/Hide           |
    |                       |
    |        Animate        |
    |    Apply OK Cancel    |
    +-----------------------+
    """
    colormap_keys = ['metal', 'gold', 'grey']
    def __init__(self, data, win_parent=None):
        PyDialog.__init__(self, data, win_parent)

        self._updated_legend = False
        self._animation_window_shown = False

        #self._icase = data['icase']
        #self._default_icase = self._icase
        self._default_name = data['name']
        self._color_int = data['color']


        #self.setupUi(self)
        self.setWindowTitle('Wing')
        self.create_widgets()
        self.create_layout()
        #self.set_connections()
        self.set_font_size(data['font_size'])
        self.symmetry = data['symmetry']
        self.transform = data['transform']

    def create_widgets(self):
        """creates the menu objects"""
        self.create_general_widgets()
        self.create_xform_widgets()

    def create_general_widgets(self):
        """creates the menu objects"""
        # --------------------------------------------------------------
        # Name
        self.name = QLabel("Name:")
        self.name_edit = QLineEdit(str(self._default_name))

        self.colormap = QLabel("Color:")
        self.colormap_edit = QPushButtonColor(self._color_int, 'Select a color', parent=self)
        self.colormap_button = QPushButton("Advanced")
        self.colormap_button.setEnabled(False)

        # --------------------------------------------------------------
        # TODO: the way these sliders work is they have some defined range
        #       if you go outside the range, they "reset" to 50% and
        #       are redefined from value-delta to value+delta, where
        #       delta=nominal/2
        num_u = 5
        num_w = 10
        self.tesselation_u = QLabel("Num_U")
        self.tesselation_u_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.tesselation_u_edit.setTickPosition(QSlider.TicksBelow)
        self.tesselation_u_edit.setRange(1, 10)
        self.tesselation_u_edit.setValue(num_u)
        self.tesselation_u_button = QLineEdit('')

        def int_func(val):
            return str(int(val))
        self.tesselation_u_edit.set_forward_connection(self.tesselation_u_button, int_func)

        self.tesselation_w = QLabel("Num_W")
        self.tesselation_w_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.tesselation_w_edit.setTickPosition(QSlider.TicksBelow)
        self.tesselation_w_edit.setRange(1, 10)
        self.tesselation_w_edit.setValue(num_w)
        self.tesselation_w_button = QLineEdit('')
        # --------------------------------------------------------------

        density = 1.0
        self.density = QLabel("Density")
        self.density_edit = QLineEdit(str(density))
        self.density_button = QCheckBox('Thin Shell')

        priority = 3
        priority_max = 50
        self.priority = QLabel('Priority')
        msg = (
            'Components compete for volume during the mass properties.\n'
            'A lower priority (e.g., 0) takes precendence.  Additionally, \n'
            'when combined with a density of 0.0, this can be used to \n'
            'create voids (empty regions).'
        )
        self.priority.setToolTip(msg)
        self.priority_edit = QSpinBox(self)
        self.priority_edit.setRange(0, priority_max)
        self.priority_edit.setSingleStep(1)
        self.priority_edit.setValue(priority)

        # --------------------------------------------------------------
        self.negative_volume_button = QCheckBox('Negative Volume')
        # --------------------------------------------------------------

        #for key in self.colormap_keys:
            #self.colormap_edit.addItem(key)

        #self._colormap = 'grey'
        #self.colormap_edit.setCurrentIndex(self.colormap_keys.index(self._colormap))

        # --------------------------------------------------------------
        # the header
        self.grid2_title = QLabel("Color Scale:")

        # on / off
        self.show_radio = QRadioButton("Show")
        self.hide_radio = QRadioButton("Hide")
        widget = QWidget(self)
        show_hide_group = QButtonGroup(widget)

        # --------------------------------------------------------------

        # closing
        self.apply_button = QPushButton("Apply")
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

    def create_xform_widgets(self):
        xloc = 0.0
        yloc = 0.0
        zloc = 0.0

        xrot = 0.0
        yrot = 0.0
        zrot = 0.0
        rot_origin_angle = 0.0

        self.xloc = QLabel("X Loc")
        self.xloc_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.xloc_button = QLineEdit(str(xloc))
        self.xloc_edit.set_forward_connection(self.xloc_button, float_func)
        #self.xloc_edit.setTickPosition(QSlider.TicksBelow)
        self.xloc_edit.setRange(1, 10)
        self.xloc_edit.setValue(xloc)

        self.yloc = QLabel("Y Loc")
        self.yloc_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.yloc_button = QLineEdit(str(yloc))
        self.yloc_edit.set_forward_connection(self.yloc_button, float_func)
        #self.yloc_edit.setTickPosition(QSlider.TicksBelow)
        self.yloc_edit.setRange(1, 10)
        self.yloc_edit.setValue(yloc)

        self.zloc = QLabel("Z Loc")
        self.zloc_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.zloc_button = QLineEdit(str(zloc))
        self.zloc_edit.set_forward_connection(self.zloc_button, float_func)

        #self.zloc_edit.setTickPosition(QSlider.TicksBelow)
        self.zloc_edit.setRange(1, 10)
        self.zloc_edit.setValue(zloc)

        self.xrot = QLabel("X Rot")
        self.xrot_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.xrot_button = QLineEdit(str(xrot))
        self.xrot_edit.set_forward_connection(self.xrot_button, float_func)
        #self.xrot_edit.setTickPosition(QSlider.TicksBelow)
        self.xrot_edit.setRange(1, 10)
        self.xrot_edit.setValue(xrot)

        self.yrot = QLabel("Y Rot")
        self.yrot_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.yrot_button = QLineEdit(str(yrot))
        self.yrot_edit.set_forward_connection(self.yrot_button, float_func)
        #self.yrot_edit.setTickPosition(QSlider.TicksBelow)
        self.yrot_edit.setRange(1, 10)
        self.yrot_edit.setValue(yrot)

        self.zrot = QLabel("Z Rot")
        self.zrot_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.zrot_button = QLineEdit(str(zrot))
        self.zrot_edit.set_forward_connection(self.zrot_button, float_func)
        #self.zrot_edit.setTickPosition(QSlider.TicksBelow)
        self.zrot_edit.setRange(1, 10)
        self.zrot_edit.setValue(zrot)

        self.rot_origin = QLabel("Rot Origin (X)")
        self.rot_origin_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.rot_origin_button = QLineEdit(str(rot_origin_angle))
        self.rot_origin_edit.set_forward_connection(self.rot_origin_button, float_func)
        #self.rot_origin_edit.setTickPosition(QSlider.TicksBelow)
        self.rot_origin_edit.setRange(1, 10)
        self.rot_origin_edit.setValue(rot_origin_angle)

    def create_geom_layout(self):
        group_name_color = QGroupBox('Name and Color')
        group_tesselation = QGroupBox('Tesselation')
        group_mass_properties = QGroupBox('Mass Properties')
        group_cfd_mesh = QGroupBox('CFD Mesh')

        grid_name_color = QGridLayout()
        grid_name_color.addWidget(self.name, 0, 0)
        grid_name_color.addWidget(self.name_edit, 0, 1)

        grid_name_color.addWidget(self.colormap, 1, 0)
        grid_name_color.addWidget(self.colormap_edit, 1, 1)
        grid_name_color.addWidget(self.colormap_button, 1, 2)
        group_name_color.setLayout(grid_name_color)

        #--------------------------------------------------------
        grid_tesselation = QGridLayout()
        grid_tesselation.addWidget(self.tesselation_u, 2, 0)
        grid_tesselation.addWidget(self.tesselation_u_edit, 2, 1)
        grid_tesselation.addWidget(self.tesselation_u_button, 2, 2)

        grid_tesselation.addWidget(self.tesselation_w, 3, 0)
        grid_tesselation.addWidget(self.tesselation_w_edit, 3, 1)
        grid_tesselation.addWidget(self.tesselation_w_button, 3, 2)
        group_tesselation.setLayout(grid_tesselation)

        #--------------------------------------------------------
        grid_mass_properties = QGridLayout()
        grid_mass_properties.addWidget(self.density, 4, 0)
        grid_mass_properties.addWidget(self.density_edit, 4, 1)
        grid_mass_properties.addWidget(self.density_button, 4, 2)

        grid_mass_properties.addWidget(self.priority, 5, 0)
        grid_mass_properties.addWidget(self.priority_edit, 5, 1)
        group_mass_properties.setLayout(grid_mass_properties)
        #--------------------------------------------------------
        grid_cfd_mesh = QGridLayout()
        grid_cfd_mesh.addWidget(self.negative_volume_button, 1, 0)
        group_cfd_mesh.setLayout(grid_cfd_mesh)

        #--------------------------------------------------------
        # footer
        ok_cancel_box = QHBoxLayout()
        ok_cancel_box.addWidget(self.apply_button)
        ok_cancel_box.addWidget(self.ok_button)
        ok_cancel_box.addWidget(self.cancel_button)


        grid2 = QGridLayout()
        grid2.addWidget(self.grid2_title, 0, 0)
        #grid2.addWidget(self.low_to_high_radio, 1, 0)
        #grid2.addWidget(self.high_to_low_radio, 2, 0)

        #grid2.addWidget(self.vertical_radio, 1, 1)
        #grid2.addWidget(self.horizontal_radio, 2, 1)

        grid2.addWidget(self.show_radio, 1, 2)
        grid2.addWidget(self.hide_radio, 2, 2)

        vbox = QVBoxLayout()
        vbox.addWidget(group_name_color)
        vbox.addWidget(group_tesselation)
        vbox.addWidget(group_mass_properties)
        vbox.addWidget(group_cfd_mesh)
        #vbox.addLayout(checkboxes)
        #vbox.addLayout(grid2)
        vbox.addStretch()
        vbox.addLayout(ok_cancel_box)
        #--------------------------------------------------------
        tab1 = QWidget()
        tab1.setLayout(vbox)
        return tab1

    def create_xform_layout(self):
        group_transforms = QGroupBox('Transforms')
        group_symmetry = QGroupBox('Symmetry')
        group_scale_factor = QGroupBox('Scale Factor')
        group_attach_to_parent = QGroupBox('Attach To Parent')
        #--------------------------------------------------------
        grid_location = QGridLayout()

        grid_location.addWidget(self.xloc, 0, 0)
        grid_location.addWidget(self.xloc_edit, 0, 1)
        grid_location.addWidget(self.xloc_button, 0, 2)

        grid_location.addWidget(self.yloc, 1, 0)
        grid_location.addWidget(self.yloc_edit, 1, 1)
        grid_location.addWidget(self.yloc_button, 1, 2)

        grid_location.addWidget(self.zloc, 2, 0)
        grid_location.addWidget(self.zloc_edit, 2, 1)
        grid_location.addWidget(self.zloc_button, 2, 2)

        #-------------
        grid_location.addWidget(self.xrot, 3, 0)
        grid_location.addWidget(self.xrot_edit, 3, 1)
        grid_location.addWidget(self.xrot_button, 3, 2)

        grid_location.addWidget(self.yrot, 4, 0)
        grid_location.addWidget(self.yrot_edit, 4, 1)
        grid_location.addWidget(self.yrot_button, 4, 2)

        grid_location.addWidget(self.zrot, 5, 0)
        grid_location.addWidget(self.zrot_edit, 5, 1)
        grid_location.addWidget(self.zrot_button, 5, 2)

        grid_location.addWidget(self.rot_origin, 6, 0)
        grid_location.addWidget(self.rot_origin_edit, 6, 1)
        grid_location.addWidget(self.rot_origin_button, 6, 2)

        group_transforms.setLayout(grid_location)
        #--------------------------------------------------------

        self.about = QLabel('About')
        self.about_edit = QComboBox(self)
        for attach_item in ['0 : Global Origin', '1 : WingGeom']:
            self.about_edit.addItem(attach_item)

        self.attach_object = QComboBox(self)
        for attach_item in ['Attach', 'Object']:
            self.attach_object.addItem(attach_item)

        grid_symmetry = QHBoxLayout()
        grid_symmetry.addWidget(self.about)
        grid_symmetry.addWidget(self.about_edit)
        grid_symmetry.addWidget(self.attach_object)

        group_symmetry.setLayout(grid_symmetry)
        #--------------------------------------------------------
        scale = 1.1
        self.scale = QLabel('Scale')
        self.scale_edit = QJumpSlider(QtCore.Qt.Horizontal)
        self.scale_button = QLineEdit(str(scale))
        self.scale_edit.set_forward_connection(self.scale_button, float_func)

        self.reset_button = QPushButton('Reset')
        self.accept_button = QPushButton('Accept')

        grid_scale_factor = QGridLayout()
        grid_scale_factor.addWidget(self.scale, 0, 0)
        grid_scale_factor.addWidget(self.scale_edit, 0, 1)
        grid_scale_factor.addWidget(self.scale_button, 0, 2)
        grid_scale_factor.addWidget(self.reset_button, 0, 3)
        grid_scale_factor.addWidget(self.accept_button, 0, 4)
        group_scale_factor.setLayout(grid_scale_factor)
        #--------------------------------------------------------
        grid_attach_to_parent = QGridLayout()
        translate = QLabel('Translate:')
        rotate = QLabel('Rotate:')

        fzero_to_100 = lambda x: str(x / 100.)

        uvalue = 0.5
        wvalue = 0.6
        uname = QLabel('U:')
        uedit = QJumpSlider(QtCore.Qt.Horizontal)
        ubutton = QLineEdit(str(uvalue))
        uedit.set_forward_connection(ubutton, fzero_to_100)
        uedit.setRange(0, 100)

        wname = QLabel('W:')
        wedit = QJumpSlider(QtCore.Qt.Horizontal)
        wbutton = QLineEdit(str(wvalue))
        wedit.set_forward_connection(wbutton, fzero_to_100)
        wedit.setRange(0, 100)

        self.translate_none = QCheckBox('None')
        self.translate_comp = QCheckBox('Comp')
        self.translate_uw = QCheckBox('UW')

        self.rotate_none = QCheckBox('None')
        self.rotate_comp = QCheckBox('Comp')
        self.rotate_uw = QCheckBox('UW')

        grid_attach_to_parent.addWidget(translate, 0, 0)
        grid_attach_to_parent.addWidget(self.translate_none, 0, 1)
        grid_attach_to_parent.addWidget(self.translate_comp, 0, 2)
        grid_attach_to_parent.addWidget(self.translate_uw, 0, 3)

        grid_attach_to_parent.addWidget(rotate, 1, 0)
        grid_attach_to_parent.addWidget(self.rotate_none, 1, 1)
        grid_attach_to_parent.addWidget(self.rotate_comp, 1, 2)
        grid_attach_to_parent.addWidget(self.rotate_uw, 1, 3)

        grid_attach_to_parent.addWidget(uname, 2, 0)
        grid_attach_to_parent.addWidget(uedit, 2, 1)
        grid_attach_to_parent.addWidget(ubutton, 2, 2)

        grid_attach_to_parent.addWidget(wname, 3, 0)
        grid_attach_to_parent.addWidget(wedit, 3, 1)
        grid_attach_to_parent.addWidget(wbutton, 3, 2)
        group_attach_to_parent.setLayout(grid_attach_to_parent)

        #--------------------------------------------------------

        vbox = QVBoxLayout()
        vbox.addWidget(group_transforms)
        vbox.addWidget(group_symmetry)
        vbox.addWidget(group_scale_factor)
        vbox.addWidget(group_attach_to_parent)
        vbox.addStretch()

        #--------------------------------------------------------
        tab1 = QWidget()
        tab1.setLayout(vbox)
        return tab1

    def create_subsurfaces_layout(self):
        tab1 = QWidget()
        #tab1.setLayout(vbox)
        return tab1

    def create_design_layout(self):
        tab1 = QWidget()
        #tab1.setLayout(vbox)
        return tab1

    def create_skinning_layout(self):
        tab1 = QWidget()
        #tab1.setLayout(vbox)
        return tab1

    def create_xsec_layout(self):
        tab1 = QWidget()
        #tab1.setLayout(vbox)
        return tab1

    def create_layout(self):
        """displays the menu objects"""
        tab1 = self.create_geom_layout()
        tab2 = self.create_xform_layout()
        tab3 = self.create_subsurfaces_layout()

        tab4 = self.create_design_layout()
        tab5 = self.create_skinning_layout()
        tab6 = self.create_xsec_layout()
        tab3.setEnabled(False)
        tab4.setEnabled(False)
        tab5.setEnabled(False)
        tab6.setEnabled(False)


        #Create central widget, add layout and set
        #central_widget = QtGui.QWidget()
        #central_widget.setLayout(vbox)
        #self.setCentralWidget(central_widget)
        tabs = QTabWidget()
        tabs.addTab(tab1, "Geom")
        tabs.addTab(tab2, "XForm")

        tabs.addTab(tab3, "Sub-Surfaces")  # 2
        tabs.addTab(tab4, "Design")
        tabs.addTab(tab5, "Skinning")
        tabs.addTab(tab6, "X-Sec")

        tabs.setTabEnabled(2, False) # 0-based
        tabs.setTabEnabled(3, False) # 0-based
        tabs.setTabEnabled(4, False) # 0-based
        tabs.setTabEnabled(5, False) # 0-based

        #=================================================================
        vbox2 = QVBoxLayout()
        vbox2.addWidget(tabs)
        self.setLayout(vbox2)

    def set_connections(self):
        """creates the actions for the buttons"""
        self.name_button.clicked.connect(self.on_default_name)
        self.min_button.clicked.connect(self.on_default_min)
        self.max_button.clicked.connect(self.on_default_max)
        self.format_button.clicked.connect(self.on_default_format)
        self.scale_button.clicked.connect(self.on_default_scale)
        self.phase_button.clicked.connect(self.on_default_phase)

        self.nlabels_button.clicked.connect(self.on_default_nlabels)
        self.labelsize_button.clicked.connect(self.on_default_labelsize)
        self.ncolors_button.clicked.connect(self.on_default_ncolors)
        self.colormap_button.clicked.connect(self.on_default_colormap)

        self.animate_button.clicked.connect(self.on_animate)

        self.show_radio.clicked.connect(self.on_show_hide)
        self.hide_radio.clicked.connect(self.on_show_hide)

        self.apply_button.clicked.connect(self.on_apply)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        if qt_version == 4:
            self.connect(self, QtCore.SIGNAL('triggered()'), self.closeEvent)
            #self.colormap_edit.activated[str].connect(self.onActivated)
        #else:
            # closeEvent???

    def set_font_size(self, font_size):
        """
        Updates the font size of the objects

        Parameters
        ----------
        font_size : int
            the font size
        """
        return
        if self.font_size == font_size:
            return
        self.font_size = font_size
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        #self.name_edit.setFont(font)
        #self.min_edit.setFont(font)
        #self.max_edit.setFont(font)
        #self.format_edit.setFont(font)
        #self.scale_edit.setFont(font)
        #self.phase_edit.setFont(font)
        #self.nlabels_edit.setFont(font)
        #self.labelsize_edit.setFont(font)
        #self.ncolors_edit.setFont(font)

    def on_default_name(self):
        """action when user clicks 'Default' for name"""
        name = str(self._default_name)
        self.name_edit.setText(name)
        self.name_edit.setStyleSheet("QLineEdit{background: white;}")

    def on_default_min(self):
        """action when user clicks 'Default' for min value"""
        self.min_edit.setText(str(self._default_min))
        self.min_edit.setStyleSheet("QLineEdit{background: white;}")

    def on_default_max(self):
        """action when user clicks 'Default' for max value"""
        self.max_edit.setText(str(self._default_max))
        self.max_edit.setStyleSheet("QLineEdit{background: white;}")

    def on_default_format(self):
        """action when user clicks 'Default' for the number format"""
        self.format_edit.setText(str(self._default_format))
        self.format_edit.setStyleSheet("QLineEdit{background: white;}")

    def on_default_scale(self):
        """action when user clicks 'Default' for scale factor"""
        self.scale_edit.setText(str(self._default_scale))
        self.scale_edit.setStyleSheet("QLineEdit{background: white;}")

    def on_default_phase(self):
        """action when user clicks 'Default' for phase angle"""
        self.phase_edit.setText(str(self._default_phase))
        self.phase_edit.setStyleSheet("QLineEdit{background: white;}")

    def on_default_ncolors(self):
        """action when user clicks 'Default' for number of colors"""
        self.ncolors_edit.setText(str(self._default_ncolors))
        self.ncolors_edit.setStyleSheet("QLineEdit{background: white;}")

    #def on_default_colormap(self):
        #"""action when user clicks 'Default' for the color map"""
        #self.colormap_edit.setCurrentIndex(colormap_keys.index(self._default_colormap))

    def on_default_nlabels(self):
        """action when user clicks 'Default' for number of labels"""
        self.nlabels_edit.setStyleSheet("QLineEdit{background: white;}")
        self.nlabels_edit.setText(str(self._default_nlabels))

    def on_default_labelsize(self):
        """action when user clicks 'Default' for number of labelsize"""
        self.labelsize_edit.setText(str(self._default_labelsize))
        self.labelsize_edit.setStyleSheet("QLineEdit{background: white;}")

    def on_show_hide(self):
        """action when user clicks the 'Show/Hide' radio button"""
        self.colormap_edit.setCurrentIndex(colormap_keys.index(self._default_colormap))
        is_shown = self.show_radio.isChecked()
        self.vertical_radio.setEnabled(is_shown)
        self.horizontal_radio.setEnabled(is_shown)

    @staticmethod
    def check_name(cell):
        cell_value = cell.text()
        try:
            text = str(cell_value).strip()
        except UnicodeEncodeError:
            cell.setStyleSheet("QLineEdit{background: red;}")
            return None, False

        if len(text):
            cell.setStyleSheet("QLineEdit{background: white;}")
            return text, True
        else:
            cell.setStyleSheet("QLineEdit{background: red;}")
            return None, False

    #@staticmethod
    #def check_colormap(cell):
        #text = str(cell.text()).strip()
        #if text in colormap_keys:
            #cell.setStyleSheet("QLineEdit{background: white;}")
            #return text, True
        #else:
            #cell.setStyleSheet("QLineEdit{background: red;}")
            #return None, False

    def on_validate(self):
        name_value, flag0 = self.check_name(self.name_edit)
        min_value, flag1 = self.check_float(self.min_edit)
        max_value, flag2 = self.check_float(self.max_edit)
        format_value, flag3 = self.check_format(self.format_edit)
        scale, flag4 = self.check_float(self.scale_edit)
        phase, flag5 = self.check_float(self.phase_edit)

        nlabels, flag6 = self.check_positive_int_or_blank(self.nlabels_edit)
        ncolors, flag7 = self.check_positive_int_or_blank(self.ncolors_edit)
        labelsize, flag8 = self.check_positive_int_or_blank(self.labelsize_edit)
        colormap = str(self.colormap_edit.currentText())

        if all([flag0, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8]):
            if 'i' in format_value:
                format_value = '%i'

            assert isinstance(scale, float), scale
            self.out_data['name'] = name_value
            self.out_data['min'] = min_value
            self.out_data['max'] = max_value
            self.out_data['format'] = format_value
            self.out_data['scale'] = scale
            self.out_data['phase'] = phase

            self.out_data['nlabels'] = nlabels
            self.out_data['ncolors'] = ncolors
            self.out_data['labelsize'] = labelsize
            self.out_data['colormap'] = colormap

            self.out_data['is_low_to_high'] = self.low_to_high_radio.isChecked()
            self.out_data['is_horizontal'] = self.horizontal_radio.isChecked()
            self.out_data['is_shown'] = self.show_radio.isChecked()

            self.out_data['clicked_ok'] = True
            self.out_data['close'] = True
            #print('self.out_data = ', self.out_data)
            #print("name = %r" % self.name_edit.text())
            #print("min = %r" % self.min_edit.text())
            #print("max = %r" % self.max_edit.text())
            #print("format = %r" % self.format_edit.text())
            return True
        return False

    def on_apply(self):
        passed = self.on_validate()
        if passed:
            self.win_parent._apply_legend(self.out_data)
        return passed

    def on_ok(self):
        passed = self.on_apply()
        if passed:
            self.close()
            #self.destroy()

    def on_cancel(self):
        self.out_data['close'] = True
        self.close()


def float_func(val):
    return str(val)


def main(): # pragma: no cover
    # kills the program when you hit Cntl+C from the command line
    # doesn't save the current state as presumably there's been an error
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)


    import sys
    # Someone is launching this directly
    # Create the QApplication
    app = QApplication(sys.argv)
    #The Main window

    transform = {
        'xyz' : [0., 0., 0.],
        'is_absolute' : False,
        'rot origin(X)' : 0.,
    }
    symmetry = {}
    data = {
        'name' : 'WingGeom',
        'color' : (0, 0, 255),
        'font_size' : 8,
        'num_U' : 16,
        'num_W' : 33,
        'Density' : 1.0,
        'Thin Shell' : False,
        'Mass/Area' : 1.0,
        #'Priority' : 0,
        'Negative Volume' : False,

        'transform' : transform,
        'symmetry' : symmetry,
    }
    main_window = WingWindow(data)

    main_window.show()
    # Enter the main loop
    app.exec_()

if __name__ == "__main__": # pragma: no cover
    main()
