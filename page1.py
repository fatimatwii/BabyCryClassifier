from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload(): 
    if 'audio_file' not in request.files:
        return render_template('index.html', file_path='No file part')
    
    file = request.files['audio_file']
    if file.filename == '':
     
        return render_template('index.html', file_path='No selected file')
    
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        return render_template('index.html', file_path=file_path)

if __name__ == '__main__':
    app.run(debug=True)
