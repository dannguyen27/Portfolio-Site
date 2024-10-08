from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import os
from flask_assets import Environment, Bundle
from flask_caching import Cache
from flask_minify import Minify

app = Flask(__name__)

# Enable Flask-Minify for HTML, JS, and CSS minification
Minify(app=app, html=True, js=True, cssless=True)

# Configure Flask-Caching for response caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Configure Flask-Assets for bundling and minifying CSS/JS
assets = Environment(app)

# Bundle and minify CSS
css = Bundle('static/assets/css/main.css', filters='cssmin', output='dist/main.min.css')

# Bundle and minify JS
js = Bundle('static/assets/js/main.js', filters='jsmin', output='dist/main.min.js')

# Register the bundles with Flask-Assets
assets.register('css_all', css)
assets.register('js_all', js)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Base path for images
IMAGE_FOLDER = 'static/images/'

def load_image(img_name):
    """Load an image and return its NumPy array."""
    img_path = os.path.join(IMAGE_FOLDER, img_name)
    img = Image.open(img_path)
    return np.array(img), img.size

@app.route('/')
@cache.cached(timeout=300)  # Cache the index page for 5 minutes
def index():
    return render_template('index.html')

@app.route('/get-color')
@cache.cached(timeout=300, query_string=True)  # Cache API calls based on query string
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
