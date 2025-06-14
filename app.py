from flask import Flask, render_template, request, send_from_directory, jsonify
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
OUTPUT_FOLDER = 'output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get('text', '')
    speed = data.get('speed', 'normal')

    if not text:
        return jsonify({'error': 'Teks tidak boleh kosong'}), 400

    try:
        # gTTS hanya punya slow=True atau False
        slow = True if speed == 'slow' else False
        tts = gTTS(text=text, lang='id', slow=slow)
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        tts.save(filepath)

        return jsonify({'file': filename, 'speed': speed})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
