"""
Create the GUI
"""
import os
import glob
from pathlib import Path

from PySide2 import QtWidgets, QtCore, QtGui
from package.data_list import SUPPORTED_IN_FORMAT
# from package.main_window import MainWindow


class FrameCustom(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__()
        parent: MainWindow
        treeview: QtWidgets.QTreeWidget
        lbl_placeholder: QtWidgets.QLabel
        self.ctx = parent.ctx
        self.treeview = parent.treewidget
        self.lbl_placeholder = parent.lbl_placeholder
        self.mainWind = parent

        QtCore.QResource.registerResource(self.ctx.get_resource('qt_resources/icon_ressource.rcc'))
        self.setAcceptDrops(True)

    def dragEnterEvent(self, drag_event):
        mime = drag_event.mimeData()
        if mime.hasUrls():
            # if the input contain supported format or folder
            if any([os.path.splitext(url.toLocalFile())[1] in SUPPORTED_IN_FORMAT or os.path.isdir(url.toLocalFile())
                    for url in mime.urls()]):
                drag_event.accept()
            else:
                drag_event.ignore()
        else:
            drag_event.ignore()

    def dragLeaveEvent(self, drag_event):
        pass

    def dragMoveEvent(self, drag_event):
        pass

    def dropEvent(self, drop_event):
        if drop_event.mimeData().hasUrls():
            urls_list = drop_event.mimeData().urls()
            self.drag_file_list = []
            for url in urls_list:
                url = url.toLocalFile()
                if os.path.splitext(url)[1] in SUPPORTED_IN_FORMAT or os.path.isdir(url):
                    self.drag_file_list.append(url)
            if self.drag_file_list:
                self.import_files()

    def import_files(self):
        self.lbl_placeholder.setHidden(True)
        self.treeview.setHidden(False)
        for file_path in self.drag_file_list:
            self.add_tree_item(file_path)

    def add_tree_item(self, file_path_in):
        if os.path.isdir(file_path_in):
            # Return direct child file in the folder:
            folder_file_list = [i for i in os.listdir(file_path_in) if os.path.isfile(os.path.join(file_path_in, i))]
            # Return all the file in the subfolder:
            full_folder_file_list = [os.path.join(r, files) for r, d, f in os.walk(file_path_in) for files in f]
            for file_path_item in full_folder_file_list:
                self.mainWind.add_tree_widget_item(file_path_item)
        else:
            self.mainWind.add_tree_widget_item(file_path_in)
            # item.setBackground(0, QtGui.QBrush(QtGui.QColor(30, 127, 30)))


