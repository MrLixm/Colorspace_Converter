from pprint import pprint

import colour

result_list = []


def rgb_conversion(in_rgb, cat):
    input_colourspace = colour.RGB_COLOURSPACES['sRGB']
    output_colourspace = colour.RGB_COLOURSPACES['ACEScg']

    result = colour.RGB_to_RGB(in_rgb, input_colourspace, output_colourspace, chromatic_adaptation_transform=cat)
    result_list.append(result)
    return result

rgb_conversion((0, 1, 0), 'CAT02')
rgb_conversion((0, 1, 0), 'XYZ Scaling')
rgb_conversion((0, 1, 0), 'Von Kries')
rgb_conversion((0, 1, 0), 'Bradford')
rgb_conversion((0, 1, 0), 'Sharp')
rgb_conversion((0, 1, 0), 'Fairchild')
rgb_conversion((0, 1, 0), 'CMCCAT97')
rgb_conversion((0, 1, 0), 'CMCCAT2000')
rgb_conversion((0, 1, 0), 'CAT02_BRILL_CAT')
rgb_conversion((0, 1, 0), 'Bianco')
rgb_conversion((0, 1, 0), 'Bianco PC')
rgb_conversion((0, 1, 0), None)


pprint(result_list)
