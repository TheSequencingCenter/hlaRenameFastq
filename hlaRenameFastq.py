import argparse
import os
import sys
import pathlib
import csv
import re

"""
Script Name: hlaRenameFastq.py
Purpose: This script is designed to process and rename FASTQ files based on CSV data exported from AirTable, 
         specifically for handling sample data in genetics research. It cleans the CSV file, validates necessary files, 
         and renames FASTQ files according to specific naming conventions and client labels.


Usage:
python3 hlaRenameFastq.py -h
python3 hlaRenameFastq.py --help
"""

# Setting up command line argument parser
parser = argparse.ArgumentParser(description='Rename FASTQ files based on CSV data from AirTable.')
args = parser.parse_args()

# Use the Downloads directory as the working directory
try:
    os.chdir('/Users/richardcasey/Downloads')
except FileNotFoundError:
    print('ERROR: Downloads directory not found.')
    sys.exit(1)  # Exit the script if the directory is not found

# Check for preexisting airtable_data.csv. Delete it if it exists. 
preexisting_airtabledata = pathlib.Path.cwd() / 'airtable_data.csv'
if preexisting_airtabledata.exists():
    os.remove(preexisting_airtabledata)
    print('Preexisting airtable_data.csv deleted.')

# Remove non-alphanumeric characters from the AirTable export, then save as airtable_data.csv
try:
    original_file = open('HLA Samples-Grid view.csv').read()
except FileNotFoundError:
    print('ERROR: HLA Samples-Grid view.csv file not found.')
    sys.exit(1)  # Exit the script if the file is not found

reg_fix = re.sub('[^a-zA-Z0-9\s\n\.\,\-\_\0357\0273\0277]', '',  original_file)
open('airtable_data.csv', 'w').write(reg_fix)

# File validation and setup
airtable_data = pathlib.Path.cwd() / 'airtable_data.csv'
fastq_directory = pathlib.Path.cwd() / 'exported_fastq'
required_files = [airtable_data, fastq_directory]

# Validate presence of required files
for f in required_files:
    if not f.exists():
        raise Exception('ERROR: Required airtable_data.csv file or exported_fastq directory not found.')

# Process CSV data and rename files
with open(airtable_data, 'r') as csvfile:
    airtable_reader = csv.DictReader(csvfile, delimiter = ',')
    list_of_sample_ids = []
    os.chdir(fastq_directory)

    # Rename files based on the naming convention and client label
    for f in os.listdir():
        f_name, f_ext = f.split(os.extsep,1)
        if f_ext == "fastq.gz":
            try:
                f_sampleid, f_s, f_L, f_R, f_001 = (f_name.split('_'))
            except ValueError:
                print('ERROR: File naming convention does not match expected pattern.')
                sys.exit(1)

            csvfile.seek(0)
            
            for row in airtable_reader:
                if row['Sample ID'] == f_sampleid:
                    list_of_sample_ids.append(f_sampleid)
                    client_label = row['Client Vial Label']
                    new_file_name = ('{}_{}_{}_{}.{}'.format(f_sampleid, client_label, f_R, f_001, f_ext))
                    os.rename(f, new_file_name)

# Completion message
print('Renaming files...')
print('Done')
