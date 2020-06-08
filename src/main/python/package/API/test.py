import os
from pprint import pprint

from oiio import OpenImageIO as oiio
import colour
from package.data_list import ODT_DICO


# class Test:
def colourConversion(odt=None):
    if ODT_DICO.get(odt):
        print("Start apply odt")
        apply_odt(odt=odt)
        result = 'string'
    else:
        print("No odt applied")
        result = True
    return result


def apply_odt(odt):
    lut_list = ODT_DICO.get(odt)
    print(lut_list)

if __name__ == '__main__':
    in_path = r"L:\SCRIPT\Colour\OCIO_converter\tests\ber_hdri\ber_terminal_original.hdr"
    out_path = r"L:\SCRIPT\Colour\OCIO_converter\tests\ber_hdri\oiio_ber_v2_half.exr"

    colourConversion(odt='sRGB(ACES)')
    # pprint(colour.RGB_COLOURSPACES['REDcolor'])
