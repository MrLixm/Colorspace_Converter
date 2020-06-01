from PySide2 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx

        self.setWindowTitle("OCIO Converter")
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()

    def modify_widgets(self):
        css_file = self.ctx.get_resource("stylesheet.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

    def create_layouts(self):
        self.lyt_main = QtWidgets.QVBoxLayout(self.main_widget)

    def add_widgets_to_layouts(self):
        self.setCentralWidget(self.main_widget)

    def setup_connections(self):
        pass
