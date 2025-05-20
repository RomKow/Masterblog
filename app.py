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
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                posts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            posts = []

        max_id = max((post.get('id', 0) for post in posts), default=0)
        new_post = {
            'id': max_id + 1,
            'author': author,
            'title': title,
            'content': content
        }

        posts.append(new_post)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Remove the post with the given ID from JSON storage and redirect to home."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    # Filter out the post to delete
    posts = [post for post in posts if post.get('id') != post_id]

    # Save updated list back to JSON
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5001, debug=True)
