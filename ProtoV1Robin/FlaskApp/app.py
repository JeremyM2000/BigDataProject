from flask import Flask, request, jsonify, render_template
import io
import torchaudio
from modules.functions import convert_webm_to_wav_memory
from modules.mlfunctions import predict, prepare_spectrogram

app = Flask(__name__)


@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)

@app.route("/capture-test")
def capture_test(name=None):
    return render_template('capture-test.html', name=name)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    webm_file = request.files['audioFile']

    if webm_file:
        # Lire le contenu du fichier en mémoire
        input_io = io.BytesIO(webm_file.read())

        # Préparer un flux de sortie pour le WAV
        output_io = io.BytesIO()

        # Convertir WebM en WAV en mémoire
        convert_webm_to_wav_memory(input_io, output_io)

        # Charger l'audio WAV en mémoire
        wave, sr = torchaudio.load(output_io)
        print(wave)
        print(type(wave))
        print(sr)
        print(type(sr))

        # Application de la prédiction
        mel = prepare_spectrogram(wave)
        print(mel.shape)
        print(mel)
        prediction = predict(wave)
        print(prediction)
        # # Retourner la réponse avec les détails de la prédiction
        return jsonify({
            'success': 'File processed successfully',
            'prediction': 'prediction'
        })

    return jsonify({'error': 'Unsupported file'}), 400

if __name__ == '__main__':
    app.run(debug=True)
