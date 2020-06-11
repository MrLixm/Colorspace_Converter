"""
Create the GUI
"""
import os

from PySide2 import QtWidgets
from package.data_list import SUPPORTED_IN_FORMAT


class FrameCustom(QtWidgets.QFrame):
    def __init__(self, treeview, lbl_placeholder):
        super().__init__()
        self.treeview = treeview
        self.lbl_placeholder = lbl_placeholder
        self.drag_file_list = []
        self.setAcceptDrops(True)

    def dragEnterEvent(self, drag_event):
        if drag_event.mimeData().hasUrls():
            drag_event.accept()
        else:
            drag_event.ignore()

    def dragLeaveEvent(self, drag_event):
        pass

    def dragMoveEvent(self, drag_event):
        pass

    def dropEvent(self, drop_event):
        if drop_event.mimeData().hasUrls():
            urls_list = drop_event.mimeData().urls()
            self.drag_file_list = [i.toLocalFile() for i in urls_list if os.path.splitext(i)[1] in SUPPORTED_IN_FORMAT]
            if self.drag_file_list:
                self.import_files()

    def import_files(self):
        self.lbl_placeholder.setHidden(True)
        self.treeview.setHidden(False)
        print(self.drag_file_list)
