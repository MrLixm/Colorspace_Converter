from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx

        self.setWindowTitle("PYCO ColorSpace")
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.add_actions_to_toolbar()

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.toolbar = QtWidgets.QToolBar()
        self.status_bar = QtWidgets.QStatusBar()

        self.treeview = QtWidgets.QTreeWidget()
        self.frm_right = QtWidgets.QFrame()

        # Toolbar items
        self.lbl_title = QtWidgets.QLabel(' IMAGE COLORSPACE CONVERTER')
        self.lbl_title.setStyleSheet(self.stylesheetContent('stylesheet_title'))
        self.widget_spacer = QtWidgets.QWidget()

    def modify_widgets(self):
        # Styling controls
        self.setStyleSheet(self.stylesheetContent('stylesheet'))
        self.main_widget.setStyleSheet(""".QWidget{background: rgb(40, 40, 42);}""")

        self.status_bar.showMessage("Status Bar Is Ready", 3000)

        # ToolBar
        self.widget_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.toolbar.setMovable(False)

        # TreeView
        self.treeview.setHeaderHidden(True)

        # Right Frame
        self.frm_right.setMinimumSize(QtCore.QSize(250, 80))

    def create_layouts(self):
        self.lyt_main = QtWidgets.QHBoxLayout(self.main_widget)
        self.lyt_rFrame = QtWidgets.QVBoxLayout(self.frm_right)

    def add_widgets_to_layouts(self):
        self.setCentralWidget(self.main_widget)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setStatusBar(self.status_bar)
        self.toolbar.addWidget(self.lbl_title)

        self.lyt_main.addWidget(self.treeview)
        self.lyt_main.addWidget(self.frm_right)

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
