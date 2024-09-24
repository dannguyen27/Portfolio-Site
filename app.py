from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

# Base path for images
IMAGE_FOLDER = 'static/images/'

def load_image(img_name):
    """Load an image and return its NumPy array."""
    img_path = os.path.join(IMAGE_FOLDER, img_name)
    img = Image.open(img_path)
    return np.array(img), img.size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-color')
def get_color():
    image_name = request.args.get('image')
    x = float(request.args.get('x'))
    y = float(request.args.get('y'))

    try:
        img_array, img_size = load_image(image_name)
        img_width, img_height = img_size

        # Convert relative coordinates to absolute coordinates
        x = int(x * img_width)
        y = int(y * img_height)

        # Ensure coordinates are within bounds
        x = min(max(x, 0), img_width - 1)
        y = min(max(y, 0), img_height - 1)

        # Get the RGB value at the specified coordinates
        rgb_value = img_array[y, x]
        r, g, b = map(int, rgb_value[:3])  # Convert to standard Python int

        return jsonify({'r': r, 'g': g, 'b': b})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
