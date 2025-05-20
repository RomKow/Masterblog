import os
import json
from flask import Flask, render_template

app = Flask(__name__)

# Path to the JSON file storing blog posts
DATA_FILE = os.path.join(os.path.dirname(__file__), 'posts.json')


@app.route('/')
def index():
    """Read all blog posts from the JSON file and render the index template."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5001, debug=True)
