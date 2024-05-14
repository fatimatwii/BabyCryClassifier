import os
import csv
import soundfile  # You need to install this package: `pip install SoundFile`

# Directory containing the .wav files
directory = "upload/recorded"

csv_filename = "features/csv/dataset.csv"

# Open the CSV file in write mode
with open(csv_filename, 'w', newline='') as csvfile:

    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['File Name', 'Type'])

    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            # Get the file type using soundfile library
            file_type =filename
            add= directory+"/"+filename
            
            # Write the file name and type to the CSV file
            csv_writer.writerow([add, file_type])
    
