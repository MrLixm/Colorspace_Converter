"""
Create the GUI for the app

Author: Liam Collod
Contact: lcollod@gmail.com
"""
import os
import logging
import subprocess
import webbrowser
from functools import partial
from pathlib import Path

from PySide2 import QtWidgets, QtCore, QtGui

from package.API.converter import Converter
from package.data_list import CS_TARGET_DICO, FORMAT_LIST, BITDEPTH_DICO, ODT_DICO, IDT_DICO, COMPRESSION_LIST
from package.info_window import InfoWindow
from package.widget_frame_custom import FrameCustom


# TODO: implement settings menu

class Worker(QtCore.QObject):
    file_converted = QtCore.Signal(object, list)
    step_converter = QtCore.Signal()
    finished = QtCore.Signal()

    def __init__(self, tree_item_list, out_location, out_format, out_bitdepth,
                 out_cs, odt, resources_path, compression, out_location_path):
        super().__init__()
        self.tree_item_list = tree_item_list
        self.out_location = out_location
        self.out_location_path = out_location_path
        self.out_format = out_format
        self.out_bitdepth = out_bitdepth
        self.out_cs = CS_TARGET_DICO.get(out_cs)[0]
        self.cctf_encoding = CS_TARGET_DICO.get(out_cs)[1]
        self.out_odt = odt
        self.resources_path = resources_path
        self.compression = compression
        self.abort = False

    def convert_file(self):
        for tree_item in self.tree_item_list:
            if not self.abort:
                item_file_path = tree_item.text(3)
                item_in_cs = IDT_DICO.get(tree_item.text(4))[0]  # Get the colorspace only
                item_cctf = IDT_DICO.get(tree_item.text(4))[1]
                output_path = self.pathGeneration(item_file_path, self.out_location, self.out_format,
                                                  self.out_location_path)

                converter = Converter(item_file_path, out_bitdepth=self.out_bitdepth, in_cs=item_in_cs,
                                      out_cs=self.out_cs, odt=self.out_odt, resources_path=self.resources_path,
                                      compression=self.compression, cctf=item_cctf, cctf_encoding=self.cctf_encoding,
                                      out_file_path=output_path)

                result_list = converter.image_processing()
                # converter.convert_progress.connect(self.step_converter.emit())
                self.file_converted.emit(tree_item, result_list)

        self.finished.emit()

    def pathGeneration(self, in_path, out_location, out_format, out_location_path):
        """

        Args:
            out_location_path: Path of the user selected output folder
            in_path: path to the input file
            out_location: user preference for the location of the output file
            out_format: user preference for the output file format

        Returns: path of the output file

        """

        file_folder_path = os.path.dirname(in_path)
        filename_original = os.path.splitext(os.path.basename(in_path))[0]
        file_ext = os.path.splitext(in_path)[1]

        # For the original options that has been removed
        if out_format.lower() == 'original':
            out_ext = file_ext
        else:
            out_ext = out_format

        # If ODT is used, prefix it to the file name
        if ODT_DICO.get(self.out_odt):
            cs_prefix = '_' + self.out_odt
        else:
            # Use the output colorspace as prefix
            cs_prefix = '_' + self.out_cs.replace(" ", "")

        out_file_name = filename_original + cs_prefix + out_ext

        if out_location == 'file':
            output_path = os.path.join(file_folder_path, out_file_name)
            return output_path
        if out_location == 'folder':
            if out_location_path:
                output_path = os.path.join(out_location_path, out_file_name)
                return output_path
            else:
                aces_folder_path = os.path.join(file_folder_path, 'ACEScg')
                if not os.path.exists(aces_folder_path):
                    os.makedirs(aces_folder_path)
                output_path = os.path.join(aces_folder_path, out_file_name)
                return output_path


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx

        self.setWindowTitle("PYCO ColorSpace Converter")
        self.setup_ui()

    def setup_ui(self):
        self.load_fonts()
        self.create_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.modify_widgets()
        self.add_actions_to_toolbar()
        self.add_cbb_items()
        self.cbb_update_format()
        self.rb_update_location()
        self.setup_connections()
        # self.cbb_udpate_odt()

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.toolbar_top = QtWidgets.QToolBar()
        self.toolbar_opt = QtWidgets.QToolBar()
        self.status_bar = QtWidgets.QStatusBar()
        self.stat_lbl_item = QtWidgets.QLabel("  Files to convert: 0 ")

        # Left Frame
        self.widget_left_icons = QtWidgets.QWidget()
        self.widget_left_icons.setHidden(True)
        self.lbl_placeholder = QtWidgets.QLabel("Drag & Drop files here")
        self.btn_tw_deleteall = QtWidgets.QPushButton(QtGui.QIcon(self.ctx.get_resource("icon_tw_all.png")), '')
        self.btn_tw_deleteall.setToolTip("Remove all items")
        self.btn_tw_deletedone = QtWidgets.QPushButton(QtGui.QIcon(self.ctx.get_resource("icon_tw_done.png")), '')
        self.btn_tw_deletedone.setToolTip("Remove all successfully converted items")
        self.btn_tw_log = QtWidgets.QPushButton(QtGui.QIcon(self.ctx.get_resource("icon_tw_log.png")), '')
        self.btn_tw_log.setToolTip("Open the log file")
        self.treewidget = QtWidgets.QTreeWidget()
        self.header_treeview = self.treewidget.header()
        self.treewidget.setHidden(True)
        self.frm_left = FrameCustom(self)  # need treewidget, lbl_placeholder and lyt_icons created

        self.spltr_middle = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.widget_rightSide = QtWidgets.QWidget()  # Widget which contain the 2 frame on the right side
        # Right Frame
        self.frm_exprt_option = QtWidgets.QFrame()
        self.frm_right_targetcs = QtWidgets.QFrame()
        self.lbl_cbb_target = QtWidgets.QLabel('TARGET COLORSPACE')
        self.cbb_target_cs = QtWidgets.QComboBox()
        self.cbb_exprt_odt = QtWidgets.QComboBox()
        self.lbl_exprt_odt = QtWidgets.QLabel(" ODT / TransferFunction")

        self.lbl_exportOptions = QtWidgets.QLabel("Global Export Options")
        self.cbb_exprt_format = QtWidgets.QComboBox()
        self.cbb_exprt_bit = QtWidgets.QComboBox()
        self.cbb_exprt_compress = QtWidgets.QComboBox()
        self.lbl_exprt_format = QtWidgets.QLabel(" format")
        self.lbl_exprt_bitdepth = QtWidgets.QLabel(" bitdepth")
        self.lbl_exprt_compress = QtWidgets.QLabel(" Compression")
        self.spnb_exprt_compress = QtWidgets.QSpinBox()
        self.lbl_exprt_compress_qual = QtWidgets.QLabel("Compression Amount")

        self.rb_exprt_folder = QtWidgets.QRadioButton('Export in a new folder')
        self.rb_exprt_file = QtWidgets.QRadioButton('Export at the same location')
        self.le_exprt_folder = QtWidgets.QLineEdit()
        self.btn_exprt_explorer = QtWidgets.QPushButton(QtGui.QIcon(self.ctx.get_resource("icon_open_2.png")), '')

        # Input Options
        self.frm_right_input = QtWidgets.QFrame()
        self.lbl_in_title = QtWidgets.QLabel("File Input Options")
        self.lbl_in_idt = QtWidgets.QLabel("Source ColorSpace (IDT)")
        self.cbb_in_idt = QtWidgets.QComboBox()
        self.btn_in_apply = QtWidgets.QPushButton('Apply to Selection')
        self.btn_in_apply_all = QtWidgets.QPushButton('Apply to All')

        # Toolbar items
        self.lbl_title = QtWidgets.QLabel('')
        self.widget_spacer = QtWidgets.QWidget()
        self.widget_spacer2 = QtWidgets.QWidget()

    def create_layouts(self):
        self.lyt_main = QtWidgets.QHBoxLayout(self.main_widget)
        self.lyt_main.setMargin(0)
        self.lyt_left_top_icons = QtWidgets.QHBoxLayout(self.widget_left_icons)
        self.lyt_left_top_icons.setContentsMargins(QtCore.QMargins(4, 4, 4, 4))
        self.lyt_lFrame = QtWidgets.QVBoxLayout(self.frm_left)
        self.lyt_lFrame.setSpacing(0)

        self.lyt_rightSide = QtWidgets.QGridLayout(self.widget_rightSide)
        self.lyt_rightSide.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.lyt_rightSide.setSpacing(0)

        self.lyt_frm_exprt_option = QtWidgets.QVBoxLayout(self.frm_exprt_option)
        self.lyt_frm_exprt_option.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.lyt_rFrame_top = QtWidgets.QVBoxLayout(self.frm_right_targetcs)

        self.lyt_exportOpt_grid = QtWidgets.QGridLayout()
        self.lyt_exportOpt_grid.setContentsMargins(QtCore.QMargins(15, 25, 15, 25))
        self.lyt_exportOpt_grid.setVerticalSpacing(0)
        self.lyt_exportOpt_grid.setRowMinimumHeight(3, 15)  # Compress row
        self.lyt_exportOpt_grid.setRowMinimumHeight(6, 15)  # Location row

        self.lyt_exprt_folder = QtWidgets.QHBoxLayout()
        self.lyt_exprt_folder.setSpacing(6)
        self.lyt_exprt_folder.setContentsMargins(QtCore.QMargins(0, 9, 9, 0))
        # self.lyt_exportOpt_grid.setRowMinimumHeight(8, 15)  # Location row

        self.lyt_in_grid = QtWidgets.QGridLayout(self.frm_right_input)
        self.lyt_in_grid.setContentsMargins(QtCore.QMargins(9, 9, 9, 9))

    def add_widgets_to_layouts(self):
        self.setCentralWidget(self.main_widget)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar_top)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbar_opt)
        self.setStatusBar(self.status_bar)
        self.toolbar_top.addWidget(self.lbl_title)

        self.lyt_main.addWidget(self.spltr_middle)

        self.lyt_left_top_icons.addWidget(self.btn_tw_deleteall)
        self.lyt_left_top_icons.addWidget(self.btn_tw_deletedone)
        self.lyt_left_top_icons.addStretch(1)
        self.lyt_left_top_icons.addWidget(self.btn_tw_log)
        self.lyt_lFrame.addWidget(self.widget_left_icons)
        self.lyt_lFrame.addWidget(self.treewidget)
        self.lyt_lFrame.addWidget(self.lbl_placeholder)
        self.lyt_lFrame.setAlignment(QtCore.Qt.AlignHCenter)

        self.lyt_rightSide.addWidget(self.lbl_in_title, 0, 0)
        self.lyt_rightSide.addWidget(self.frm_right_input, 1, 0)
        # self.lyt_in_grid.addWidget(self.lbl_in_title, 0, 0, 1, 1)
        self.lyt_in_grid.addWidget(self.lbl_in_idt, 0, 0, 1, 2)
        self.lyt_in_grid.addWidget(self.cbb_in_idt, 1, 0, 1, 2)
        self.lyt_in_grid.addWidget(self.btn_in_apply, 2, 0)
        self.lyt_in_grid.addWidget(self.btn_in_apply_all, 2, 1)

        self.lyt_rightSide.addWidget(self.lbl_exportOptions, 3, 0)
        self.lyt_rightSide.addWidget(self.frm_exprt_option, 4, 0)
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
        self.lyt_exportOpt_grid.addWidget(self.rb_exprt_folder, 7, 0, 1, 1)
        self.lyt_exportOpt_grid.addWidget(self.rb_exprt_file, 7, 1, 1, 1)
        self.lyt_exportOpt_grid.addLayout(self.lyt_exprt_folder, 8, 0, 1, 2)
        self.lyt_exprt_folder.addWidget(self.le_exprt_folder)
        self.lyt_exprt_folder.addWidget(self.btn_exprt_explorer)

        self.lyt_rightSide.addWidget(self.frm_right_targetcs, 6, 0)
        self.lyt_rFrame_top.addWidget(self.lbl_cbb_target)
        self.lyt_rFrame_top.addWidget(self.cbb_target_cs)
        self.lyt_rFrame_top.addWidget(self.cbb_exprt_odt)
        self.lyt_rFrame_top.addWidget(self.lbl_exprt_odt)

    def modify_widgets(self):
        QtCore.QResource.registerResource(self.ctx.get_resource('qt_resources/icon_ressource.rcc'))
        stylesheet_var = self.stylesheetContent('stylesheet_variations')
        stylesheet_title = self.stylesheetContent('stylesheet_title')
        self.stylesheet_main = self.stylesheetContent('stylesheet')

        # self.status_bar.showMessage("Status Bar Is Ready", 3000)
        self.status_bar.addWidget(self.stat_lbl_item)

        # Styling controls
        self.setStyleSheet(self.stylesheet_main)
        self.frm_left.setStyleSheet("""QFrame{
                border-radius: 4px;
                border: 2px solid rgb(60,60,60);
                background-color: rgb(45, 45, 48);
                alternate-background-color: rgb(25, 25, 25);
                color: #fafafa;
                }""")
        self.main_widget.setStyleSheet(""".QWidget{background: rgb(40, 40, 42);}""")
        self.toolbar_opt.setStyleSheet(stylesheet_var)
        self.lbl_placeholder.setStyleSheet(self.stylesheet_main)
        self.widget_left_icons.setStyleSheet(stylesheet_title)
        self.treewidget.setStyleSheet(self.stylesheet_main)
        self.treewidget.header().setStyleSheet(self.stylesheet_main)
        self.lbl_title.setStyleSheet(stylesheet_title)
        self.lbl_cbb_target.setStyleSheet(stylesheet_title)
        self.cbb_target_cs.setStyleSheet(stylesheet_var)
        self.frm_right_targetcs.setStyleSheet(
            """.QFrame{background-color: rgb(50,50,50) ;margin:0px; border-left: 3px solid rgb(240,237,97);} """)
        self.lbl_exportOptions.setStyleSheet(stylesheet_var)
        self.lbl_in_title.setStyleSheet(stylesheet_var)

        # ToolBar
        title_pix = QtGui.QPixmap(":/root/title.png")
        title_pix = title_pix.scaled(300, 150, QtCore.Qt.KeepAspectRatio,
                                     QtCore.Qt.TransformationMode.SmoothTransformation)
        self.lbl_title.setPixmap(title_pix)
        self.widget_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.widget_spacer2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.toolbar_top.setMovable(False)
        self.toolbar_top.setMinimumHeight(45)
        self.toolbar_opt.setIconSize(QtCore.QSize(40, 40))
        self.toolbar_opt.setMinimumHeight(55)

        # TreeView
        self.btn_tw_deleteall.setIconSize(QtCore.QSize(25, 25))
        self.btn_tw_deleteall.setFixedSize(25, 25)
        self.btn_tw_deletedone.setIconSize(QtCore.QSize(25, 25))
        self.btn_tw_deletedone.setFixedSize(25, 25)
        self.btn_tw_log.setIconSize(QtCore.QSize(25, 25))
        self.btn_tw_log.setFixedSize(25, 25)

        self.frm_left.setAcceptDrops(True)
        self.lbl_placeholder.setAcceptDrops(True)
        self.treewidget.setHeaderHidden(False)
        self.treewidget.setColumnCount(2)
        self.treewidget.setHeaderLabels(['', ' IDT', 'File Name'])
        self.treewidget.setAlternatingRowColors(True)
        self.treewidget.setSortingEnabled(True)
        self.treewidget.setIndentation(0)
        self.treewidget.setUniformRowHeights(True)
        self.treewidget.setMinimumHeight(50)
        self.treewidget.setIconSize(QtCore.QSize(35, 35))
        self.header_treeview.setMinimumSectionSize(39)
        self.treewidget.setColumnWidth(0, 39)
        self.treewidget.setColumnWidth(1, 39)
        self.treewidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.treewidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.spltr_middle.addWidget(self.frm_left)
        self.spltr_middle.addWidget(self.widget_rightSide)
        self.spltr_middle.setSizes([400, 200])
        self.spltr_middle.setHandleWidth(15)
        self.spltr_middle.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                        QtWidgets.QSizePolicy.MinimumExpanding, )

        # ----------------- #
        # Right Frame
        # ----------------- #
        self.lyt_rightSide.setRowMinimumHeight(2, 20)
        self.lyt_rightSide.setRowMinimumHeight(5, 20)

        self.cbb_target_cs.setMinimumHeight(50)
        self.cbb_exprt_odt.setMinimumHeight(30)

        # self.lyt_frm_exprt_option.insertStretch(-1)
        self.lbl_exportOptions.setMinimumHeight(30)
        self.cbb_exprt_format.setMaximumWidth(95)
        self.cbb_exprt_bit.setMaximumWidth(150)
        self.cbb_exprt_format.setMinimumHeight(30)
        self.cbb_exprt_bit.setMinimumHeight(30)
        self.cbb_exprt_compress.setMinimumHeight(30)
        self.spnb_exprt_compress.setMinimumHeight(30)
        self.spnb_exprt_compress.setMaximum(100)
        self.spnb_exprt_compress.setWrapping(True)

        self.lyt_exportOpt_grid.setRowMinimumHeight(1, 30)
        self.rb_exprt_folder.setIconSize(QtCore.QSize(90, 50))
        # self.rb_exprt_file.setFixedSize(25, 25)
        self.rb_exprt_file.setChecked(QtCore.Qt.Checked)
        self.le_exprt_folder.setMinimumHeight(25)
        self.le_exprt_folder.setMinimumWidth(300)
        self.le_exprt_folder.setPlaceholderText('By default ./ACEScg')
        self.btn_exprt_explorer.setFixedSize(25, 25)

        # Inputs options
        self.lbl_in_title.setMinimumHeight(30)
        self.cbb_in_idt.setMinimumHeight(30)
        self.cbb_in_idt.setIconSize(QtCore.QSize(30, 30))
        self.btn_in_apply.setMinimumHeight(30)
        self.btn_in_apply_all.setMinimumHeight(30)
        self.lyt_in_grid.setRowStretch(4, 1)

    # End of base Ui modification

    def abort_convert(self):
        """
        Stop the convert operation (QProgress Dialog)
        """
        self.worker.abort = True
        self.thread.quit()

    def add_actions_to_toolbar(self):

        # Add space before creating actions
        self.toolbar_top.addWidget(self.widget_spacer)

        self.act_info = QtWidgets.QAction(QtGui.QIcon(self.ctx.get_resource("icon_info.png")), "About this app", self)
        self.toolbar_top.addAction(self.act_info)
        self.act_settings = QtWidgets.QAction(QtGui.QIcon(self.ctx.get_resource("icon_settings.png")), "Settings", self)
        # self.toolbar_top.addAction(self.act_settings)

        self.act_open = QtWidgets.QAction(QtGui.QIcon(self.ctx.get_resource("icon_open_2.png")), "Open image", self)
        self.toolbar_opt.addAction(self.act_open)
        self.act_convert = QtWidgets.QAction(QtGui.QIcon(self.ctx.get_resource("icon_convert_2.png")), "Convert", self)
        self.toolbar_opt.addAction(self.act_convert)

        self.toolbar_opt.insertWidget(self.act_convert, self.widget_spacer2)

    def add_cbb_items(self):
        """
        Method to fill comboxbox at initialisation
        """
        self.cbb_target_cs.addItems([k for k in CS_TARGET_DICO.keys()])
        self.cbb_exprt_format.addItems(FORMAT_LIST)
        self.cbb_exprt_bit.addItems([k for k in BITDEPTH_DICO.keys()])
        self.cbb_exprt_bit.setCurrentIndex(2)
        self.cbb_exprt_odt.addItems([k for k in ODT_DICO.keys()])
        for keys in IDT_DICO.keys():
            icon = QtGui.QIcon(IDT_DICO.get(keys)[2])
            self.cbb_in_idt.addItem(icon, keys)
        self.cbb_exprt_compress.addItems([i.capitalize() for i in COMPRESSION_LIST])
        # self.cbb_target_cs.setMaximumHeight()

    def add_tree_widget_item(self, file_path_in):
        file_path = str(Path(file_path_in))
        # Check if an item for the filepath already exists
        existing_items = self.list_tree_items()
        for item in existing_items:
            if file_path == item.text(2):
                return False
        # Add the item to the treeWidget
        file_name = os.path.basename(file_path)
        icon = QtGui.QIcon(":/idt/icon_idt_none.png")
        icon_statut = QtGui.QIcon(":/statut/icon_convert_wait.png")
        item = QtWidgets.QTreeWidgetItem(self.treewidget, ['none', '', file_name, file_path, 'None'])
        item.setIcon(0, icon_statut)
        item.setIcon(1, icon)
        item.setTextAlignment(0, QtCore.Qt.AlignHCenter)
        item.setTextAlignment(1, QtCore.Qt.AlignHCenter)

        self.status_bar_update()

    def apply_idt(self, target):
        """
        Apply the idt to the items with the select target (All or Selection only)

        Args:
            target: True if Selection Only - False if All

        """
        if target:
            sel = self.treewidget.selectedItems()
        else:
            # Loop in the root to get all the child
            sel = self.list_tree_items()

        for tree_item in sel:
            tree_item: QtWidgets.QTreeWidgetItem
            idt = self.cbb_in_idt.currentText()
            tree_item.setText(4, idt)
            icon = QtGui.QIcon(IDT_DICO.get(idt)[2])
            tree_item.setIcon(1, icon)

    # def progress_step(self):
    #     self.prg_dialog.setValue(self.prg_dialog.value() + 1)

    def convert(self):
        out_cs = self.cbb_target_cs.currentText()
        out_format = self.cbb_exprt_format.currentText()
        out_bitdepth = self.cbb_exprt_bit.currentText()
        out_compression = self.cbb_exprt_compress.currentText().lower() + ':' + str(self.spnb_exprt_compress.value())
        out_odt = self.cbb_exprt_odt.currentText()
        out_location = 'file' if self.rb_exprt_file.isChecked() else 'folder'
        out_location_path = self.le_exprt_folder.text()
        resources = self.ctx.get_resource()

        tree_item_list = self.list_tree_items()
        if not any([tree_item.text(4).endswith('None') for tree_item in tree_item_list]):
            if tree_item_list:
                if os.path.exists(out_location_path) or not out_location_path:
                    self.thread = QtCore.QThread(self)
                    self.worker = Worker(tree_item_list, out_location, out_format, out_bitdepth, out_cs, out_odt,
                                         resources, out_compression, out_location_path)

                    self.worker.moveToThread(self.thread)
                    self.worker.file_converted.connect(self.convert_result)
                    self.worker.finished.connect(self.convert_finished)
                    # self.worker.step_converter.connect(self.progress_step)
                    self.thread.started.connect(self.worker.convert_file)
                    self.thread.start()

                    self.prg_dialog = QtWidgets.QProgressDialog("Converting files ...", "Abort", 0, len(tree_item_list),
                                                                self)
                    self.prg_dialog.setStyleSheet(""" background-color: rgb(30,30,30); color: #fafafa; """)
                    # self.prg_dialog.setCancelButton(self.prg_dialog_pushButton())
                    # self.prg_dialog.setContentsMargins(15, 15, 15, 15)
                    self.prg_dialog.canceled.connect(self.abort_convert)
                    self.prg_dialog.show()
                else:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setText("Output folder path doesn't exist")
                    msgbox.exec_()
            else:
                msgbox = QtWidgets.QMessageBox()
                msgbox.setText('No file to convert !')
                msgbox.exec_()
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setText('Some files have unassigned IDT')
            msgbox.exec_()

    def convert_finished(self):
        """

        Called when the converting process is finished

        """
        self.thread.quit()
        self.prg_dialog.setValue(self.prg_dialog.maximum())

    def cbb_update_format(self):
        """
        Is called when the file format cbb change
        """
        export_format = self.cbb_exprt_format.currentText()
        if export_format == '.jpg':
            self.cbb_exprt_bit.clear()
            self.cbb_exprt_bit.addItem('8bit Int')
            self.cbb_exprt_bit.setEnabled(False)
            self.cbb_exprt_compress.clear()
            self.cbb_exprt_compress.addItem('jpeg')
            self.cbb_exprt_compress.setEnabled(False)
            self.spnb_exprt_compress.setEnabled(True)
        elif export_format == '.png':
            self.cbb_exprt_bit.clear()
            self.cbb_exprt_bit.addItems(['8bit Int', '16bit Int'])
            self.cbb_exprt_bit.setEnabled(True)
            self.cbb_exprt_compress.clear()
            self.cbb_exprt_compress.addItem('None')
            self.cbb_exprt_compress.setEnabled(False)
            self.spnb_exprt_compress.setEnabled(False)
        elif export_format == '.exr':
            self.cbb_exprt_bit.clear()
            self.cbb_exprt_bit.addItems(['16bit Half', '32bit Float'])
            self.cbb_exprt_bit.setEnabled(True)
            self.cbb_exprt_compress.clear()
            self.cbb_exprt_compress.addItems([i.capitalize() for i in COMPRESSION_LIST])
            self.cbb_exprt_compress.setEnabled(True)
            self.cbb_exprt_compress.setCurrentText('Zip')
            self.spnb_exprt_compress.setEnabled(False)
        elif export_format == 'Original':
            self.cbb_exprt_bit.clear()
            self.cbb_exprt_bit.addItem('Original')
            self.cbb_exprt_bit.setEnabled(False)
            self.cbb_exprt_compress.clear()
            self.cbb_exprt_compress.addItem('/')
            self.cbb_exprt_compress.setEnabled(False)
            self.spnb_exprt_compress.setEnabled(False)

        if export_format == '.exr' or export_format == 'Original':
            self.cbb_exprt_odt.setEnabled(False)
            self.cbb_exprt_odt.setCurrentText('None')
            self.cbb_exprt_odt.setHidden(True)

            self.lbl_exprt_odt.setHidden(True)

        else:
            self.cbb_exprt_odt.setEnabled(True)
            self.cbb_exprt_odt.setHidden(False)
            self.cbb_exprt_odt.setCurrentText('None')
            self.lbl_exprt_odt.setHidden(False)

    def cbb_udpate_odt(self):
        current_out_cs = self.cbb_target_cs.currentText()
        if current_out_cs != 'ACEScg':
            for i in range(self.cbb_target_cs.count()):
                if self.cbb_exprt_odt.itemText(i).endswith('(ACES)'):
                    self.cbb_exprt_odt.model().item(i).setEnabled(False)
        else:
            for i in range(self.cbb_target_cs.count()):
                if self.cbb_exprt_odt.itemText(i).endswith('(ACES)'):
                    self.cbb_exprt_odt.model().item(i).setEnabled(True)

    def compression_update(self):
        compression = self.cbb_exprt_compress.currentText()
        if compression == 'Dwaa' or compression == 'Dwab':
            self.spnb_exprt_compress.setEnabled(True)
        else:
            self.spnb_exprt_compress.setEnabled(False)

    def convert_result(self, tree_item, result_list):
        """
        Method called each time a file is finished to be converted

        Args:
            tree_item: QtWidgets.QTreeWidgetItem
            result_list: List[Bool, oiio error]

        """
        tree_item: QtWidgets.QTreeWidgetItem
        self.prg_dialog.setValue(self.prg_dialog.value() + 1)
        if all(result_list):
            icon_check = QtGui.QIcon(":/statut/icon_convert_check.png")
            tree_item.setIcon(0, icon_check)
            tree_item.setText(0, 'check')
            # self.treewidget.takeTopLevelItem(self.treewidget.indexOfTopLevelItem(tree_item))
        else:
            icon_error = QtGui.QIcon(":/statut/icon_convert_error.png")
            tree_item.setIcon(0, icon_error)
            tree_item.setText(0, 'error')
            logging.error(f"File not converted: {tree_item.text(3)}")

        self.status_bar_update()

    def delete_tree_items_selected(self):
        selection = self.treewidget.selectedItems()
        for tree_items in selection:
            self.treewidget.takeTopLevelItem(self.treewidget.indexOfTopLevelItem(tree_items))

        self.status_bar_update()

    def icons_treewidget_actions(self, action):
        if action == "all":
            self.treewidget.clear()
            self.status_bar_update()

        elif action == "done":
            root = self.treewidget.invisibleRootItem()
            item_list = []
            for i in range(root.childCount()):
                item_list.append(self.treewidget.topLevelItem(i))

            for items in item_list:
                if items.text(0) == 'check':
                    index = self.treewidget.indexOfTopLevelItem(items)
                    self.treewidget.takeTopLevelItem(index)

            self.status_bar_update()

        elif action == "log":
            document_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
            pyco_path = os.path.join(document_path, 'PYCO', 'ColorspaceConverter')
            if os.path.exists(pyco_path):
                pyco_file_path = os.path.join(pyco_path, 'log_file.log')
                if os.path.exists(pyco_file_path):
                    print("PATH:", pyco_file_path)
                    webbrowser.open(pyco_file_path)

    def load_fonts(self):
        path1 = self.ctx.get_resource("font/JosefinSans-SemiBold.ttf")
        path2 = self.ctx.get_resource("font/JosefinSans-Medium.ttf")
        path3 = self.ctx.get_resource("font/JosefinSans-Bold.ttf")
        path4 = self.ctx.get_resource("font/JetBrainsMono-Regular.ttf")
        font_load1 = QtGui.QFontDatabase.addApplicationFont(path1)
        font_load2 = QtGui.QFontDatabase.addApplicationFont(path2)
        font_load3 = QtGui.QFontDatabase.addApplicationFont(path3)
        font_load4 = QtGui.QFontDatabase.addApplicationFont(path4)

    def list_tree_items(self):
        """

        Returns: QtWidgets.QTreeWidgetItem List

        """
        items_list = []
        root = self.treewidget.invisibleRootItem()
        child_root_n = root.childCount()
        for i in range(child_root_n):
            items_list.append(root.child(i))
        return items_list

    def open_file(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.exr *.jpg *.hdr *.jpeg *.tiff *.tif)")

        if dialog.exec_():
            self.lbl_placeholder.setHidden(True)
            self.treewidget.setHidden(False)
            self.widget_left_icons.setHidden(False)
            filenames = dialog.selectedFiles()
            for file_path in filenames:
                self.add_tree_widget_item(file_path)

    def open_folder(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        # dialog.setNameFilter("Images (*.png *.exr *.jpg *.hdr *.jpeg *.tiff *.tif)")
        if dialog.exec_():
            folder = dialog.selectedFiles()[0]
            self.le_exprt_folder.setText(folder)

    def open_info_wind(self):
        self.wind_info = InfoWindow(self.main_widget, self.ctx)
        self.wind_info.exec_()

    @staticmethod
    def prg_dialog_pushButton():
        btn = QtWidgets.QPushButton('Abort')
        btn.setMinimumSize(70, 40)
        btn.setContentsMargins(QtCore.QMargins(15, 15, 15, 15))
        return btn

    def rb_update_location(self):
        if self.rb_exprt_file.isChecked():
            self.le_exprt_folder.setVisible(False)
            self.btn_exprt_explorer.setVisible(False)
        else:
            self.le_exprt_folder.setVisible(True)
            self.btn_exprt_explorer.setVisible(True)

    def select_all_tree_items(self):
        self.treewidget.selectAll()

    def setup_connections(self):
        self.act_convert.triggered.connect(self.convert)
        self.act_info.triggered.connect(self.open_info_wind)
        self.act_open.triggered.connect(self.open_file)

        self.btn_tw_deleteall.clicked.connect(partial(self.icons_treewidget_actions, "all"))
        self.btn_tw_deletedone.clicked.connect(partial(self.icons_treewidget_actions, "done"))
        self.btn_tw_log.clicked.connect(partial(self.icons_treewidget_actions, "log"))

        self.btn_in_apply.clicked.connect(partial(self.apply_idt, True))
        self.btn_in_apply_all.clicked.connect(partial(self.apply_idt, False))
        self.cbb_target_cs.currentTextChanged.connect(self.cbb_udpate_odt)
        self.cbb_exprt_format.currentTextChanged.connect(self.cbb_update_format)
        self.cbb_exprt_compress.currentTextChanged.connect(self.compression_update)

        self.rb_exprt_file.toggled.connect(self.rb_update_location)
        self.rb_exprt_folder.toggled.connect(self.rb_update_location)
        self.btn_exprt_explorer.clicked.connect(self.open_folder)

        QtWidgets.QShortcut(QtGui.QKeySequence('Delete'), self, self.delete_tree_items_selected)
        QtWidgets.QShortcut(QtGui.QKeySequence('Backspace'), self, self.delete_tree_items_selected)
        QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+A'), self, self.select_all_tree_items)

    def status_bar_update(self):
        root = self.treewidget.invisibleRootItem()
        child_root_n = root.childCount()
        self.stat_lbl_item.setText(f"  Files to convert: {child_root_n}  ")

    def stylesheetContent(self, name):
        main_yellow = '#E0D43D'
        css_file = self.ctx.get_resource(f"{name}.css")
        with open(css_file, "r") as f:
            content = f.read()
        return content
