import webbrowser
from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui


class InfoWindow(QtWidgets.QDialog):
    def __init__(self, parent, ctx):
        super().__init__(parent)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
        self.setFixedSize(300, 400)
        self.appversion = ctx.build_settings['version']
        self.setup_ui()
        self.setBackgroundRole(QtGui.QPalette.Mid)
        self.setWindowTitle("Info")

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.create_social()
        self.modify_widgets()
        self.setup_connections()

    def create_widgets(self):
        self.lbl_title = QtWidgets.QLabel(f"Image Colorspace Convert v{self.appversion}")
        self.btn_madeby = QtWidgets.QPushButton("Developed by Liam Collod")

        self.lbl_request = QtWidgets.QLabel(
            "Bug/Feature request: <a href= mailto:monsieurlixm@gmail.com style=color:rgb(36,221,121) "
            "style=text-decoration:none >monsieurlixm@gmail.com</a>")

        self.btn_doc = QtWidgets.QPushButton("Documentation")
        self.wdgt_line = QtWidgets.QWidget()
        self.lbl_thanks = QtWidgets.QLabel("""Made possible thanks to : """)
        self.lbl_thanks_color = QtWidgets.QLabel("<a href=https://www.colour-science.org style=color:rgb(36,221,121) "
                                                 "style=text-decoration:none > - Colour-Science Python Package - </a>")
        self.lbl_thanks_fred = QtWidgets.QLabel(
            "<a href=https://github.com/fredrikaverpil/oiio-python style=color:rgb(36,221,121) "
            "style=text-decoration:none > - Fredrik Averpil's Work -</a>")

    def modify_widgets(self):
        stylesheet = """
            QDialog{background-color: rgb(50,50,50);
            color: #fafafa;
            border: 1px solid rgb(36,221,121);
            }
        
        """
        stylesheet_title = """
            font-family: Josefin Sans;
            font-size: 15px;
            color: #fafafa;
        """
        stylesheet_line = """
            background-color: rgb(90,90,90);

        """
        self.setStyleSheet(stylesheet)
        self.lyt_v_main.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setStyleSheet(stylesheet_title)
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.btn_madeby.setMinimumHeight(25)
        self.btn_madeby.setEnabled(False)
        self.btn_doc.setMinimumHeight(30)
        self.lbl_request.setOpenExternalLinks(True)
        self.wdgt_line.setStyleSheet(stylesheet_line)
        self.wdgt_line.setMinimumHeight(1)
        self.lbl_thanks_color.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_thanks_color.setOpenExternalLinks(True)
        self.lbl_thanks_fred.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_thanks_fred.setOpenExternalLinks(True)

    def create_layouts(self):
        self.lyt_v_main = QtWidgets.QVBoxLayout()
        self.lyt_social = QtWidgets.QHBoxLayout()

    def create_social(self):
        icon_list = {'twitter': 'https://twitter.com/MrLixm',
                     'artstation': 'https://www.artstation.com/monsieur_lixm',
                     'linkedin':  'https://www.linkedin.com/in/liam-collod/',
                     'github': 'https://github.com/MrLixm/Colorspace_Converter',
                     'gumroad': 'https://gumroad.com/liam_collod'
                     }
        for item in icon_list.keys():
            lbl = QtWidgets.QPushButton()
            icon = QtGui.QIcon(f':/social/icon_social_{item}.png')
            lbl.setIcon(icon)
            lbl.setFixedSize(25 , 25)
            lbl.clicked.connect(partial(self.open_social, icon_list.get(item)))
            lbl.setStyleSheet(""" QPushButton{ background-color: transparent;}
             QPushButton:hover{ background-color: rgb(80,80,80);}}
            """)
            self.lyt_social.addWidget(lbl)

    def open_social(self, link):
        webbrowser.open(link)

    def add_widgets_to_layouts(self):
        self.setLayout(self.lyt_v_main)
        self.lyt_v_main.addWidget(self.lbl_title)
        self.lyt_v_main.addWidget(self.btn_madeby)
        self.lyt_v_main.addLayout(self.lyt_social)
        self.lyt_v_main.addWidget(self.btn_doc)
        self.lyt_v_main.addWidget(self.lbl_request)
        self.lyt_v_main.addWidget(self.wdgt_line)
        self.lyt_v_main.addWidget(self.lbl_thanks)
        self.lyt_v_main.addWidget(self.lbl_thanks_color)
        self.lyt_v_main.addWidget(self.lbl_thanks_fred)

    def setup_connections(self):
        self.btn_doc.clicked.connect(partial(self.open_social,
                                               'https://mrlixm.github.io/PYCO/standalone/ColorspaceConvert/home/'))
