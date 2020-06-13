
from PySide2 import QtWidgets, QtCore, QtGui


class InfoWindow(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(150, 150)
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.edit = QtWidgets.QLineEdit("Write my name here")
        self.button = QtWidgets.QPushButton("Show Greetings")
        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)

    def modify_widgets(self):
        pass

    def create_layouts(self):
        pass

    def add_widgets_to_layouts(self):
        pass

    def setup_connections(self):
        pass
