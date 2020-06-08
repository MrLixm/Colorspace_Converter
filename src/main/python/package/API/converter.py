import os

import colour
from oiio import OpenImageIO as oiio
from package.data_list import ODT_DICO


class Converter:
    def __init__(self, in_img, out_location, out_format='.exr', out_bitdepth=None, in_cs=None, out_cs=None, odt=None, resources_path=None):
        """

        Args:
            in_img: path\name.ext of the file
            out_location: 'file' or 'folder'
            out_format: file extension like '.jpg'
            out_bitdepth: bitdepth for the output file: uint8,uint16,half,float, original
            in_cs: source colorspace
            out_cs: target colorspace
            odt: the Output Display Transform to apply (False if not wanted)
        """
        self.resources_path = resources_path
        self.out_filePath = self.pathGeneration(in_img, out_location, out_format)
        ip_result = self.imageProcessing(filepath=in_img, outpath=self.out_filePath, in_cs=in_cs, out_cs=out_cs,
                                         out_bitdepth=out_bitdepth, odt=odt)

    def imageProcessing(self, filepath, outpath, in_cs, out_cs, out_bitdepth, odt):
        """

        Args:
            filepath: the file to convert path
            outpath: the output path given by pathGeneration() method
            in_cs: the input colorspace of the file
            out_cs: the output colorspace of the file
            out_bitdepth: the desired output bitdepth for the file
            odt: the Output Display Transform to apply (False if not wanted)

        Returns: Bool: True is succedd, [False,str] if Error

        """

        # Read Image
        in_img = oiio.ImageInput.open(filepath)
        if not in_img:
            return [False, oiio.geterror()]
        spec = in_img.spec()
        pixels = in_img.read_image()
        in_img.close()

        # Convert the rgb data
        final_image = self.colourConversion(pixels, in_cs, out_cs, odt=odt)

        # pick the output file bitdepth format
        spec.format = self.bitdepth_picker(spec.format, out_bitdepth)

        output = oiio.ImageOutput.create(outpath)
        output.open(outpath, spec)
        output.write_image(final_image)
        output.close()
        return True

    def colourConversion(self, in_rgb, in_cs, out_cs, cctf=False, cat='Bradford', odt=None):
        input_colourspace = colour.RGB_COLOURSPACES[in_cs]
        output_colourspace = colour.RGB_COLOURSPACES[out_cs]
        cat = cat
        conversion_rgb = colour.RGB_to_RGB(in_rgb, input_colourspace, output_colourspace, chromatic_adaptation_transform=cat,
                                   apply_cctf_decoding=cctf)
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

    def apply_odt(self, in_rgb, odt):
        lut_path = os.path.join(self.resources_path, "luts")
        lut_list = ODT_DICO.get(odt)
        lut_1 = colour.io.read_LUT_SonySPI3D(os.path.join(lut_path, lut_list[0]))
        lut_2 = colour.io.read_LUT_SonySPI3D(os.path.join(lut_path, lut_list[1]))
        apply_lut_1 = lut_1.apply(in_rgb)
        apply_lut_2 = lut_2.apply(apply_lut_1)
        return apply_lut_2


if __name__ == '__main__':
    filename = r"E:\Images\artist_workshop_4k.hdr"
