import os
from pprint import pprint

import colour
from oiio import OpenImageIO as oiio

from package.data_list import ODT_DICO, BITDEPTH_DICO


class Converter:
    def __init__(self, in_img_path, out_location, out_format, out_bitdepth, in_cs, out_cs,
                 odt, resources_path, compression):
        """

        Args:
            in_img_path: path\name.ext of the file
            out_location: 'file' or 'folder'
            out_format: file extension like '.jpg'
            out_bitdepth: bitdepth for the output file: uint8,uint16,half,float, original
            in_cs: source colorspace
            out_cs: target colorspace
            odt: the Output Display Transform to apply (False if not wanted)
            compression: Compression method for exr: none, rle, zip, zips, piz, pxr24, b44, b44a, dwaa, or dwab
        """
        self.resources_path = resources_path
        self.out_filePath = self.pathGeneration(in_img_path, out_location, out_format)
        self.in_img_path = in_img_path
        self.out_bitdepth = out_bitdepth
        self.in_cs = in_cs
        self.out_cs = out_cs
        self.odt = odt
        self.compression = compression

        self.errors = self.image_processing()
        print("Errors:", errors)

    def image_processing(self):
        # Read Image
        in_img_data = oiio.ImageInput.open(self.in_img_path)
        if not in_img_data:
            return oiio.geterror()
        spec = in_img_data.spec()
        spec.attribute("compression", self.compression.lower())
        spec.attribute("oiio:ColorSpace", self.out_cs)
        pixels = in_img_data.read_image()
        in_img_data.close()

        # # Convert the rgb data
        # final_image = self.colourConversion(pixels, self.in_cs, self.out_cs, odt=self.odt)
        #
        # # pick the output file bitdepth format
        # spec.format = self.bitdepth_picker(spec.format, self.out_bitdepth)
        #
        # output = oiio.ImageOutput.create(self.out_filePath)
        # if not output:
        #     return[False, oiio.geterror()]
        # output.open(self.out_filePath, spec)
        # writing = output.write_image(final_image)
        # if not writing:
        #     return [False, oiio.geterror()]
        # output.close()

    def apply_odt(self, in_rgb, odt):
        lut_path = os.path.join(self.resources_path, "luts")
        lut_list = ODT_DICO.get(odt)
        lut_1 = colour.io.read_LUT_SonySPI3D(os.path.join(lut_path, lut_list[0]))
        lut_2 = colour.io.read_LUT_SonySPI3D(os.path.join(lut_path, lut_list[1]))
        apply_lut_1 = lut_1.apply(in_rgb)
        apply_lut_2 = lut_2.apply(apply_lut_1)
        return apply_lut_2

    @staticmethod
    def bitdepth_picker(in_bitdepth, out_bitdepth):
        if BITDEPTH_DICO.get(out_bitdepth) == 'original':
            output = in_bitdepth
        else:
            output = BITDEPTH_DICO.get(out_bitdepth)
        return output

    def colourConversion(self, in_rgb, in_cs, out_cs, cctf=False, cat='Bradford', odt=None):
        if in_cs != out_cs:
            input_colourspace = colour.RGB_COLOURSPACES[in_cs]
            output_colourspace = colour.RGB_COLOURSPACES[out_cs]
            cat = cat
            conversion_rgb = colour.RGB_to_RGB(in_rgb, input_colourspace, output_colourspace,
                                               chromatic_adaptation_transform=cat,
                                               apply_cctf_decoding=cctf)
        else:
            conversion_rgb = in_rgb
        if ODT_DICO.get(odt):
            odt_rgb = self.apply_odt(conversion_rgb, odt=odt)
            result = odt_rgb
        else:
            result = conversion_rgb
        return result

    @staticmethod
    def pathGeneration(in_path, out_location='file', out_format='.exr'):
        file_folder_path = os.path.dirname(in_path)
        filename_original = os.path.splitext(os.path.basename(in_path))[0]
        file_ext = os.path.splitext(in_path)[1]
        if out_format.lower() == 'original':
            out_ext = file_ext
        else:
            out_ext = out_format
        out_file_name = "oiio_" + filename_original + '_ACEScg' + out_ext

        if out_location == 'file':
            output_path = os.path.join(file_folder_path, out_file_name)
            return output_path
        if out_location == 'folder':
            aces_folder_path = os.path.join(file_folder_path, 'ACEScg')
            if not os.path.exists(aces_folder_path):
                os.makedirs(aces_folder_path)
            output_path = os.path.join(aces_folder_path, out_file_name)
            return output_path


if __name__ == '__main__':
    filename2 = r"L:\SCRIPT\Colour\OCIO_converter\tests\artist_workshop_4k.hdr"
    filename = r"L:\SCRIPT\Colour\OCIO_converter\tests\odt_test\cabin_render_original.exr"
    # Converter(filename, 'file', '.exr', '16bit Half', 'sRGB', 'ACEScg', 'None',
    #           r'L:\SCRIPT\Colour\OCIO_converter\script\github\OCIO_Converter\src\main\resources\base')

    Converter(filename, 'file', '.png', '16bit Int', 'ACEScg', 'ACEScg', 'None',
              r'L:\SCRIPT\Colour\OCIO_converter\script\github\OCIO_Converter\src\main\resources\base', "None")
