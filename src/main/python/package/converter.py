import os
from pprint import pprint

import colour
from oiio import OpenImageIO as oiio


class Converter:
    def __init__(self, in_img, out_location, out_format='.exr', out_bitdepth=None, in_cs=None, out_cs=None):
        """
        Args:
            in_img: path\name.ext of the file
            out_location: 'file' or 'folder'
            out_format: file extension like '.jpg'
            out_bitdepth: 'bitdepth for the output file: uint8,uint16,half,float
            in_cs: source colorspace
            out_cs: target colorspace
        """

        self.out_filePath = self.pathGeneration(in_img, out_location, out_format)
        ip_result = self.imageProcessing(filepath=in_img, outpath=self.out_filePath, in_cs=in_cs, out_cs=out_cs,
                                         out_bitdepth=out_bitdepth)

    def imageProcessing(self, filepath, outpath, in_cs, out_cs, out_bitdepth):
        in_img = oiio.ImageInput.open(filepath)
        if not in_img:
            return oiio.geterror()
        spec = in_img.spec()
        pixels = in_img.read_image()
        in_img.close()

        print("resolution ", spec.width, "x", spec.height)

        converted_rgb = self.colourConversion(pixels)
        final_image = converted_rgb

        output = oiio.ImageOutput.create(outpath)
        output.open(outpath, spec)
        final_image.set_write_format("uint16")
        output.write_image(final_image)
        output.close()

    @staticmethod
    def colourConversion(in_rgb, cctf=False):
        input_colourspace = colour.RGB_COLOURSPACES['sRGB']
        output_colourspace = colour.RGB_COLOURSPACES['ACEScg']
        cat = 'CAT02'
        result = colour.RGB_to_RGB(in_rgb, input_colourspace, output_colourspace, chromatic_adaptation_transform=cat,
                                   apply_cctf_decoding=cctf)
        return result

    @staticmethod
    def pathGeneration(in_path, out_location='file', out_format='.exr'):
        file_folder_path = os.path.dirname(in_path)
        filename_original = os.path.splitext(os.path.basename(in_path))[0]
        file_ext = os.path.splitext(in_path)[1]
        if out_format == 'original':
            out_ext = file_ext
        else:
            out_ext = out_format
        out_file_name = filename_original + '_ACEScg' + out_ext

        if out_location == 'file':
            output_path = os.path.join(file_folder_path, out_file_name)
            return output_path
        if out_location == 'folder':
            acesFolder_path = os.path.join(file_folder_path, 'ACEScg')
            if not os.path.exists(acesFolder_path):
                os.makedirs(acesFolder_path)
            output_path = os.path.join(acesFolder_path, out_file_name)
            return output_path


if __name__ == '__main__':
    filename = r"E:\Images\artist_workshop_4k.hdr"
    out_path = r"E:\Images\artist_workshop_oiio_acescg_v1.exr"
    # c = Converter(filename, out_path)
    list = colour.models.rgb.__all__
    index = list.index('RGB_COLOURSPACES')
    pprint(list[index:])
