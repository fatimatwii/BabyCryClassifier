from flask import Flask, render_template, request, send_from_directory
import os
from pydub import AudioSegment
import mimetypes
from functions import *

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
RECORDED_FOLDER = 'recorded'
CSV_FOLDER = 'features/csv'
FEATURES_FOLDER = 'features'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RECORDED_FOLDER'] = RECORDED_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER
app.config['FEATURES_FOLDER'] = FEATURES_FOLDER

record_count = get_next_record_number()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global record_count
    
    uploaded_audio = request.files.get('audio_file')
    if uploaded_audio:
        filename = f'upload_{uploaded_audio.filename}'
        uploaded_audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Convert to WAV
        audio = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        wav_filename = f'upload_{os.path.splitext(uploaded_audio.filename)[0]}.wav'
        audio.export(os.path.join(app.config['UPLOAD_FOLDER'], wav_filename), format="wav")
        add_uploaded_to_dataset(wav_filename)
        result = process_audio(wav_filename)
        
        clear_csv(os.path.join(app.config['CSV_FOLDER'], 'dataset.csv'))
        clear_csv(os.path.join(app.config['CSV_FOLDER'], 'normalized_data.csv'))
        clear_csv(os.path.join(app.config['CSV_FOLDER'], 'features.csv'))
        return render_template('index.html', file_path=wav_filename, result=result)
    
    recorded_audio = request.files.get('recorded_audio')
    if recorded_audio:
        filename = f'record{record_count}.wav'
        recorded_audio.save(os.path.join(app.config['UPLOAD_FOLDER'], app.config['RECORDED_FOLDER'], filename))
        # Convert to WAV
        audio = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER'], app.config['RECORDED_FOLDER'], filename), format="weba")
        wav_filename = f'record{record_count}.wav'
        audio.export(os.path.join(app.config['UPLOAD_FOLDER'], app.config['RECORDED_FOLDER'], wav_filename), format="wav")
        add_recorded_to_dataset(wav_filename)
        result = process_audio(wav_filename)
        record_count += 1  
        return render_template('index.html', file_path=wav_filename, result=result)
    clear_csv(os.path.join(app.config['CSV_FOLDER'], 'dataset.csv'))
    clear_csv(os.path.join(app.config['CSV_FOLDER'], 'features.csv'))
    clear_csv(os.path.join(app.config['CSV_FOLDER'], 'normalized_data.csv'))
    return render_template('index.html', file_path=None)

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], app.config['RECORDED_FOLDER']), filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)