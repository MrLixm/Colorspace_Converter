"""
File for running test with colour and OIIO
"""
import os
from pathlib import Path
import colour
from package.data_list import CS_TARGET_DICO, FORMAT_LIST, BITDEPTH_DICO, ODT_DICO, IDT_DICO, COMPRESSION_LIST
from PySide2 import QtCore
from oiio import OpenImageIO as oiio


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


def converter(filepath):
    out_filePath= r'L:\temp\xyz\converted_v2.jpg'
    in_buf_data = oiio.ImageBuf(filepath)
    in_buf_roi = oiio.get_roi(in_buf_data.spec())

    in_buf_rgb = oiio.ImageBufAlgo.channels(in_buf_data, (0, 1, 2))  # Remove other channels(multi-channels exr)

    in_array_rgb = in_buf_rgb.get_pixels()

    colourspace_acescg = colour.RGB_COLOURSPACES['ACEScg']
    colourspace_srgb = colour.RGB_COLOURSPACES['sRGB']
    # conversion = colour.XYZ_to_sRGB(in_array_rgb)
    conversion = colour.XYZ_to_RGB(in_array_rgb, colourspace_acescg.whitepoint, colourspace_acescg.whitepoint,
                                   colourspace_acescg.XYZ_to_RGB_matrix)
    conversion_srgb = colour.RGB_to_RGB(conversion, colourspace_acescg, colourspace_srgb, 'Bradford', apply_cctf_encoding= True)

    converted_array_rgba = conversion_srgb
    in_buf_rgb.set_pixels(in_buf_roi, converted_array_rgba)  # Replace the buffer with the converted pixels
    if in_buf_data.spec().alpha_channel > 0:  # If image has an alpha channel
        in_buf_alpha = oiio.ImageBufAlgo.channels(in_buf_data, (3,))  # copy the Alpha channel
        in_buf_rgba = oiio.ImageBufAlgo.channel_append(in_buf_rgb, in_buf_alpha)  # Merge the alpha channel back
    else:
        in_buf_rgba = in_buf_rgb

    in_buf_rgba.specmod().attribute("compression", "jpg:100")
    in_buf_rgba.specmod().attribute("oiio:ColorSpace", 'sRGB')
    bitdepth = 'uint8'
    in_buf_rgba.set_write_format(bitdepth)
    in_buf_rgba.write(out_filePath)


if __name__ == '__main__':
    # foopath()
    # result = colour.RGB_COLOURSPACES['sRGB'].whitepoint
    # result2 = colour.RGB_COLOURSPACES['ACEScg'].whitepoint
    # result3 = colour.RGB_COLOURSPACES['ITU-R BT.709'].whitepoint
    # print("sRGB", result)
    # print("ACEScg", result2)
    # print("rec709", result3)
    # print(colour.ILLUMINANTS_SDS['D60'])
    # document_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
    # pyco_path = os.path.join(document_path, 'PYCO', 'ColorspaceConverter')
    #
    # result = pyco_path
    #
    # print(result)
    # print(type(result))

    converter(r"L:\temp\xyz\test0.exr")
