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
        self.ctx = ctx
        self.treeview = treeview
        self.lbl_placeholder = lbl_placeholder
        self.setAcceptDrops(True)
        QtCore.QResource.registerResource(self.ctx.get_resource('qt_resources/icon_ressource.rcc'))

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
            if os.path.isdir(file_path):
                folder_file_list = [i for i in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, i))]
                full_folder_file_list = [os.path.join(r, files) for r, d, f in os.walk(file_path) for files in f]

            else:
                file_name = os.path.basename(file_path)
                icon = QtGui.QIcon(":/idt/icon_idt_none.png")
                item = QtWidgets.QTreeWidgetItem(self.treeview, ['img', '  ', file_name, file_path])
                item.setIcon(1, icon)
                item.setTextAlignment(1, QtCore.Qt.AlignHCenter)
                item.setBackground(1,QtGui.QBrush(QtGui.QColor(30, 127, 30)))
            # item.data = ['None', file_path]
