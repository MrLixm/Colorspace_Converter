"""
Create the GUI
"""

from PySide2 import QtWidgets, QtCore, QtGui
from package.data_list import CS_TARGET_LIST, FORMAT_LIST, BITDEPTH_DICO


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
        self.toolbar = QtWidgets.QToolBar()
        self.status_bar = QtWidgets.QStatusBar()

        # Left Frame
        self.frm_left = QtWidgets.QFrame()
        self.treeview = QtWidgets.QTreeWidget()

        self.spltr_middle = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Right Frame
        self.frm_right = QtWidgets.QFrame()
        self.frm_right_top = QtWidgets.QFrame()
        self.lbl_cbb_target = QtWidgets.QLabel('TARGET COLORSPACE')
        self.cbb_target_cs = QtWidgets.QComboBox()

        self.lbl_exportOptions = QtWidgets.QLabel("Global Export Options")
        self.cbb_exprt_format = QtWidgets.QComboBox()
        self.cbb_exprt_bit = QtWidgets.QComboBox()


        # Toolbar items
        self.lbl_title = QtWidgets.QLabel(' IMAGE COLORSPACE CONVERTER')
        self.widget_spacer = QtWidgets.QWidget()

    def modify_widgets(self):
        # Styling controls
        self.setStyleSheet(self.stylesheetContent('stylesheet'))
        self.main_widget.setStyleSheet(""".QWidget{background: rgb(40, 40, 42);}""")
        self.status_bar.showMessage("Status Bar Is Ready", 3000)

        # ToolBar
        self.lbl_title.setEnabled(False)
        print(self.lbl_title.isEnabled())
        self.lbl_title.setStyleSheet(self.stylesheetContent('stylesheet_title'))
        self.widget_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.toolbar.setMovable(False)

        # TreeView
        self.treeview.setHeaderHidden(True)

        self.spltr_middle.addWidget(self.frm_left)
        self.spltr_middle.addWidget(self.frm_right)
        self.spltr_middle.setSizes([200, 200])
        self.spltr_middle.setHandleWidth(5)

        # Right Frame
        self.lbl_cbb_target.setStyleSheet(self.stylesheetContent('stylesheet_title'))
        self.cbb_target_cs.setStyleSheet(self.stylesheetContent('stylesheet_variations'))
        self.frm_right_top.setStyleSheet("""QFrame{background-color: #E0D43D;} """)
        self.lyt_rFrame.insertStretch(-1)
        self.frm_right.setMinimumSize(QtCore.QSize(250, 400))
        self.frm_left.setMinimumSize(QtCore.QSize(250, 400))

    def create_layouts(self):
        self.lyt_main = QtWidgets.QHBoxLayout(self.main_widget)
        self.lyt_main.setMargin(0)
        self.lyt_lFrame = QtWidgets.QVBoxLayout(self.frm_left)
        self.lyt_rFrame = QtWidgets.QVBoxLayout(self.frm_right)
        self.lyt_rFrame.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.lyt_rFrame_top = QtWidgets.QVBoxLayout(self.frm_right_top)
        self.lyt_exportOpt_grid = QtWidgets.QGridLayout()
        self.lyt_exportOpt_grid.setContentsMargins(QtCore.QMargins(9, 9, 9, 9))


    def add_widgets_to_layouts(self):
        self.setCentralWidget(self.main_widget)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setStatusBar(self.status_bar)
        self.toolbar.addWidget(self.lbl_title)

        self.lyt_main.addWidget(self.spltr_middle)

        self.lyt_lFrame.addWidget(self.treeview)
        self.lyt_rFrame.addWidget(self.frm_right_top)
        self.lyt_rFrame_top.addWidget(self.lbl_cbb_target)
        self.lyt_rFrame_top.addWidget(self.cbb_target_cs)
        self.lyt_rFrame.addLayout(self.lyt_exportOpt_grid)

        self.lyt_exportOpt_grid.addWidget(self.lbl_exportOptions, 0, 0)
        self.lyt_exportOpt_grid.addWidget(self.cbb_exprt_format, 1, 0)
        self.lyt_exportOpt_grid.addWidget(self.cbb_exprt_bit, 1, 1)

    def setup_connections(self):
        pass

    def add_actions_to_toolbar(self):
        self.toolbar.addWidget(self.widget_spacer)
        action_list = ['info', 'settings']
        for action in action_list:
            icon = self.ctx.get_resource(f"icon_{action}.png")
            action = self.toolbar.addAction(QtGui.QIcon(icon), action.capitalize())
            # action.triggered.connect(partial(self.change_location, location))

    def stylesheetContent(self, name):
        css_file = self.ctx.get_resource(f"{name}.css")
        with open(css_file, "r") as f:
            content = f.read()
        return content

    def add_cbb_items(self):
        self.cbb_target_cs.addItems(CS_TARGET_LIST)
        self.cbb_exprt_format.addItems()
        # self.cbb_target_cs.setMaximumHeight()

    def load_fonts(self):
        path1 = self.ctx.get_resource("font/JosefinSans-Bold.ttf")
        path2 = self.ctx.get_resource("font/JosefinSans-Thin.ttf")
        font_load1 = QtGui.QFontDatabase.addApplicationFont(path1)
        font_load2 = QtGui.QFontDatabase.addApplicationFont(path2)
