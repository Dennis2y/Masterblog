from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "blog_data.json"

# Load posts from the JSON file
def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Save posts to the JSON file
def save_posts(posts):
    with open(DATA_FILE, "w") as file:
        json.dump(posts, file, indent=4)

# Homepage - show all posts
@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

# View a single post
@app.route('/post/<int:post_id>')
def post(post_id):
    posts = load_posts()
    if 0 <= post_id < len(posts):
        return render_template('post.html', post=posts[post_id])
    else:
        return "Post not found", 404

# Add a new post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        posts = load_posts()
        posts.append({'title': title, 'content': content})
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')

# Update a post
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    if 0 <= post_id < len(posts):
        if request.method == 'POST':
            posts[post_id]['title'] = request.form['title']
            posts[post_id]['content'] = request.form['content']
            save_posts(posts)
            return redirect(url_for('index'))
        return render_template('update.html', post=posts[post_id], post_id=post_id)
    return "Post not found", 404

# Delete a post
@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    if 0 <= post_id < len(posts):
        posts.pop(post_id)
        save_posts(posts)
        return redirect(url_for('index'))
    return "Post not found", 404

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
