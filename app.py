from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os

app = Flask(__name__)
CORS(app)

# Cargar modelo de Whisper (puede tardar)
model = whisper.load_model("tiny")

@app.route('/')
def home():
    return 'Servidor Flask funcionando correctamente.'

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No se recibió archivo de audio"}), 400

        audio_file = request.files['audio']
        if audio_file.filename == "":
            return jsonify({"error": "Nombre de archivo vacío"}), 400

        audio_path = os.path.join(os.getcwd(), "temp_audio.wav")  # ✅ Ruta absoluta
        audio_file.save(audio_path)
        print("📥 Archivo recibido:", audio_file.filename)
        print("📂 Ruta completa del archivo guardado:", audio_path)

        result = model.transcribe(audio_path, language='es')
        os.remove(audio_path)
        return jsonify({"transcripcion": result['text']})

    except Exception as e:
        print("❌ Error interno en Flask:", str(e))
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
