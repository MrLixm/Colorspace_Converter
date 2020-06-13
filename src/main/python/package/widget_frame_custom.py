"""
Create the GUI
"""
import os
import glob

from PySide2 import QtWidgets, QtCore, QtGui
from package.data_list import SUPPORTED_IN_FORMAT


class FrameCustom(QtWidgets.QFrame):
    def __init__(self, ctx, treeview, lbl_placeholder):
        super().__init__()
        treeview: QtWidgets.QTreeWidget
        lbl_placeholder: QtWidgets.QLabel
        self.ctx = ctx
        self.treeview = treeview
        self.lbl_placeholder = lbl_placeholder

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

    def add_tree_item(self, file_path):
        if os.path.isdir(file_path):
            # TODO: Implement folder
            # Return direct child file in the folder:
            folder_file_list = [i for i in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, i))]
            # Return all the file in the subfolder:
            full_folder_file_list = [os.path.join(r, files) for r, d, f in os.walk(file_path) for files in f]

        else:
            file_name = os.path.basename(file_path)
            icon = QtGui.QIcon(":/idt/icon_idt_none.png")
            item = QtWidgets.QTreeWidgetItem(self.treeview, ['', file_name, file_path, 'None'])
            item.setIcon(0, icon)
            item.setTextAlignment(0, QtCore.Qt.AlignHCenter)

            # item.setBackground(0, QtGui.QBrush(QtGui.QColor(30, 127, 30)))

    def check_item_exists(self):
        pass

