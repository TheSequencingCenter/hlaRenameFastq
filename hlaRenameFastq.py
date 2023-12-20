#!/usr/bin/env python

import os
import sys
import pathlib
import csv
import re

"""
This script processes CSV data exported from AirTable, specifically dealing with sample data in a genetics laboratory setting.
It cleans the CSV file, validates necessary files, and renames FASTQ files according to specific naming conventions.
"""

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

"""
The script begins by setting the working directory to the user's Downloads folder.
If the 'airtable_data.csv' file exists from a previous run, it is removed to avoid conflicts.
"""

# Remove non-alphanumeric characters that are created from the AirTable export. Then rename the csv to airtable_data.
try:
    original_file = open('HLA Samples-Grid view.csv').read()
except FileNotFoundError:
    print('ERROR: HLA Samples-Grid view.csv file not found.')
    sys.exit(1)  # Exit the script if the file is not found

# Cleaning up the exported CSV file
reg_fix = re.sub('[^a-zA-Z0-9\s\n\.\,\-\_\0357\0273\0277]', '',  original_file)
open('airtable_data.csv', 'w').write(reg_fix)

"""
Here, the script reads an exported CSV file, cleans it by removing non-alphanumeric characters,
and then writes the cleaned data into a new file named 'airtable_data.csv'.
"""

# File validation and setup
airtable_data = pathlib.Path.cwd() / 'airtable_data.csv'
fastq_directory = pathlib.Path.cwd() / 'exported_fastq'
required_files = [airtable_data, fastq_directory]

# Validation check to confirm required files are present.
for f in required_files:
    if not f.exists():
        raise Exception('ERROR: Either the required airtable_data.csv file or the exported_fastq directory were not found.')

"""
The script then checks for the presence of the necessary 'airtable_data.csv' file and 'exported_fastq' directory.
If either is missing, an exception is raised and the script terminates.
"""

# Processing CSV data and renaming files
with open(airtable_data, 'r') as csvfile:
    airtable_reader = csv.DictReader(csvfile, delimiter = ',')
    list_of_sample_ids = []
    os.chdir(fastq_directory)

    # Renames files to remove the unwanted labels and adds in client label.
    for f in os.listdir():
        f_name, f_ext = f.split(os.extsep,1)
        if f_ext == "fastq.gz":
            try:
                f_sampleid, f_s, f_L, f_R, f_001 = (f_name.split('_'))
            except ValueError:
                print('ERROR: The file naming convention does not match the expected pattern for renaming.')
                sys.exit(1)

            csvfile.seek(0)
            
            for row in airtable_reader:
                if row['Sample ID'] == f_sampleid:
                    list_of_sample_ids.append(f_sampleid)
                    client_label = row['Client Vial Label']
                    new_file_name = ('{}_{}_{}_{}.{}'.format(f_sampleid, client_label, f_R, f_001, f_ext))
                    os.rename(f, new_file_name)

"""
In this section, the script reads the 'airtable_data.csv' file, iterates over the files in the 'exported_fastq' directory,
and renames the FASTQ files according to a specific format that includes the sample ID and client label.
"""

# We're done
print('Renaming files...')
print('Done')
