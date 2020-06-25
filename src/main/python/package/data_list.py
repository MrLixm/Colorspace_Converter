"""
Data list and dicos used through the app to determine features

Author: Liam Collod
Contact: lcollod@gmail.com
"""

"""
Dictionnary of the output colorspaces
keys: str: graphical element
value: list: 
        list[0]: API element
        list[1]: Apply CCTF cctf_encoding
"""
CS_TARGET_DICO = {
    'ACEScg':               ['ACEScg', False],
    'ACES2065-1':           ['ACES2065-1', False],
    'ACEScc':               ['ACEScc', True],
    'ACEScct':              ['ACEScct', True],
    'sRGB-Rec709':          ['sRGB', False],
    'Adobe Wide Gamut RGB': ['Adobe Wide Gamut RGB', False],
    'Adobe RGB (1998)':     ['Adobe RGB (1998)', False],
    'Rec2020':              ['ITU-R BT.2020', False]
}

SUPPORTED_IN_FORMAT = ['.exr', '.png', '.jpg', '.jpeg', '.tiff', '.tif', '.hdr']
FORMAT_LIST = [".exr", ".jpg", ".png"]  # , "Original"]
COMPRESSION_LIST = ['none', 'rle', 'zip', 'zips', 'piz', 'pxr24', 'b44', 'b44a', 'dwaa', 'dwab']

BITDEPTH_DICO = {
    "8bit Int": "uint8",
    "16bit Int": "uint16",
    "16bit Half": "half",
    "32bit Float": "float",
    "Original": "original"
}

"""
Dictionnary of the Outputs Display Transform options
keys: str: graphical element
value: list: list of lut corresponding to the odt
        list[0]: 3d Lut: log to RRT
        list[1]: 3d Lut: RRT to log 
"""
ODT_DICO = {
    'None': False,
    'sRGB(ACES)': ['Log2_48_nits_Shaper.RRT.sRGB.spi3d',
                   'InvRRT.sRGB.Log2_48_nits_Shaper.spi3d'],
    'Rec709(ACES)': ['Log2_48_nits_Shaper.RRT.Rec.709.spi3d'],
    'P3D60(ACES)': ['Log2_48_nits_Shaper.RRT.P3-D60.spi3d'],
    'P3D65(ACES)': ['Log2_48_nits_Shaper.RRT.P3D65.spi3d'],
    'sRGB(EOTF)': ['sRGB'],
    'rec709(OETF)': ['ITU-R BT.709'],
    'Gamma 2.2': ['Gamma 2.2'],
}

"""
Dictionnary of the Inputs Device Transform options
keys: str: graphical element
value: list: list of the API element and Icon
        list[0]: input colorpsace
        list[1]: apply cctf decoding
        list[2]: icon path
"""
IDT_DICO = {
    'Utility - sRGB - Linear': ['sRGB', False, ':/idt/icon_idt_srgb_lin.png'],
    'Utility - sRGB - Texture': ['sRGB', True, ':/idt/icon_idt_srgb_tex.png'],
    'Utility - rec709 - Texture': ['ITU-R BT.709', True, ':/idt/icon_idt_rec709_tex.png'],
    'ACEScg': ['ACEScg', False, ':/idt/icon_idt_acescg.png'],
    'ACES2065-1': ['ACES2065-1', False, ':/idt/icon_idt_acesap0.png'],
    'ACEScc': ['ACEScc', True, ':/idt/icon_idt_acescc.png'],
    'ACEScct': ['ACEScct', True, ':/idt/icon_idt_acescct.png'],
    'XYZ D60': ['XYZ', False, ':/idt/icon_idt_xyz.png'],
    'ADOBE 1998 - Linear': ['Adobe RGB (1998)', False, ':/idt/icon_idt_adobe.png'],
    'ADOBE WIDE GAMUT - Linear': ['Adobe Wide Gamut RGB', False, ':/idt/icon_idt_adobewg.png']
}

