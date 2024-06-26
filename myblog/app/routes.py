from flask import render_template, request, send_from_directory
from app import app
import os
import markdown

BASEDIR = os.path.abspath(os.path.dirname(__file__))
CLASSIFY_PATH = os.path.join(BASEDIR, '..', 'classify')

@app.route('/')
def index():
    class_dirs = [d for d in os.listdir(CLASSIFY_PATH) if os.path.isdir(os.path.join(CLASSIFY_PATH, d))]
    return render_template('index.html', class_dirs=class_dirs)

@app.route('/classify/<class_name>')
def classify(class_name):
    class_path = os.path.join(CLASSIFY_PATH, class_name)
    articles = [f for f in os.listdir(class_path) if f.endswith('.md')]
    return render_template('classify.html', class_name=class_name, articles=articles)

@app.route('/classify/<class_name>/<article>')
def article(class_name, article):
    article_path = os.path.join(CLASSIFY_PATH, class_name, article)
    with open(article_path, 'r', encoding='utf-8') as file:
        content = file.read()
        html_content = markdown.markdown(content)
    return render_template('article.html', class_name=class_name, article=article, content=html_content)

@app.route('/search')
def search():
    query = request.args.get('q')
    results = search_articles(query)
    return render_template('search.html', query=query, results=results)

def search_articles(query):
    results = []
    for root, dirs, files in os.walk(CLASSIFY_PATH):
        for file in files:
            if file.endswith('.md'):
                if query.lower() in file.lower():
                    relative_path = os.path.relpath(os.path.join(root, file), CLASSIFY_PATH)
                    class_name = os.path.basename(os.path.dirname(relative_path))
                    article_name = file.rsplit('.', 1)[0]  # 去掉 .md 后缀
                    results.append({'class_name': class_name, 'article_name': article_name, 'file_name': file})
    return results

@app.route('/classify/<class_name>/assets/<path:filename>')
def serve_assets(class_name, filename):
    assets_path = os.path.join(CLASSIFY_PATH, class_name, 'assets')
    return send_from_directory(assets_path, filename)
