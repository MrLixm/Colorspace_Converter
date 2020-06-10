CS_TARGET_LIST = [
    'ACEScg',
    'ACES2065-1',
    'ACEScc',
    'ACEScct',
    'sRGB',
    'Adobe Wide Gamut RGB',
    'Adobe RGB (1998)',
    'ITU-R BT.2020',
]

FORMAT_LIST = [".exr", ".jpg", ".png", "Original"]

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
        list[0]: 1d Lut: log to lin
        list[1]: 3d Lut: log to RRT
        list[2]: 3d Lut: RRT to log 
"""
ODT_DICO = {
    'None': False,
    'sRGB(ACES)': ['Log2_48_nits_Shaper_to_linear.spi1d',
                   'Log2_48_nits_Shaper.RRT.sRGB.spi3d',
                   'InvRRT.sRGB.Log2_48_nits_Shaper.spi3d'],
    'rec709(ACES)': [],
    'P3D60(ACES)': [],
    'P3D65(ACES)': [],
    'sRGB(EOTF)': [],
    'Gamma 2.2': [],  # don't know if really usefull
    'Maybe filmic ?': [],
}

IDT_DICO = {
    'sRGB-Linear': ['sRGB', False],
    'sRGB-Texture': ['sRGB', True],
    'rec709-Texture': ['ITU-R BT.709', True],
    'ACEScg': ['ACEScg', False],
    'ACES2065-1': ['ACES2065-1', False],
    'ACEScc': ['ACEScc', False],
    'ACEScct': ['ACEScct', False],
    'XYZ': ['XYZ', False]
}

COMPRESSION_LIST = ['none', 'rle', 'zip', 'zips', 'piz', 'pxr24', 'b44', 'b44a', 'dwaa', 'dwab']
