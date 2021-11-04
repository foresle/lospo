from PIL import Image


# input_im = Image.open('input.jpg')
# input_im = Image.open('output.png')

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


def encode_text(image: Image, text: str):
    # Convert text to bit
    raw_text: list = []

    for symbol in text:
        symbol_byte: str = bin(ord(symbol))[2:]

        while True:
            if len(symbol_byte) != 8:
                symbol_byte = '0' + symbol_byte
            else:
                break

        for bit in symbol_byte:
            raw_text.append(bit)

    image = image.convert('RGBA')
    px_list = image.load()
    image_w, image_h = image.size

    print(f'Text len: {len(raw_text)}\nImage pixels: {image_h * image_w}')

    output_im = Image.new(mode="RGBA", size=(image_w, image_h))

    raw_text_index: int = 0
    for w in range(image_w):
        for h in range(image_h):
            if raw_text_index < len(raw_text):
                output_im.putpixel((w, h), (px_list[w, h][0], px_list[w, h][1],
                                            px_list[w, h][2], 248 if bool(int(raw_text[raw_text_index])) else 249))
                raw_text_index += 1
            else:
                output_im.putpixel((w, h), (px_list[w, h][0], px_list[w, h][1], px_list[w, h][2], 255))

    output_im.save('output.png')


def decode_text(image: Image):
    # raw_text_binary: str = ''

    image = image.convert('RGBA')
    px_list = image.load()
    image_w, image_h = image.size

    byte_str: str = ''
    bytes_list: list = []
    for w in range(image_w):
        for h in range(image_h):
            if px_list[w, h][3] == 255:
                pass
            elif px_list[w, h][3] == 249:
                byte_str += '0'
            elif px_list[w, h][3] == 248:
                byte_str += '1'

            if len(byte_str) == 8:
                bytes_list.append(byte_str)
                byte_str = ''

    final_text: str = ''
    for byte_str in bytes_list:
        decimal = 0

        for digit in byte_str:
            decimal = decimal * 2 + int(digit)

        print(f"{byte_str} -- {decimal} -- {chr(decimal)}")
        final_text += chr(decimal)

    with open('output.txt', 'w') as output_text_file:
        output_text_file.write(final_text)


if __name__ == '__main__':
    # print_pixel_opacity(input_im)
    # create_chess_opacity(input_im)
    # encrypt_text(input_im, input_txt)
    # decrypt_text(input_im)
    menu_choose: str = input('Select a menu item:\n1 - encode\n2 - decode\n> ')
    match menu_choose:
        case '1':
            input('Put the image in which you want to mask the text in a folder with a program called input.png\n'
                  'and the text in the input.txt file, then press ENTER')

            with open('input.txt', 'r') as input_text_file:
                input_txt = input_text_file.read()

            input_im = Image.open('input.png')

            encode_text(input_im, input_txt)
        case '2':
            input('Place the image to be decoded in the folder with the program output.png,\n'
                  'press ENTER and the text will appear in the file output.txt')

            input_im = Image.open('output.png')

            decode_text(input_im)
        case _:
            print('Please try again')
            exit(0)
