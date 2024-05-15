# functions.py

import os
import shutil
import csv
import numpy as np
import pandas as pd
import librosa
import tensorflow as tf
from pydub import AudioSegment

UPLOAD_FOLDER = 'upload'

CSV_FOLDER = 'features/csv'
FEATURES_FOLDER = 'features'

def get_next_record_number():
    record_files = [file for file in os.listdir(UPLOAD_FOLDER) if file.startswith('record')]
    if record_files:
        record_numbers = [int(file.split('.')[0].replace('record', '')) for file in record_files]
        return max(record_numbers) + 1
    else:
        return 1
    
def add_uploaded_to_dataset(filename):
    with open(os.path.join(CSV_FOLDER, 'dataset.csv'), 'a', newline='') as csvfile:
         csv_writer = csv.writer(csvfile)
         csv_writer.writerow([filename])
    shutil.copy(os.path.join(UPLOAD_FOLDER, filename), os.path.join(CSV_FOLDER, filename))

def add_recorded_to_dataset(filename):
    with open(os.path.join(CSV_FOLDER, 'dataset.csv'), 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([filename])
    shutil.copy(os.path.join(UPLOAD_FOLDER, RECORDED_FOLDER, filename), os.path.join(CSV_FOLDER, filename))

def feature_Extraction(file_path):
    x, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
    mfcc = np.mean(librosa.feature.mfcc(y=x, sr=sample_rate, n_mfcc=100).T, axis=0)
    return mfcc

def extract_features():
    with open(os.path.join(CSV_FOLDER, 'dataset.csv'), 'r', newline='') as csvfile:
       csv_reader = csv.reader(csvfile)
       next(csv_reader)
       for line in csv_reader:
            file_path = os.path.join(CSV_FOLDER, line[0])  
            print("Processing:", file_path)  
            try:
                features = feature_Extraction(file_path)
                row = features.tolist()
                return row
            except Exception as e:
                print("Error processing:", file_path)
                print(e)
    return row
def normalize(row):
    # Initialize arrays to store min and max values for each feature column
     min_values = []
     max_values = []
     csv1=CSV_FOLDER+'/min_max_values.csv'
     # Read the CSV file  
     with open(csv1, 'r', newline='') as csvfile :
      csv_reader=csv.reader(csvfile)
      next(csv_reader)
      for line in csv_reader:
        min_val = float(line[1])  # Convert to float
        max_val = float(line[2])  # Convert to float
        min_values.append(min_val)
        max_values.append(max_val)  
     row1=[]
     
         # Normalize the feature columns between 0 and 1 using the min and max values
     for i in range(len(row)):
        normalized_val = (row[i] - min_values[i]) / (max_values[i] - min_values[i])
        row1.append(normalized_val)
     return row1 
     

def decode(labels):
    decoded_labels = []
    for label in labels:
        if label == 1:
            decoded_labels.append('belly_pain')
        elif label == 2:
            decoded_labels.append('burping')
        elif label == 3:
            decoded_labels.append('discomfort')
        elif label == 4:
            decoded_labels.append('hungry')
        elif label == 5:
            decoded_labels.append('tired')
        else:
            decoded_labels.append('unknown')
    return decoded_labels


def predict(norm):
    loaded_model = tf.keras.models.load_model('features/my_model.h5')
# Assuming you have new_data that is preprocessed and normalized between 0 and 1
    
    data_array = np.vstack([norm, norm])
# Use the loaded model to make predictions on the new data
    predictions = loaded_model.predict(data_array)
    predicted_labels = np.argmax(predictions, axis=1)+1
    x=decode(predicted_labels)
    return x

def process_audio(filename):
    row = extract_features()
    norm= normalize(row)
    result = predict(norm)
    return result


def clear_csv(file_path):
    try:
        # Read the header from the CSV file
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
        
        # Write only the header back to the CSV file
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
        print(f"Cleared all rows in {file_path}.")
    except Exception as e:
        print(f"Error clearing rows in {file_path}: {e}")
        raise

def clear_csv_except_header(file_path):
    try:
        df = pd.read_csv(file_path)
        df.iloc[0:1].to_csv(file_path, index=False)
        print(f"Cleared all rows in {file_path} except for the header.")
    except Exception as e:
        print(f"Error clearing rows in {file_path}: {e}")
        raise

