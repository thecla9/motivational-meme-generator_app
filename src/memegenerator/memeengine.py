"""This module generates memes by adding quotes to images."""

import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from random import randint


class MemeEngine:
    """Class to create memes from images and quotes"""

    def __init__(self, output_dir: str) -> None:
        """Initialize a meme generator object."""
        self.output_dir = output_dir

    @classmethod
    def load_image(cls, path: str, size: int) -> Image:
        '''
        Load and return croped image if bigger then 500 px
        '''
        im = Image.open(path)
        width, height = im.size
        if width > size or height > size:
            resize = size, size
            im.thumbnail(resize)
        return im

    @classmethod
    def split_text(cls, text, chars):
        words = text.split(' ')
        new_quote = ''
        c = chars
        rows = 1
        for word in words:
            if len(word) < c - 6:
                new_quote += word + ' '
                c -= len(word) + 1
            else:
                rows += 1
                new_quote += '\n' + word + ' '
                c = chars
        return new_quote, rows

    @classmethod
    def place_text(cls, im: Image, quote, author):
        '''
        Place text on a random position on the image
        '''
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(
            "arial.ttf", 15)

        chars = im.size[0]//18
        quote, quote_r = cls.split_text(quote, chars)
        author,  author_r = cls.split_text(author, chars)
        rows = quote_r + author_r

        try:
            randomPosition = (0, randint(
                0, im.size[1] - im.size[0]//17 * rows))
            draw.text(randomPosition, quote + '\n- ' +
                      author, (255, 255, 255), font)
        except:
            raise Exception('Text too long for the image,\
                             it doesn\'t fit in the image')

        return im

    def make_meme(self, path, quote, author) -> str:
        '''
        Place text of choice on a picture of choice
        OR Place some random text on a random pic
        from the database
        @param path: path to the picture
        @param quote: str
        @param author: str
        '''
        im = self.load_image(path, 500)
        extension = path.split('/')[-1].split('.')[1]
        save_path = self.output_dir + extension
        print(save_path)
        im = self.place_text(im, quote, author)
        im.save(save_path)
        return 'static/pic.' + \
            path.split('/')[-1].split('.')[1]
