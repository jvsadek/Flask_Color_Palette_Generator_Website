from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request
from PIL import Image
import io
from collections import Counter
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.image as mpimg

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FLASK_KEY'
# app.config['SECRET_KEY']=  os.environ.get('FLASK_KEY')
Bootstrap5(app)

def get_color_palette(image_path):
    # Load the image using mpimg.imread(). Use a raw string (prefix r) or escape the backslashes.
    image = Image.open(image_path)
    # image = mpimg.imread(image_path)
    # Resize the image to a small size for faster processing
    image = image.resize((np.array(image.size)/10).astype(int))
    # Get the dimensions (width, height, and depth) of the image
    image = np.asarray(image)
    w, h, d = tuple(image.shape)

    # Reshape the image into a 2D array, where each row represents a pixel
    pixel = np.reshape(image, (w * h, d))

    # Import the KMeans class from sklearn.cluster

    # Set the desired number of colors for the image
    n_colors = 6

    # Create a KMeans model with the specified number of clusters and fit it to the pixels
    model = KMeans(n_clusters=n_colors, random_state=42).fit(pixel)

    # Get the cluster centers (representing colors) from the model
    colour_palette = np.uint8(model.cluster_centers_)
    palette = [tuple(color) for color in colour_palette]

    return palette

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file:
        # Save the uploaded image to a temporary file
        image_path = 'static/css/Img/temp_image.jpg'
        file.save(image_path)

        # Get the color palette
        color_palette = get_color_palette(image_path)

        return render_template('result.html', image_path=image_path, color_palette=color_palette)

if __name__ == '__main__':
    app.run(debug=True,port=5002)
