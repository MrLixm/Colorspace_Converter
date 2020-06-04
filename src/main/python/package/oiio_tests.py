import colour
from oiio import OpenImageIO as oiio


def image_processing(filepath, outpath):
    in_img = oiio.ImageInput.open(filepath)
    spec = in_img.spec()
    pixels = in_img.read_image()
    in_img.close()

    print("resolution ", spec.width, "x", spec.height)

    converted_rgb = colour_conversion(pixels)
    final_image = converted_rgb

    output = oiio.ImageOutput.create(outpath)
    output.open(outpath, spec)
    output.write_image(converted_rgb)
    output.close()


def colour_conversion(in_rgb):
    input_colourspace = colour.RGB_COLOURSPACES['sRGB']
    output_colourspace = colour.RGB_COLOURSPACES['ACEScg']
    cat = 'CAT02'
    result = colour.RGB_to_RGB(in_rgb, input_colourspace, output_colourspace, chromatic_adaptation_transform=cat,
                               apply_cctf_decoding=False)
    return result


if __name__ == '__main__':
    filename = r"E:\Images\artist_workshop_4k.hdr"
    out_path = r"E:\Images\artist_workshop_oiio_acescg_v1.exr"
    image_processing(filename, out_path)
