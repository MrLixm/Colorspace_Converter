CS_TARGET_LIST = [
    'ACEScg',
    'ACES2065-1',
    'ACEScc',
    'ACEScct',
    'sRGB-Rec709',
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
    'XYZ': ['XYZ', False],
    'ADOBE 1998': ['Adobe RGB (1998)', False],
    'ADOBE WIDE GAMUT': ['Adobe Wide Gamut RGB', False]
}

COMPRESSION_LIST = ['none', 'rle', 'zip', 'zips', 'piz', 'pxr24', 'b44', 'b44a', 'dwaa', 'dwab']

SUPPORTED_IN_FORMAT = ['.exr', '.png', '.jpg', '.jpeg', '.tiff', '.hdr']
