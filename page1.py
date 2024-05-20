# main.py

from flask import Flask, request, jsonify, render_template
import os
from functions import *

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
CSV_FOLDER = 'features/csv'
app.config['CSV_FOLDER'] = CSV_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_file' in request.files:
        audio_file = request.files['audio_file']
        filename = audio_file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        audio_file.save(filepath)

        add_uploaded_to_dataset(filename)
        prediction = process_audio(filename)
        clear_csv(os.path.join(app.config['CSV_FOLDER'], 'dataset.csv'))

        return jsonify(success=True, prediction=prediction)
    elif 'uploaded_audio' in request.files:
        audio_file = request.files['uploaded_audio']
        filename = audio_file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        audio_file.save(filepath)

        add_uploaded_to_dataset(filename)
        prediction = process_audio(filename)
        clear_csv(os.path.join(app.config['CSV_FOLDER'], 'dataset.csv'))

        return jsonify(success=True, prediction=prediction)
    else:
        clear_csv(os.path.join(app.config['CSV_FOLDER'], 'dataset.csv'))
        return jsonify(success=False, prediction="")

if __name__ == '__main__':
    app.run(debug=True)
