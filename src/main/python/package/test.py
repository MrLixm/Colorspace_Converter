import os
from pprint import pprint

from oiio import OpenImageIO as oiio
import colour


def test_func(filepath, outpath):
    in_img = oiio.ImageInput.open(filepath)
    if not in_img:
        return oiio.geterror()
    spec = in_img.spec()
    pixels = in_img.read_image()
    in_img.close()

    print(f"resolution {spec.width} x {spec.height}")

    converted_rgb = pixels
    final_image = converted_rgb

    spec.format = 'half'
    output = oiio.ImageOutput.create(outpath)
    output.open(outpath, spec)
    output.write_image(converted_rgb)
    output.close()
    return spec


if __name__ == '__main__':
    in_path = r"L:\SCRIPT\Colour\OCIO_converter\tests\ber_hdri\ber_terminal_original.hdr"
    out_path = r"L:\SCRIPT\Colour\OCIO_converter\tests\ber_hdri\oiio_ber_v2_half.exr"
    # print(test_func(in_path, out_path).format)
    pprint(colour.RGB_COLOURSPACES['REDcolor'])
