import os

import colour


class Converter:
    def __init__(self):
        pass

    def image_processing(self, img_path):
        image_RGB = colour.read_image(img_path)

        image_XYZ = colour.sRGB_to_XYZ(image_RGB)

        final_image = image_XYZ
        out_path = os.path.join(os.path.dirname(img_path), "testBobRoss.jpg")
        self.result = colour.write_image(final_image, out_path)


if __name__ == '__main__':
    img_path = r"E:\Images\bob-ross-9464216-1-402.jpg"
    c = Converter()
    c.image_processing(img_path)
