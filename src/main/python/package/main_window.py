"""
Create the GUI
"""

from PySide2 import QtWidgets, QtCore, QtGui

from package.data_list import CS_TARGET_LIST, FORMAT_LIST, BITDEPTH_DICO, ODT_LIST,IDT_LIST


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx

        self.setWindowTitle("PYCO ColorSpace")
        self.setup_ui()

    def setup_ui(self):
        self.load_fonts()
        self.create_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.modify_widgets()
        self.setup_connections()
        self.add_actions_to_toolbar()
        self.add_cbb_items()

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.toolbar_top = QtWidgets.QToolBar()
        self.toolbar_opt = QtWidgets.QToolBar()
        self.status_bar = QtWidgets.QStatusBar()

        # Left Frame
        self.frm_left = QtWidgets.QFrame()
        self.treeview = QtWidgets.QTreeWidget()
        self.lbl_placeholder = QtWidgets.QLabel("Drag & Drop files here")

        self.spltr_middle = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Right Frame
        self.frm_right = QtWidgets.QFrame()
        self.frm_right_top = QtWidgets.QFrame()
        self.lbl_cbb_target = QtWidgets.QLabel('TARGET COLORSPACE')
        self.cbb_target_cs = QtWidgets.QComboBox()

        self.lbl_exportOptions = QtWidgets.QLabel("Global Export Options")
        self.cbb_exprt_format = QtWidgets.QComboBox()
        self.cbb_exprt_bit = QtWidgets.QComboBox()
        self.cbb_exprt_odt = QtWidgets.QComboBox()
        self.lbl_exprt_format = QtWidgets.QLabel(" format")
        self.lbl_exprt_bitdepth = QtWidgets.QLabel(" bitdepth")
        self.lbl_exprt_odt = QtWidgets.QLabel(" ODT")

        self.rb_exprt_folder = QtWidgets.QRadioButton('Export in a new folder')
        self.rb_exprt_file = QtWidgets.QRadioButton('Export at the same location')

        # Input Options
        self.lbl_in_title = QtWidgets.QLabel("File Input Options")
        self.lbl_in_idt = QtWidgets.QLabel("Source ColorSpace (IDT)")
        self.cbb_in_idt = QtWidgets.QComboBox()

        # Toolbar items
        self.lbl_title = QtWidgets.QLabel(' IMAGE COLORSPACE CONVERTER')
        self.widget_spacer = QtWidgets.QWidget()
        self.widget_spacer2 = QtWidgets.QWidget()

    def modify_widgets(self):
        QtCore.QResource.registerResource(self.ctx.get_resource('qt_resources/icon_ressource.rcc'))

        # Styling controls
        self.setStyleSheet(self.stylesheetContent('stylesheet'))
        self.main_widget.setStyleSheet(""".QWidget{background: rgb(40, 40, 42);}""")
        self.status_bar.showMessage("Status Bar Is Ready", 3000)

        # ToolBar
        self.lbl_title.setEnabled(False)
        print(self.lbl_title.isEnabled())
        self.toolbar_opt.setStyleSheet(self.stylesheetContent('stylesheet_variations'))
        self.lbl_title.setStyleSheet(self.stylesheetContent('stylesheet_title'))
        self.widget_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.widget_spacer2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.toolbar_top.setMovable(False)
        self.toolbar_opt.setIconSize(QtCore.QSize(40, 40))

        # TreeView
        self.treeview.setHeaderHidden(False)

        self.spltr_middle.addWidget(self.frm_left)
        self.spltr_middle.addWidget(self.frm_right)
        self.spltr_middle.setSizes([400, 200])
        self.spltr_middle.setHandleWidth(5)
        self.spltr_middle.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                        QtWidgets.QSizePolicy.MinimumExpanding, )
        # Right Frame
        self.lbl_cbb_target.setStyleSheet(self.stylesheetContent('stylesheet_title'))
        self.cbb_target_cs.setStyleSheet(self.stylesheetContent('stylesheet_variations'))
        self.frm_right_top.setStyleSheet(
            """.QFrame{background-color: rgb(40,40,40) ;margin:5px; border-left: 3px solid #E0D43D;} """)
        self.lyt_rFrame.insertStretch(-1)
        self.frm_right.setMinimumSize(QtCore.QSize(250, 400))
        self.frm_left.setMinimumSize(QtCore.QSize(250, 400))
        self.lbl_exportOptions.setStyleSheet(self.stylesheetContent('stylesheet_variations'))
        self.cbb_exprt_format.setMaximumWidth(50)
        self.cbb_exprt_bit.setMaximumWidth(150)
        self.rb_exprt_file.setChecked(QtCore.Qt.Checked)

        self.lbl_in_title.setStyleSheet(self.stylesheetContent('stylesheet_variations'))

    def create_layouts(self):
        self.lyt_main = QtWidgets.QHBoxLayout(self.main_widget)
        self.lyt_main.setMargin(0)
        self.lyt_lFrame = QtWidgets.QVBoxLayout(self.frm_left)
        self.lyt_rFrame = QtWidgets.QVBoxLayout(self.frm_right)
        self.lyt_rFrame.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.lyt_rFrame_top = QtWidgets.QVBoxLayout(self.frm_right_top)
        self.lyt_exportOpt_grid = QtWidgets.QGridLayout()
        self.lyt_exportOpt_grid.setContentsMargins(QtCore.QMargins(9, 9, 9, 9))
        self.lyt_exportOpt_grid.setVerticalSpacing(0)
        self.lyt_exportOpt_grid.setRowMinimumHeight(3, 65)
        self.lyt_in_grid = QtWidgets.QGridLayout()
        self.lyt_in_grid.setContentsMargins(QtCore.QMargins(9, 9, 9, 9))

    def add_widgets_to_layouts(self):
        self.setCentralWidget(self.main_widget)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar_top)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar_opt)
        self.setStatusBar(self.status_bar)
        self.toolbar_top.addWidget(self.lbl_title)

        self.lyt_main.addWidget(self.spltr_middle)

        # self.lyt_lFrame.addWidget(self.treeview)
        self.lyt_lFrame.addWidget(self.lbl_placeholder)
        self.lyt_lFrame.setAlignment(QtCore.Qt.AlignHCenter)

        self.lyt_rFrame.addWidget(self.frm_right_top)
        self.lyt_rFrame_top.addWidget(self.lbl_cbb_target)
        self.lyt_rFrame_top.addWidget(self.cbb_target_cs)
        self.lyt_rFrame.addLayout(self.lyt_exportOpt_grid)

        self.lyt_exportOpt_grid.addWidget(self.lbl_exportOptions, 0, 0, 1, 3)
        self.lyt_exportOpt_grid.addWidget(self.cbb_exprt_format, 1, 0)
        self.lyt_exportOpt_grid.addWidget(self.cbb_exprt_bit, 1, 1)
        self.lyt_exportOpt_grid.addWidget(self.cbb_exprt_odt, 1, 2)
        self.lyt_exportOpt_grid.addWidget(self.lbl_exprt_format, 2, 0)
        self.lyt_exportOpt_grid.addWidget(self.lbl_exprt_bitdepth, 2, 1)
        self.lyt_exportOpt_grid.addWidget(self.lbl_exprt_odt, 2, 2)
        self.lyt_exportOpt_grid.addWidget(self.rb_exprt_folder, 3, 1, 1, 1)
        self.lyt_exportOpt_grid.addWidget(self.rb_exprt_file, 3, 2, 1, 1)

        self.lyt_rFrame.addLayout(self.lyt_in_grid)
        self.lyt_in_grid.addWidget(self.lbl_in_title, 0, 0, 1, 1)
        self.lyt_in_grid.addWidget(self.lbl_in_idt, 1, 0)
        self.lyt_in_grid.addWidget(self.cbb_in_idt, 2, 0)

    def setup_connections(self):
        pass

    def add_actions_to_toolbar(self):
        self.toolbar_top.addWidget(self.widget_spacer)
        action_list = ['info', 'settings']
        for action in action_list:
            icon = self.ctx.get_resource(f"icon_{action}.png")
            self.toolbar_top.addAction(QtGui.QIcon(icon), action.capitalize())
            # action.triggered.connect(partial(self.change_location, location))
        action_list2 = ['open', 'convert']
        for action in action_list2:
            icon = self.ctx.get_resource(f"icon_{action}.png")
            action = self.toolbar_opt.addAction(QtGui.QIcon(icon), action.capitalize())
        self.toolbar_opt.insertWidget(action, self.widget_spacer2)

    def stylesheetContent(self, name):
        css_file = self.ctx.get_resource(f"{name}.css")
        with open(css_file, "r") as f:
            content = f.read()
        return content

    def add_cbb_items(self):
        self.cbb_target_cs.addItems(CS_TARGET_LIST)
        self.cbb_exprt_format.addItems(FORMAT_LIST)
        self.cbb_exprt_bit.addItems(BITDEPTH_DICO.keys())
        self.cbb_exprt_bit.setCurrentIndex(2)
        self.cbb_exprt_odt.addItems(ODT_LIST)
        self.cbb_in_idt.addItems(IDT_LIST)
        # self.cbb_target_cs.setMaximumHeight()

    def load_fonts(self):
        path1 = self.ctx.get_resource("font/JosefinSans-SemiBold.ttf")
        path2 = self.ctx.get_resource("font/JosefinSans-Medium.ttf")
        path3 = self.ctx.get_resource("font/JosefinSans-Bold.ttf")
        font_load1 = QtGui.QFontDatabase.addApplicationFont(path1)
        font_load2 = QtGui.QFontDatabase.addApplicationFont(path2)
        font_load3 = QtGui.QFontDatabase.addApplicationFont(path3)
        print(QtGui.QFontDatabase.applicationFontFamilies(font_load1))
        print(QtGui.QFontDatabase.applicationFontFamilies(font_load2))
        print(QtGui.QFontDatabase.applicationFontFamilies(font_load3))
