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
RECORDED_FOLDER = 'recorded'
CSV_FOLDER = 'features/csv'
FEATURES_FOLDER = 'features'

def get_next_record_number():
    record_files = [file for file in os.listdir(os.path.join(UPLOAD_FOLDER, RECORDED_FOLDER)) if file.startswith('record')]
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
    csv_file_path = os.path.join(CSV_FOLDER, 'dataset.csv')
    with open(csv_file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([filename])
    src_path = os.path.join(UPLOAD_FOLDER, RECORDED_FOLDER, filename)
    dest_path = os.path.join(CSV_FOLDER, filename)
    print(f"Copying recorded file from {src_path} to {dest_path}")  # Debugging statement
    shutil.copy(src_path, dest_path)

def feature_Extraction(file_path):
    x, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
    mfcc = np.mean(librosa.feature.mfcc(y=x, sr=sample_rate, n_mfcc=100).T, axis=0)
    return mfcc

def extract_features():
    with open(os.path.join(CSV_FOLDER, 'dataset.csv'), 'r', newline='') as csvfile:
       csv_reader = csv.reader(csvfile)
       next(csv_reader)
       csv_filename = CSV_FOLDER + "/features.csv"
       with open(csv_filename, 'w', newline='') as csvfile1:
        csv_writer = csv.writer(csvfile1)
        csv_writer.writerow([f'Feature_{i+1}' for i in range(100)])
        for line in csv_reader:
            file_path = os.path.join(CSV_FOLDER, line[0])  
            print("Processing:", file_path)  
            try:
                features = feature_Extraction(file_path)
                row = features.tolist()
                csv_writer.writerow(row)
            except Exception as e:
                print("Error processing:", file_path)
                print(e)

def normalize():
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

     # Read the CSV file
     df = pd.read_csv(CSV_FOLDER+"/features.csv")

     # Extract the feature columns (excluding the 'type' column)
     feature_columns = df.columns

    # Normalize the feature columns between 0 and 1 using the min and max values
     for i, col in enumerate(feature_columns):
       df[col] = (df[col] - min_values[i]) / (max_values[i] - min_values[i])
     duplicated_df = pd.concat([df, df])  
     # Save the normalized data back to a CSV file
     duplicated_df.to_csv(CSV_FOLDER+"/normalized_data.csv", index=False)   
     

def decode(line):
     match line:
                case 1:
                    return 'belly_pain'
                    
                case 2:
                    return 'burping'
                    
                case 3:
                    return 'discomfort'
                    
                case 4:
                    return 'hungry'
                    
                case 5:
                    return 'tired' 

def predict():
    loaded_model = tf.keras.models.load_model('features/my_model.h5')
# Assuming you have new_data that is preprocessed and normalized between 0 and 1
    new_data = pd.read_csv("features/csv/normalized_data.csv",skiprows=1)
    data_array = new_data.values
# Use the loaded model to make predictions on the new data
    predictions = loaded_model.predict(data_array)
    predicted_labels = np.argmax(predictions, axis=1)+1
    x=decode(predicted_labels)
    return x

def process_audio(filename):
    extract_features()
    normalize()
    result = predict()
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
