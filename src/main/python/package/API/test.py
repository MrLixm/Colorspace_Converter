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

row_dico_1 = {
    'black': [1, (0, 0, 0)],
    'dark grey': [2, (.2, .2, .2)],
    'light grey': [3, (.6, .6, .6)]
}
wv= 25
for item in row_dico_1.keys():
    cmds.button(lbl='', ann= row_dico_1.get(item)[0], w= wv, cmd=)


cmds.button(label='', ann='dark green', width=wv, command=partial(setNurbOverrideColor,7), bgc=(.3,.6,.3))
cmds.button(label='', ann='soft green', width=wv, command=partial(setNurbOverrideColor,23), bgc=(.4,.7,.4))
cmds.button(label='', ann='lime green', width=wv, command=partial(setNurbOverrideColor,26), bgc=(.6,.8,.4))
cmds.button(label='', ann='light green', width=wv, command=partial(setNurbOverrideColor,14), bgc=(.4,.9,.2))
cmds.button(label='', ann='light green', width=wv, command=partial(setNurbOverrideColor,27), bgc=(.4,.8,.4))
cmds.button(label='', ann='light green', width=wv, command=partial(setNurbOverrideColor,19), bgc=(.6,1,.7))

cmds.button(label='', ann='dark purple', width=wv, command=partial(setNurbOverrideColor,30), bgc=(.4,.3,.7))
cmds.button(label='', ann='navy', width=wv, command=partial(setNurbOverrideColor,15), bgc=(.2,.3,.5))
cmds.button(label='', ann='dark blue', width=wv, command=partial(setNurbOverrideColor,5), bgc=(.2,.2,.7))
cmds.button(label='', ann='blue', width=wv, command=partial(setNurbOverrideColor,6), bgc=(.2,.3,1))
cmds.button(label='', ann='soft blue', width=wv, command=partial(setNurbOverrideColor,29), bgc=(.4,.5,.6))
cmds.button(label='', ann='light blue', width=wv, command=partial(setNurbOverrideColor,18), bgc=(.6,.7,1))
cmds.button(label='', ann='soft light blue', width=wv, command=partial(setNurbOverrideColor,28), bgc=(.3,.8,.8))
cmds.setParent('..')

