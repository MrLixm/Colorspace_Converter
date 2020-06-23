import os
import logging

import colour
from colour.algebra import table_interpolation_tetrahedral
from oiio import OpenImageIO as oiio

from package.data_list import ODT_DICO, BITDEPTH_DICO

# TODO: implemant logging
# TODO: finish ODT/tf

logging.basicConfig(level=logging.DEBUG)
#                    filename=r"L:\SCRIPT\Colour\OCIO_converter\tests\loggs.log",  # or specify the path+file
#                    filemode="a",  # or w to replace data
#                    format='%(asctime)s - %(levelname)S - %(message)s')


class Converter:

    # convert_progress = QtCore.Signal()

    def __init__(self, in_img_path, out_location, out_format, out_bitdepth, in_cs, out_cs,
                 odt, resources_path, compression, cctf):
        """

        Args:
            in_img_path: path/name.ext of the file
            out_location: 'file' or 'folder'
            out_format: file extension like '.jpg'
            out_bitdepth: bitdepth for the output file: uint8,uint16,half,float, original
            in_cs: source colorspace [0] item from the IDT dico
            out_cs: target colorspace : key from the ODT dico
            compression: Compression method for exr: none, rle, zip, zips, piz, pxr24, b44, b44a, dwaa, or dwab
            odt: the Output Display Transform to apply (False if not wanted)
            cctf: Bool : Apply in cs decoding colour component transferfunction/electro-optical transferfunction.

        """
        # logging.debug("C init")
        self.cctf = cctf
        self.resources_path = resources_path
        self.out_format = out_format
        self.in_img_path = in_img_path
        self.out_bitdepth = out_bitdepth
        self.in_cs = in_cs
        self.out_cs = out_cs
        self.odt = odt
        self.compression = compression
        self.out_filePath = self.pathGeneration(in_img_path, out_location, out_format)

        oiio.attribute("threads", 0)
        oiio.attribute("exr_threads", 0)

    def image_processing(self):
        logging.info("Image processing")
        # Read Image
        in_buf_data = oiio.ImageBuf(self.in_img_path)
        in_buf_roi = oiio.get_roi(in_buf_data.spec())
        if in_buf_data.has_error:
            return [False, in_buf_data.geterror()]

        in_buf_rgb = oiio.ImageBufAlgo.channels(in_buf_data, (0, 1, 2))  # Remove other channels(multi-channels exr)
        in_buf_alpha = oiio.ImageBufAlgo.channels(in_buf_data, (3,))  # copy the Alpha channel
        if in_buf_rgb.has_error:
            return [False, in_buf_rgb.geterror()]
        # self.convert_progress.emit()

        in_array_rgb = in_buf_rgb.get_pixels()
        converted_array_rgba = self.pixel_processing(in_array_rgb, cctf=self.cctf)
        in_buf_rgb.set_pixels(in_buf_roi, converted_array_rgba)  # Replace the buffer with the converted pixels
        in_buf_rgba = oiio.ImageBufAlgo.channel_append(in_buf_rgb, in_buf_alpha)  # Merge the alpha channel back
        # self.convert_progress.emit()

        in_buf_rgba.specmod().attribute("compression", self.compression.lower())
        in_buf_rgba.specmod().attribute("oiio:ColorSpace", self.out_cs if not ODT_DICO.get(self.odt) else self.odt)
        bitdepth = self.bitdepth_picker(in_buf_data.nativespec().format, self.out_bitdepth)
        in_buf_rgba.set_write_format(bitdepth)
        if in_buf_rgba.has_error:
            return [False, in_buf_rgba.geterror()]
        in_buf_rgba.write(self.out_filePath)
        # self.convert_progress.emit()
        return [True]

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

    def apply_odt_cctf(self, in_rgb):
        cctf_func = ODT_DICO.get(self.odt)[0]
        result = colour.cctf_encoding(in_rgb, cctf_func)
        return result

    def apply_odt(self, in_rgb):
        if ODT_DICO.get(self.odt):
            if self.odt.endswith('(ACES)'):
                odt_rgb = self.apply_odt_aces(in_rgb)
                result = odt_rgb
            else:
                cctf = self.apply_odt_cctf(in_rgb)
                result = cctf

        else:
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
            if self.in_cs == 'XYZ':
                conversion_rgb = colour.XYZ_to_RGB(in_rgb, output_colourspace.whitepoint, output_colourspace.whitepoint,
                                                   output_colourspace.XYZ_to_RGB_matrix, chromatic_adaptation_transform=
                                                   cat)
            else:
                conversion_rgb = colour.RGB_to_RGB(in_rgb, input_colourspace, output_colourspace,
                                                    chromatic_adaptation_transform=cat,
                                                    apply_cctf_decoding=cctf)
        else:
            conversion_rgb = in_rgb

        odt_result = self.apply_odt(conversion_rgb)
        return odt_result

    def pathGeneration(self, in_path, out_location='file', out_format='.exr'):
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
        if ODT_DICO.get(self.odt):
            cs_prefix = '_' + self.odt
        else:
            cs_prefix = '_' + self.out_cs.replace(" ", "")

        # TODO: think to remove vX_oiio
        out_file_name = "v2_oiio_" + filename_original + cs_prefix + out_ext

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

    # c = Converter(filename, 'file', '.png', '8bit Int', 'ACEScg', 'ACEScg', 'sRGB(ACES)',
    #           r'L:\SCRIPT\Colour\OCIO_converter\script\github\OCIO_Converter\src\main\resources\base', "none", False)

    # c = Converter(filename, 'file', '.exr', '32bit Float', 'ACEScg', 'ACEScg', 'None',
    #               r'L:\SCRIPT\Colour\OCIO_converter\script\github\OCIO_Converter\src\main\resources\base', "dwaa:10",
    #               False)

    c = Converter(filename, 'file', '.jpg', '8bit Int', 'ACEScg', 'sRGB', 'sRGB(EOTF)',
                  r'L:\SCRIPT\Colour\OCIO_converter\script\github\OCIO_Converter\src\main\resources\base', "jpeg:100",
                  False)

    c.image_processing()
