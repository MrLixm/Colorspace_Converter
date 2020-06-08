CS_TARGET_LIST = [
    'ACEScg',
    'ACES2065-1',
    'ACEScc',
    'ACEScct',
    'sRGB',
    'Adobe Wide Gamut RGB',
    'ITU-R BT.2020',
]

FORMAT_LIST = [".exr", ".jpg", ".png", "original"]

BITDEPTH_DICO = {
    "8bit Int": "uint8",
    "16bit Int": "uint16",
    "16bit Half": "half",
    "32bit Float": "float",
    "Original": "original"
}

ODT_DICO = {
    'None': False,
    'sRGB(ACES)': ['InvRRT.sRGB.Log2_48_nits_Shaper.spi3d', 'Log2_48_nits_Shaper.RRT.sRGB.spi3d'],
    'Rec709(ACES)': [],
    'P3-D60(ACES)': []
}
IDT_LIST = [
    'sRGB-Linear',
    'sRGB-Texture',
    'ACEScg',
    'ACES2065-1',
    'XYZ'
]

COMPRESSION_LIST = ['none', 'rle', 'zip', 'zips', 'piz', 'pxr24', 'b44', 'b44a', 'dwaa', 'dwab']
