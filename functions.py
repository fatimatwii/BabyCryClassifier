from flask import Flask, render_template, request, send_from_directory
import os
from pydub import AudioSegment
import mimetypes
from functions import *

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
CSV_FOLDER = 'features/csv'
FEATURES_FOLDER = 'features'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER
app.config['FEATURES_FOLDER'] = FEATURES_FOLDER

record_count = get_next_record_number()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global record_count
    audio_file = request.files.get('audio_file')
    result="none"
    if audio_file:
        filename = f'audio{record_count}.wav'
        audio_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Convert to WAV
        audio = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        wav_filename = f'audio{record_count}.wav'
        audio.export(os.path.join(app.config['UPLOAD_FOLDER'], wav_filename), format="wav")
        add_uploaded_to_dataset(wav_filename)
        result = process_audio(wav_filename)
        record_count += 1
        #clear_csv(os.path.join(app.config['CSV_FOLDER'], 'dataset.csv'))
        #clear_csv(os.path.join(app.config['CSV_FOLDER'], 'normalized_data.csv'))
        #clear_csv(os.path.join(app.config['CSV_FOLDER'], 'features.csv'))
        os.remove(os.path.join(app.config['CSV_FOLDER'], wav_filename))
        return render_template('index.html', file_path=wav_filename, result=result)

    return render_template('index.html', result=result)
    
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(app.config['RECORDED_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
