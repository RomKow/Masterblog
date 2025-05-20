import os
import json
from flask import Flask, render_template, request, redirect, url_for, abort

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
    """Display the add-post form on GET; on POST, append a new post (with 0 likes) and redirect."""
    if request.method == 'POST':
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        # Load existing posts
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                posts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            posts = []

        # Generate a new unique ID
        max_id = max((post.get('id', 0) for post in posts), default=0)
        new_post = {
            'id': max_id + 1,
            'author': author,
            'title': title,
            'content': content,
            'likes': 0
        }

        # Append and save
        posts.append(new_post)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """On GET: render form with current post data; on POST: update the post and redirect."""
    # Load posts
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    # Find the target post
    post = next((p for p in posts if p.get('id') == post_id), None)
    if post is None:
        abort(404, description="Post not found")

    if request.method == 'POST':
        # Update fields
        post['author'] = request.form.get('author', '').strip()
        post['title'] = request.form.get('title', '').strip()
        post['content'] = request.form.get('content', '').strip()

        # Save back
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    # GET → show form
    return render_template('update.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Remove the post with the given ID from JSON storage and redirect to home."""
    # Load posts
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    # Filter out the deleted post
    posts = [p for p in posts if p.get('id') != post_id]

    # Save updated list
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))


@app.route('/like/<int:post_id>')
def like(post_id):
    """Increment the 'likes' count for the post with the given ID and redirect to home."""
    # Load posts
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    # Find and increment
    for p in posts:
        if p.get('id') == post_id:
            p['likes'] = p.get('likes', 0) + 1
            break

    # Save back
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5001, debug=True)
