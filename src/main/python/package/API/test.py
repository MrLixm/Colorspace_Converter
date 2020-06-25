"""
File for running test with colour and OIIO
"""
import os
from pathlib import Path
import colour
from package.data_list import CS_TARGET_DICO, FORMAT_LIST, BITDEPTH_DICO, ODT_DICO, IDT_DICO, COMPRESSION_LIST
from PySide2 import QtCore


class Window:
    def __init__(self):
        print("WIndow init")
        self.cust = Custom(self)
        self.fruit_list = ["Apple"]

    def add_item(self, name):
        self.fruit_list.append(name)
        print("Item added:", self.fruit_list)

    def run_foo(self):
        self.cust.foo()

    def display_list(self):
        print(self.fruit_list)


class Custom:
    def __init__(self, parent):
        print("Custom init")
        self.parent = parent

    def foo(self):
        name = input("Enter name:")
        self.parent.add_item(name)


path_1 = "L:/SCRIPT/Colour/OCIO_converter/design/output_design//icon_idt_v2\icon_idt_acescc.png"
path_2 = "L:/SCRIPT/Colour/OCIO_converter/design/output_design/icon_idt_v2/icon_idt_acescc.png "


def foopath():
    var1 = Path(path_1)
    var2 = Path(path_2)
    print(str(var1), type(str(var1)))
    print(var2, type(var2))


if __name__ == '__main__':
    # foopath()
    # result = colour.RGB_COLOURSPACES['sRGB'].whitepoint
    # result2 = colour.RGB_COLOURSPACES['ACEScg'].whitepoint
    # result3 = colour.RGB_COLOURSPACES['ITU-R BT.709'].whitepoint
    # print("sRGB", result)
    # print("ACEScg", result2)
    # print("rec709", result3)
    # print(colour.ILLUMINANTS_SDS['D60'])
    document_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
    pyco_path = os.path.join(document_path, 'PYCO', 'ColorspaceConverter')

    result = pyco_path

    print(result)
    print(type(result))
