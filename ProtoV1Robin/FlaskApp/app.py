from flask import Flask, request, jsonify, render_template
import io
from modules.functions import convert_webm_to_wav_memory
from modules.mlfunctions import prepare_spectrogram, load_lstm
import os 
import torchaudio
from torch import nn
import torch 


app = Flask(__name__)
lstm = load_lstm(f'{os.getcwd()}/models/lstm-75-v4-acc-85.pth')
map = {
     0:'un',
     1:'deux',
     2:'trois',
     3:'quatre',
     4:'cinq',
     5:'six',
     6:'sept',
     7:'huit',
     8:'neuf',
     9: 'oui',
    10: 'non',
    11: 'Firefox',
    12: 'Hey',
    13: 'zéro',
    14: 'empty',
}


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
        wave = convert_webm_to_wav_memory(input_io, output_io)
        print(type(wave))
        # Charger l'audio WAV en mémoire
        wave, sr = torchaudio.load(output_io)
        print(wave)
        print(type(wave))
        print(sr)
        print(type(sr))

        # Application de la prédiction
        mel = prepare_spectrogram(wave)
        print(mel.shape)
        mel = mel.unsqueeze(0)
        print(f'mean {mel.mean()}')
        print(f'std {mel.std()}')
        print(mel.shape)
        lstm.eval()
        prediction = lstm(mel)
        print(prediction)
        result = prediction.argmax(dim=1)
        print(result.item())
        x = map[result.item()]
        # # Retourner la réponse avec les détails de la prédiction
        return jsonify({
            'success': 'File processed successfully',
            'prediction': x
        })

    return jsonify({'error': 'Unsupported file'}), 400

if __name__ == '__main__':
    app.run(debug=True)
