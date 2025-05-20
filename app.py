import os
import json
from flask import Flask, render_template, request, redirect, url_for

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


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Display the add-post form on GET; on POST, append a new post and redirect."""
    if request.method == 'POST':
        # Extract form data
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        # Load existing posts
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                posts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            posts = []

        # Generate new unique ID
        max_id = max((post.get('id', 0) for post in posts), default=0)
        new_post = {
            'id': max_id + 1,
            'author': author,
            'title': title,
            'content': content
        }

        # Append and save back to JSON
        posts.append(new_post)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)

        # Redirect to home page
        return redirect(url_for('index'))

    # GET request — render the form
    return render_template('add.html')


if __name__ == '__main__':
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5001, debug=True)
