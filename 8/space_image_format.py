from collections import Counter
from colorama import init
from termcolor import colored


def corruption_check(filename, width, height):
    with open(filename, 'r') as f:
        data = f.read()

    pixels_in_layer = width * height
    fewest_zeros = pixels_in_layer
    fewest_zeros_counter = None
    while len(data) > 1:
        layer = data[:pixels_in_layer]
        data = data[pixels_in_layer:]
        c = Counter(layer)
        fewest_zeros_counter = c if c['0'] < fewest_zeros else fewest_zeros_counter
        fewest_zeros = min(c['0'], fewest_zeros)

    return fewest_zeros_counter['1'] * fewest_zeros_counter['2']


def render_border(width, left_side=False):
    print(colored('  ' * width, 'white', 'on_cyan'), end='' if left_side else '\n')


def render(filename, width, height):
    with open(filename, 'r') as f:
        data = f.read()

    # Get the composite of the image layers for rendering
    # 0 is black
    # 1 is white
    # 2 is transparent; the pixel on the layer below this one is visible
    pixels_in_layer = width * height
    rendered_layer = ['2'] * pixels_in_layer
    while len(data) > 1:
        layer = data[:pixels_in_layer]
        data = data[pixels_in_layer:]
        for i in range(pixels_in_layer):
            rendered_layer[i] = layer[i] if rendered_layer[i] == '2' else rendered_layer[i]

    # Render the image
    render_border(width + 2)
    for _ in range(height):
        render_border(1, True)
        line = rendered_layer[:width]
        rendered_layer = rendered_layer[width:]
        for pix in line:
            print(colored('  ', 'white', None if pix == '0' else 'on_white'), end='')
        render_border(1)
    render_border(width + 2)


if __name__ == '__main__':
    print(corruption_check('image.txt', 25, 6))
    render('image.txt', 25, 6)
