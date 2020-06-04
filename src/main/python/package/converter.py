import os

import colour
from oiio import OpenImageIO as oiio

from OIIO import ImageInput, ImageOutput


class Converter:
    def __init__(self):
        pass

    def image_processing(self, img_path, bit_depth):
        image_RGB = colour.read_image(img_path)
        input_colourspace = colour.RGB_COLOURSPACES['sRGB']
        output_colourspace = colour.RGB_COLOURSPACES['ACEScg']

        # image_XYZ = colour.sRGB_to_XYZ(image_RGB)
        converted = self.rgb_to_rgb_conversion(image_RGB, input_colourspace, output_colourspace)
        result = colour.io.convert_bit_depth(converted, bit_depth=bit_depth)
        final_image = result
        # final_image = image_XYZ
        out_path = os.path.join(os.path.dirname(img_path), "testBobRoss_acesccg_lin_f16.exr")
        self.result = colour.io.write_image_Imageio(final_image, out_path)

    @staticmethod
    def rgb_to_rgb_conversion(in_rgb, in_cs, out_cs, cat='CAT02', cctf_decode=True):
        result = colour.RGB_to_RGB(in_rgb, in_cs, out_cs, chromatic_adaptation_transform=cat,
                                   apply_cctf_decoding=cctf_decode)
        return result

    def compute_image(self, image_path, out_name='default.exr', w_format=oiio.UNKNOWN):
        img_in = ImageInput.open(image_path)
        img_specs = img_in.spec()
        rgb_data = img_in.read_image()
        self.write_image(rgb_data, out_name, w_format, img_specs)
        img_in.close()

    @staticmethod
    def write_image(rgb_data, filename, w_format, spec):
        output = ImageOutput.create(filename=filename)
        output.open(filename, spec)
        output.write(rgb_data, w_format)
        output.close()


if __name__ == '__main__':
    img_path = r"E:\Images\bob-ross-9464216-1-402.jpg"
    c = Converter()
    c.compute_image(img_path, 'bobross.exr', oiio.FLOAT)
