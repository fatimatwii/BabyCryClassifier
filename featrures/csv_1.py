import os
import csv
import soundfile  # You need to install this package: `pip install SoundFile`

# Directory containing the .wav files
directory = "dataset1"

# Name of the CSV file to create
csv_filename = "full-dataset.csv"

# Open the CSV file in write mode
with open(csv_filename, 'w', newline='') as csvfile:

    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['File Name', 'Type'])

    for shift in os.listdir(directory):
        for filename in os.listdir(directory+"/"+shift):
            # Check if the file is a .wav file
            if filename.endswith(".wav"):
                # Get the file type using soundfile library
                file_type =shift
                add= directory+"/"+shift+"/"+filename
                filename=add
                
                # Write the file name and type to the CSV file
                csv_writer.writerow([filename, file_type])
    directory = "aug-dataset1"
    for shift in os.listdir(directory):
        for filename in os.listdir(directory+"/"+shift):
            # Check if the file is a .wav file
            if filename.endswith(".wav"):
                # Get the file type using soundfile library
                file_type =shift
                add= directory+"/"+shift+"/"+filename
                filename=add
                
                # Write the file name and type to the CSV file
                csv_writer.writerow([filename, file_type])

        
    
