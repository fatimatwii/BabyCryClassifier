import librosa
import librosa.display
import IPython.display as ipd
import os
import numpy as np
import csv

def feature_exectraction(file_path, count):
    x, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
    mfcc = np.mean(librosa.feature.mfcc(y=x, sr=sample_rate, n_mfcc=count).T, axis=0)

    return mfcc

csv_dataset1 = "aug-dataset1.csv"
for count in range(5,101,5):
    print(count)
    with open(csv_dataset1, 'r', newline='') as csvfile :
        csv_reader=csv.reader(csvfile)
        next(csv_reader)
        directory="aug-features"
        csv_filename = directory+"/"+str(count)+"_features.csv"
        with open(csv_filename, 'w', newline='') as csvfile1:
            csv_writer = csv.writer(csvfile1)
            csv_writer.writerow(['Features', 'Type'])
            print ("midle of "+ str(count))
            for line in csv_reader:
                
                csv_writer.writerow([feature_exectraction(line[0],count),line[1]])
            print ("end of "+ str(count))
                
            

