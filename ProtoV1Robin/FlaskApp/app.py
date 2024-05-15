from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)

@app.route("/capture-test")
def captureTest(name=None):
    return render_template('capture-test.html', name=name)

# route pour recevoir données de l'audio
@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    wave = request.files['audioFile']

    if wave:
        filename = 'wave.wav'
        #file_path = os.path.join('/path/to/save', filename)
        #wave.save(file_path)
        
        
        return jsonify({'success': 'File successfully uploaded'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')