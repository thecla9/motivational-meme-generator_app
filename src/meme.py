import argparse
import os
import random



# @TODO Import your Ingestor and MemeEngine classes
from memegenerator.memeengine import MemeEngine
from quoteengine.ingestor import Ingestor
from quoteengine.quotes import QuoteModel



def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = os.getcwd() +"./src/_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = [os.getcwd()+'./src/_data/DogQuotes/DogQuotesTXT.txt',
                       os.getcwd()+'./src/_data/DogQuotes/DogQuotesDOCX.docx',
                       os.getcwd()+'./src/_data/DogQuotes/DogQuotesPDF.pdf',
                       os.getcwd()+'./src/_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in [Ingestor.parse(file) for file in quote_files]:
            for a in f or []:
                quotes.append(a)
        
        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine(os.getcwd()+'./src/tmp.')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = argparse.ArgumentParser(description="Meme generator")
    parser.add_argument('-p', '--path')
    parser.add_argument('-b', '--body')
    parser.add_argument('-a', '--author')
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
