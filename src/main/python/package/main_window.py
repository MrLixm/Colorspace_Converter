"""
Create the GUI
"""

from PySide2 import QtWidgets, QtCore, QtGui

from package.data_list import CS_TARGET_LIST, FORMAT_LIST, BITDEPTH_DICO, ODT_DICO, IDT_DICO, COMPRESSION_LIST
from package.API.converter import Converter


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
        self.add_actions_to_toolbar()
        self.add_cbb_items()
        self.cbb_update()
        self.setup_connections()

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

        self.widget_rightSide = QtWidgets.QWidget()  # Widget which contain the 2 frame on the right side
        # Right Frame
        self.frm_exprt_option = QtWidgets.QFrame()
        self.frm_right_targetcs = QtWidgets.QFrame()
        self.lbl_cbb_target = QtWidgets.QLabel('TARGET COLORSPACE')
        self.cbb_target_cs = QtWidgets.QComboBox()

        self.lbl_exportOptions = QtWidgets.QLabel("Global Export Options")
        self.cbb_exprt_format = QtWidgets.QComboBox()
        self.cbb_exprt_bit = QtWidgets.QComboBox()
        self.cbb_exprt_odt = QtWidgets.QComboBox()
        self.cbb_exprt_compress = QtWidgets.QComboBox()
        self.lbl_exprt_format = QtWidgets.QLabel(" format")
        self.lbl_exprt_bitdepth = QtWidgets.QLabel(" bitdepth")
        self.lbl_exprt_odt = QtWidgets.QLabel(" ODT")
        self.lbl_exprt_compress = QtWidgets.QLabel(" Compression")
        self.spnb_exprt_compress = QtWidgets.QSpinBox()
        self.lbl_exprt_compress_qual = QtWidgets.QLabel("Compression Amount")

        self.rb_exprt_folder = QtWidgets.QRadioButton('Export in a new folder')
        self.rb_exprt_file = QtWidgets.QRadioButton('Export at the same location')

        # Input Options
        self.frm_right_input = QtWidgets.QFrame()
        self.lbl_in_title = QtWidgets.QLabel("File Input Options")
        self.lbl_in_idt = QtWidgets.QLabel("Source ColorSpace (IDT)")
        self.cbb_in_idt = QtWidgets.QComboBox()

        # Toolbar items
        self.lbl_title = QtWidgets.QLabel(' IMAGE COLORSPACE CONVERTER')
        self.widget_spacer = QtWidgets.QWidget()
        self.widget_spacer2 = QtWidgets.QWidget()

    def create_layouts(self):
        self.lyt_main = QtWidgets.QHBoxLayout(self.main_widget)
        self.lyt_main.setMargin(0)
        self.lyt_lFrame = QtWidgets.QVBoxLayout(self.frm_left)
        self.lyt_rightSide = QtWidgets.QVBoxLayout(self.widget_rightSide)
        self.lyt_rightSide.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.lyt_rightSide.setSpacing(0)

        self.lyt_frm_exprt_option = QtWidgets.QVBoxLayout(self.frm_exprt_option)
        self.lyt_frm_exprt_option.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.lyt_rFrame_top = QtWidgets.QVBoxLayout(self.frm_right_targetcs)

        self.lyt_exportOpt_grid = QtWidgets.QGridLayout()
        self.lyt_exportOpt_grid.setContentsMargins(QtCore.QMargins(9, 9, 9, 9))
        self.lyt_exportOpt_grid.setVerticalSpacing(0)
        # self.lyt_exportOpt_grid.setRowMinimumHeight(0, 60)  # title row
        self.lyt_exportOpt_grid.setRowMinimumHeight(3, 15)  # Compress row
        # self.lyt_exportOpt_grid.setRowMinimumHeight(5, 65)

        self.lyt_in_grid = QtWidgets.QGridLayout(self.frm_right_input)
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

        self.lyt_rightSide.addWidget(self.frm_right_targetcs)
        self.lyt_rFrame_top.addWidget(self.lbl_cbb_target)
        self.lyt_rFrame_top.addWidget(self.cbb_target_cs)
        self.lyt_rFrame_top.addWidget(self.cbb_exprt_odt)
        self.lyt_rFrame_top.addWidget(self.lbl_exprt_odt)

        self.lyt_rightSide.addWidget(self.lbl_exportOptions)

        self.lyt_rightSide.addWidget(self.frm_exprt_option)
        self.lyt_frm_exprt_option.addLayout(self.lyt_exportOpt_grid)
        # self.lyt_exportOpt_grid.addWidget(self.lbl_exportOptions, 0, 0, 1, 2)
        self.lyt_exportOpt_grid.addWidget(self.cbb_exprt_format, 1, 0)
        self.lyt_exportOpt_grid.addWidget(self.lbl_exprt_format, 2, 0)
        self.lyt_exportOpt_grid.addWidget(self.cbb_exprt_bit, 1, 1)
        self.lyt_exportOpt_grid.addWidget(self.lbl_exprt_bitdepth, 2, 1)
        self.lyt_exportOpt_grid.addWidget(self.cbb_exprt_compress, 4, 0)
        self.lyt_exportOpt_grid.addWidget(self.lbl_exprt_compress, 5, 0)
        self.lyt_exportOpt_grid.addWidget(self.spnb_exprt_compress, 4, 1)
        self.lyt_exportOpt_grid.addWidget(self.lbl_exprt_compress_qual, 5, 1)
        # self.lyt_exportOpt_grid.addWidget(self.rb_exprt_folder, 6, 0, 1, 1)
        # self.lyt_exportOpt_grid.addWidget(self.rb_exprt_file, 6, 1, 1, 1)

        self.lyt_rightSide.addWidget(self.lbl_in_title)
        self.lyt_rightSide.addWidget(self.frm_right_input)
        # self.lyt_in_grid.addWidget(self.lbl_in_title, 0, 0, 1, 1)
        self.lyt_in_grid.addWidget(self.lbl_in_idt, 0, 0)
        self.lyt_in_grid.addWidget(self.cbb_in_idt, 1, 0)

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
        self.frm_left.setAcceptDrops(True)
        # self.frm_left.dropEvent(QtGui.QDropEvent())
        self.treeview.setHeaderHidden(False)

        self.spltr_middle.addWidget(self.frm_left)
        self.spltr_middle.addWidget(self.widget_rightSide)
        self.spltr_middle.setSizes([400, 200])
        self.spltr_middle.setHandleWidth(5)
        self.spltr_middle.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                        QtWidgets.QSizePolicy.MinimumExpanding, )

        # ----------------- #
        # Right Frame
        # ----------------- #
        self.lbl_cbb_target.setStyleSheet(self.stylesheetContent('stylesheet_title'))
        self.cbb_target_cs.setStyleSheet(self.stylesheetContent('stylesheet_variations'))
        # self.cbb_target_cs.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # self.cbb_exprt_odt.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # self.cbb_target_cs.setInputMethodHints(QtCore.Qt.InputMethodHint.)
        self.cbb_target_cs.setMinimumHeight(50)
        self.cbb_exprt_odt.setMinimumHeight(30)

        self.frm_right_targetcs.setStyleSheet(
            """.QFrame{background-color: rgb(50,50,50) ;margin:0px; border-left: 3px solid #E0D43D;} """)
        self.cbb_exprt_odt.setStyleSheet("""QComboBox{background-color:rgb(40,40,40);}""")
        # self.lyt_frm_exprt_option.insertStretch(-1)
        self.lbl_exportOptions.setStyleSheet(self.stylesheetContent('stylesheet_variations'))
        # self.lbl_exportOptions.setMinimumHeight(40)
        self.cbb_exprt_format.setMaximumWidth(95)
        self.cbb_exprt_bit.setMaximumWidth(150)
        self.cbb_exprt_format.setMinimumHeight(30)
        self.cbb_exprt_bit.setMinimumHeight(30)
        self.cbb_exprt_compress.setMinimumHeight(30)
        self.spnb_exprt_compress.setMinimumHeight(30)

        # self.lyt_exportOpt_grid.setRowMinimumHeight(1,30)
        # self.rb_exprt_folder.setIconSize(QtCore.QSize(90,50))
        # self.rb_exprt_file.setFixedSize(25, 25)
        self.rb_exprt_file.setChecked(QtCore.Qt.Checked)

        # Inputs options
        self.lbl_in_title.setStyleSheet(self.stylesheetContent('stylesheet_variations'))
        self.lbl_in_title.setMaximumHeight(35)
        self.cbb_in_idt.setMinimumHeight(30)
        self.lyt_in_grid.setRowStretch(4,1)

    def add_actions_to_toolbar(self):

        # Add space before creating actions
        self.toolbar_top.addWidget(self.widget_spacer)

        action_list = ['info', 'settings']
        for action in action_list:
            icon = self.ctx.get_resource(f"icon_{action}.png")
            self.toolbar_top.addAction(QtGui.QIcon(icon), action.capitalize())

        self.act_open = QtWidgets.QAction(QtGui.QIcon(self.ctx.get_resource("icon_open.png")), "Open image", self)
        self.toolbar_opt.addAction(self.act_open)
        self.act_convert = QtWidgets.QAction(QtGui.QIcon(self.ctx.get_resource("icon_convert.png")), "Convert", self)
        self.toolbar_opt.addAction(self.act_convert)

        self.toolbar_opt.insertWidget(self.act_convert, self.widget_spacer2)

    def add_cbb_items(self):
        self.cbb_target_cs.addItems(CS_TARGET_LIST)
        self.cbb_exprt_format.addItems(FORMAT_LIST)
        self.cbb_exprt_bit.addItems(BITDEPTH_DICO.keys())
        self.cbb_exprt_bit.setCurrentIndex(2)
        self.cbb_exprt_odt.addItems(ODT_DICO)
        self.cbb_in_idt.addItems(IDT_DICO)
        self.cbb_exprt_compress.addItems([i.capitalize() for i in COMPRESSION_LIST])
        # self.cbb_target_cs.setMaximumHeight()

    def convert(self):
        self.error_list=[]
        resources = self.ctx.get_resource()
        print("Converting")

    def cbb_update(self):
        export_format = self.cbb_exprt_format.currentText()
        if export_format == '.jpg':
            self.cbb_exprt_bit.clear()
            self.cbb_exprt_bit.addItem('8bit Int')
            self.cbb_exprt_bit.setEnabled(False)
            self.cbb_exprt_compress.clear()
            self.cbb_exprt_compress.addItem('jpg')
            self.cbb_exprt_compress.setEnabled(False)

        elif export_format == '.png':
            self.cbb_exprt_bit.clear()
            self.cbb_exprt_bit.addItems(['8bit Int', '16bit Int'])
            self.cbb_exprt_bit.setEnabled(True)
            self.cbb_exprt_compress.clear()
            self.cbb_exprt_compress.addItem('None')
            self.cbb_exprt_compress.setEnabled(False)
        elif export_format == '.exr':
            self.cbb_exprt_bit.clear()
            self.cbb_exprt_bit.addItems(['16bit Half', '32bit Float'])
            self.cbb_exprt_bit.setEnabled(True)
            self.cbb_exprt_compress.clear()
            self.cbb_exprt_compress.addItems([i.capitalize() for i in COMPRESSION_LIST])
            self.cbb_exprt_compress.setEnabled(True)
            self.cbb_exprt_compress.setCurrentText('Zip')

        elif export_format == 'Original':
            self.cbb_exprt_bit.clear()
            self.cbb_exprt_bit.addItem('Original')
            self.cbb_exprt_bit.setEnabled(False)
            self.cbb_exprt_compress.clear()
            self.cbb_exprt_compress.addItem('/')
            self.cbb_exprt_compress.setEnabled(False)

        if export_format == '.exr' or export_format == 'Original':
            print("No ODT")
            self.cbb_exprt_odt.setEnabled(False)
            self.cbb_exprt_odt.setCurrentText('None')
            self.cbb_exprt_odt.setHidden(True)
            self.lbl_exprt_odt.setHidden(True)

        else:
            print("odt")
            self.cbb_exprt_odt.setEnabled(True)
            self.cbb_exprt_odt.setHidden(False)
            self.cbb_exprt_odt.setCurrentText('None')
            self.lbl_exprt_odt.setHidden(False)

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

    def setup_connections(self):
        self.act_convert.triggered.connect(self.convert)
        self.cbb_exprt_format.currentTextChanged.connect(self.cbb_update)

    def stylesheetContent(self, name):
        css_file = self.ctx.get_resource(f"{name}.css")
        with open(css_file, "r") as f:
            content = f.read()
        return content

