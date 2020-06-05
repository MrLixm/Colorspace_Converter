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
            out_bitdepth: bitdepth for the output file: uint8,uint16,half,float, original
            in_cs: source colorspace
            out_cs: target colorspace
        """

        self.out_filePath = self.pathGeneration(in_img, out_location, out_format)
        ip_result = self.imageProcessing(filepath=in_img, outpath=self.out_filePath, in_cs=in_cs, out_cs=out_cs,
                                         out_bitdepth=out_bitdepth)

    def imageProcessing(self, filepath, outpath, in_cs, out_cs, out_bitdepth):
        """

        Args:
            filepath: the file to convert path
            outpath: the output path given by pathGeneration() method
            in_cs: the input colorspace of the file
            out_cs: the output colorspace of the file
            out_bitdepth: the desired output bitdepth for the file

        Returns: Bool: True is succedd, [False,str] if Error

        """
        in_img = oiio.ImageInput.open(filepath)
        if not in_img:
            return [False, oiio.geterror()]
        spec = in_img.spec()
        pixels = in_img.read_image()
        in_img.close()

        # Convert the rgb data
        converted_rgb = self.colourConversion(pixels, in_cs, out_cs)
        final_image = converted_rgb

        # pick the output file bitdepth format
        spec.format = self.bitdepth_picker(spec.format, out_bitdepth)

        output = oiio.ImageOutput.create(outpath)
        output.open(outpath, spec)
        output.write_image(final_image)
        output.close()
        return True

    @staticmethod
    def colourConversion(in_rgb, in_cs, out_cs, cctf=False, cat='Bradford'):
        input_colourspace = colour.RGB_COLOURSPACES[in_cs]
        output_colourspace = colour.RGB_COLOURSPACES[out_cs]
        cat = cat
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

    @staticmethod
    def bitdepth_picker(in_bitdepth, out_bitdepth):
        if out_bitdepth == 'original':
            output = in_bitdepth
        else:
            output = out_bitdepth
        return output


if __name__ == '__main__':
    filename = r"E:\Images\artist_workshop_4k.hdr"
    c = Converter(filename, out_path)
