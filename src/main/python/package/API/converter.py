import os

import colour
from colour.algebra import table_interpolation_tetrahedral
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
        self.out_format = out_format
        self.out_filePath = self.pathGeneration(in_img_path, out_location, out_format)
        self.in_img_path = in_img_path
        self.out_bitdepth = out_bitdepth
        self.in_cs = in_cs
        self.out_cs = out_cs
        self.odt = odt
        self.compression = compression

        self.errors = self.image_processing()
        print("Errors:", self.errors)

    def image_processing(self):
        # Read Image
        in_buf_data = oiio.ImageBuf(self.in_img_path)
        in_buf_roi = oiio.get_roi(in_buf_data.spec())
        if in_buf_data.has_error:
            return in_buf_data.geterror()

        in_buf_rgb = oiio.ImageBufAlgo.channels(in_buf_data, (0, 1, 2))  # Remove other channels(multi-channels exr)
        if in_buf_rgb.has_error:
            return in_buf_rgb.geterror()

        in_array_rgb = in_buf_rgb.get_pixels()
        converted_array_rgba = self.pixel_processing(in_array_rgb)  # Apply colorspace conversion & various
        in_buf_rgb.set_pixels(in_buf_roi, converted_array_rgba)  # Replace the buffer with the converted pixels

        bitdepth = self.bitdepth_picker(in_buf_data.nativespec().format, self.out_bitdepth)
        in_buf_rgb.specmod().attribute("compression", self.compression.lower())
        in_buf_rgb.specmod().attribute("oiio:ColorSpace", self.out_cs if not ODT_DICO.get(self.odt) else self.odt)

        in_buf_rgb.set_write_format(bitdepth)
        in_buf_rgb.write(self.out_filePath)

    def apply_odt_aces(self, in_rgb):
        """

        Args:
            in_rgb: pixel data as numpy array

        Returns: pixel data as numpy array with odt applied

        """
        lut_path = os.path.join(self.resources_path, "luts")
        lut_list = ODT_DICO.get(self.odt)

        # Convert from ACEScg to ACES2065-1
        in_rgb_ap0 = colour.RGB_to_RGB(in_rgb, colour.RGB_COLOURSPACES['ACEScg'], colour.RGB_COLOURSPACES['ACES2065-1'],
                                       chromatic_adaptation_transform='Bradford',
                                       apply_cctf_decoding=False)

        lut_rrt = colour.io.read_LUT_SonySPI3D(os.path.join(lut_path, lut_list[0]))
        lin_to_log = colour.models.log_encoding_ACEScc(in_rgb_ap0)
        log_to_rrt = lut_rrt.apply(lin_to_log, interpolator=table_interpolation_tetrahedral)
        return log_to_rrt

    def apply_odt(self, in_rgb):
        if ODT_DICO.get(self.odt):
            odt_rgb = self.apply_odt_aces(in_rgb)
            result = odt_rgb
        else:
            print("No odt")
            result = in_rgb

        return result

    @staticmethod
    def bitdepth_picker(in_bitdepth, out_bitdepth):
        if BITDEPTH_DICO.get(out_bitdepth) == 'original':
            output = in_bitdepth
        else:
            output = BITDEPTH_DICO.get(out_bitdepth)
        return output

    def pixel_processing(self, in_rgb, cctf=False, cat='Bradford'):
        """

        Args:
            in_rgb: pixel data (numpy array)
            cctf: bool: apply_cctf_decoding
            cat: chromatic adaptation model

        Returns: pixel data converted with odt applied or not

        """
        if self.in_cs != self.out_cs:
            input_colourspace = colour.RGB_COLOURSPACES[self.in_cs]
            output_colourspace = colour.RGB_COLOURSPACES[self.out_cs]
            cat = cat
            conversion_rgb = colour.RGB_to_RGB(in_rgb, input_colourspace, output_colourspace,
                                               chromatic_adaptation_transform=cat,
                                               apply_cctf_decoding=cctf)
        else:
            print("Same cs")
            conversion_rgb = in_rgb

        odt_result = self.apply_odt(conversion_rgb)
        return odt_result

    @staticmethod
    def pathGeneration(in_path, out_location='file', out_format='.exr'):
        """

        Args:
            in_path: path to the input file
            out_location: user preference for the location of the output file
            out_format: user preference for the output file format

        Returns: path of the output file

        """
        file_folder_path = os.path.dirname(in_path)
        filename_original = os.path.splitext(os.path.basename(in_path))[0]
        file_ext = os.path.splitext(in_path)[1]
        if out_format.lower() == 'original':
            out_ext = file_ext
        else:
            out_ext = out_format
        # TODO: think to remove vX_oiio
        out_file_name = "v9_oiio_" + filename_original + '_ACEScg' + out_ext

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
    filename3 = r"L:\SCRIPT\Colour\OCIO_converter\tests\bob-ross-9464216-1-402.jpg"
    filename2 = r"L:\SCRIPT\Colour\OCIO_converter\tests\artist_hdri\artist_workshop_4k.hdr"
    filename = r"L:\SCRIPT\Colour\OCIO_converter\tests\odt_test\cabin_render_original.exr"

    Converter(filename, 'file', '.png', '8bit Int', 'ACEScg', 'ACEScg', 'sRGB(ACES)',
              r'L:\SCRIPT\Colour\OCIO_converter\script\github\OCIO_Converter\src\main\resources\base', "none")

    # Converter(filename, 'file', '.exr', '32bit Float', 'ACEScg', 'ACEScg', 'None',
    #           r'L:\SCRIPT\Colour\OCIO_converter\script\github\OCIO_Converter\src\main\resources\base', "none")
