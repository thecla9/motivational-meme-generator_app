import random
import os
import requests
from flask import Flask, render_template, request

# Import Ingestor and MemeEngine classes
from quoteengine.ingestor import Ingestor
from memegenerator.memeengine import MemeEngine

app = Flask(__name__)
static_dir = "./src/static/pic."
meme = MemeEngine(os.getcwd() + static_dir)


def setup():
    """Load all resources."""

    quote_files = [os.getcwd()+'./src/_data/DogQuotes/DogQuotesTXT.txt',
                   os.getcwd()+'./src/_data/DogQuotes/DogQuotesDOCX.docx',
                   os.getcwd()+'./src/_data/DogQuotes/DogQuotesPDF.pdf',
                   os.getcwd()+'./src/_data/DogQuotes/DogQuotesCSV.csv']

    # Parse all files in the quote_files variable
    quotes = []
    for f in [Ingestor.parse(file) for file in quote_files]:
        for a in f or []:
            quotes.append(a)

    images_path = os.getcwd()+"./src/_data/photos/dog/"

    # Find all images within the images images_path directory
    imgs = [os.getcwd() + './src/_data/photos/dog/' + img
            for img in os.listdir(images_path)]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""

    # Select a random image from imgs array
    img = random.choice(imgs)
    # Select a random quote from the quotes array
    quote = random.choice(quotes)

    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # Save the image from the image_url
    img = "./temp_image.jpg"
    image_url = request.form.get("image_url")
    img_data = requests.get(image_url, stream=True).content

    with open(img, "wb") as f:
        f.write(img_data)
    # Generate a meme using this temp
    body = request.form.get("body", "")
    author = request.form.get("author", "")
    path = meme.make_meme(img, body, author)
    # print(path)
    # Remove the temporary saved image.
    os.remove(img)
    return render_template("meme.html", path=path)


if __name__ == "__main__":
    app.run()
