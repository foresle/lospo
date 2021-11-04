from PIL import Image

input_im = Image.open('input.jpg')


def print_pixel_opacity(image: Image):
    image = image.convert('RGBA')
    px_list = image.load()
    image_w, image_h = image.size

    for w in range(image_w):
        row_str: str = ''
        for h in range(image_h):
            row_str += str(px_list[w, h]) + '-'

        print(f'{row_str}\n')


def create_chess_opacity(image: Image):
    image = image.convert('RGBA')
    px_list = image.load()
    image_w, image_h = image.size

    output_im = Image.new(mode="RGBA", size=(image_w, image_h))

    for w in range(image_w):
        black_cell: bool = True
        for h in range(image_h):
            output_im.putpixel((w, h), (px_list[w, h][0], px_list[w, h][1],
                                        px_list[w, h][2], 249 if black_cell else 255))
            black_cell = not black_cell

    output_im.save('output.png')


if __name__ == '__main__':
    # print_pixel_opacity(input_im)
    # create_chess_opacity(input_im)
    pass
