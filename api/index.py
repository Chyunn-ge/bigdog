from flask import Flask, jsonify, request, send_file
import os
import random

app = Flask(__name__)

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio_files')

@app.route('/')
def home():
    return 'API 正常运行中！'

@app.route('/api/audio')
def get_audio():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': '请输入 keyword 参数'}), 400

    folder_path = os.path.join(BASE_DIR, keyword)
    if not os.path.exists(folder_path):
        return jsonify({'error': f'找不到关键词: {keyword}'}), 404

    files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
    if not files:
        return jsonify({'error': '这个关键词还没有 mp3 文件'}), 404

    chosen = random.choice(files)
    audio_url = request.url_root + f'audio_files/{keyword}/{chosen}'
    return jsonify({'url': audio_url})

@app.route('/audio_files/<keyword>/<filename>')
def serve_audio(keyword, filename):
    file_path = os.path.join(BASE_DIR, keyword, filename)
    return send_file(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
