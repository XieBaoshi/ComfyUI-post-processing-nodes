import torch

class Dither:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "bits": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 8,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "dither"

    CATEGORY = "postprocessing"

    def dither(self, image: torch.Tensor, bits: int):
        tensor_image = image.numpy()[0]
        img = (tensor_image * 255)
        height, width, _ = img.shape

        scale = 255 / (2**bits - 1)

        for y in range(height):
            for x in range(width):
                old_pixel = img[y, x].copy()
                new_pixel = np.round(old_pixel / scale) * scale
                img[y, x] = new_pixel

                quant_error = old_pixel - new_pixel

                if x + 1 < width:
                    img[y, x + 1] += quant_error * 7 / 16
                if y + 1 < height:
                    if x - 1 >= 0:
                        img[y + 1, x - 1] += quant_error * 3 / 16
                    img[y + 1, x] += quant_error * 5 / 16
                    if x + 1 < width:
                        img[y + 1, x + 1] += quant_error * 1 / 16

        dithered = img / 255
        tensor = torch.from_numpy(dithered).unsqueeze(0)
        return (tensor,)

NODE_CLASS_MAPPINGS = {
    "Dither": Dither
}
