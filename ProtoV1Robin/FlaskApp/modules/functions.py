import subprocess


# Exemple de fonction pour convertir WebM en WAV en mémoire
def convert_webm_to_wav_memory(input_io, output_io):
    # Utilisez une bibliothèque ou une méthode appropriée pour convertir l'audio
    # Cela pourrait être une utilisation d'une commande ffmpeg exécutée en mémoire, par exemple:
    command = ['ffmpeg', '-i', 'pipe:0', '-acodec', 'pcm_s16le', '-ar', '48000', '-ac', '1', '-f', 'wav', 'pipe:1']
    process = subprocess.run(command, input=input_io.read(), stdout=subprocess.PIPE,  stderr=subprocess.DEVNULL)
    output_io.write(process.stdout)
    output_io.seek(0) 
    return output_io
