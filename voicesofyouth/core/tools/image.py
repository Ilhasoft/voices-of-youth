from PIL import Image
import numpy as np

def change_colors(original_image, dest_image, from_colors, to_color):
    """
    Changes all colors of from_colors by the color of to_color.

    :param original_image:
    :param dest_image:
    :param from_colors: Array of tuples of colors in format (R, G, B)
    :param to_color: Tuple of final color in format (R, G, B)
    """
    from_image = original_image

    for n in range(len(from_colors)):
        if n == len(from_colors) - 1:
            to_image = dest_image
        else:
            to_image = f'step{n}.png'
        change_color(from_image, to_image, from_colors[n], to_color)
        from_image = to_image

def change_color(original_image, dest_image, from_color, to_color):
    """
    Change the color from_color to to_color and save a new image in dest_image.

    :param original_image:
    :param dest_image:
    :param from_color: Tuple of target color in format (R, G, B)
    :param to_color: Tuple of final color in format (R, G, B)
    """
    if not isinstance(from_color, tuple) and isinstance(to_color, tuple):
        raise ValueError('The params from_color and to_color needs to be a tuple instance')

    if not len(from_color) == 3 and len(to_color) == 3:
        raise ValueError('The params from_color and to_color needs to be a tuple with 3 elements(R, G, B)')

    im = Image.open(original_image)

    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    target_color = (red == from_color[0]) & (blue == from_color[2]) & (green == from_color[1])
    data[..., :-1][target_color.T] = to_color # Transpose back needed

    im2 = Image.fromarray(data)
    im2.save(dest_image)
