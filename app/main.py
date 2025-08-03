from flask import Flask, jsonify, request, redirect, abort, url_for
from app.models import store
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "service": "URL Shortener API"})

@app.route('/api/health')
def api_health():
    return jsonify({"status": "ok", "message": "URL Shortener API is running"})

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL"}), 400

    original_url = data['url']
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    while store.get_url(short_code):  # avoid collisions
        short_code = generate_short_code()

    store.save_url(short_code, original_url)
    short_url = request.host_url.rstrip('/') + '/' + short_code

    return jsonify({"short_code": short_code, "short_url": short_url})

@app.route('/<short_code>')
def redirect_url(short_code):
    entry = store.get_url(short_code)
    if not entry:
        abort(404)

    store.increment_click(short_code)
    return redirect(entry['url'])

@app.route('/api/stats/<short_code>')
def stats(short_code):
    entry = store.get_stats(short_code)
    if not entry:
        abort(404)

    return jsonify({
        "url": entry['url'],
        "clicks": entry['clicks'],
        "created_at": entry['created_at'].isoformat()
    })
