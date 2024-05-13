from flask import Flask, render_template, request, send_from_directory
import os
from pydub import AudioSegment
import mimetypes

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
RECORDED_FOLDER = 'recorded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RECORDED_FOLDER'] = RECORDED_FOLDER

def get_next_record_number():
    record_files = [file for file in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], app.config['RECORDED_FOLDER'])) if file.startswith('record')]
    if record_files:
        record_numbers = [int(file.split('.')[0].replace('record', '')) for file in record_files]
        return max(record_numbers) + 1
    else:
        return 1

record_count = get_next_record_number()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global record_count
    
    uploaded_audio = request.files.get('uploaded_audio')
    if uploaded_audio:
        filename = f'upload_{uploaded_audio.filename}'
        uploaded_audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Convert to WAV
        audio = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), format=mimetypes.guess_extension(uploaded_audio.content_type))
        wav_filename = f'upload_{os.path.splitext(uploaded_audio.filename)[0]}.wav'
        audio.export(os.path.join(app.config['UPLOAD_FOLDER'], wav_filename), format="wav")
        return render_template('index.html', file_path=wav_filename)
    
    
    recorded_audio = request.files.get('recorded_audio')
    if recorded_audio:
        filename = f'record{record_count}.wav'
        recorded_audio.save(os.path.join(app.config['UPLOAD_FOLDER'], app.config['RECORDED_FOLDER'], filename))
        # Convert to WAV
        audio = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER'], app.config['RECORDED_FOLDER'], filename), format=mimetypes.guess_extension(recorded_audio.content_type))
        wav_filename = f'record{record_count}.wav'
        audio.export(os.path.join(app.config['UPLOAD_FOLDER'], app.config['RECORDED_FOLDER'], wav_filename), format="wav")
        record_count += 1  
        return render_template('index.html', file_path=wav_filename)
    
    return render_template('index.html', file_path=None)

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], app.config['RECORDED_FOLDER']), filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
