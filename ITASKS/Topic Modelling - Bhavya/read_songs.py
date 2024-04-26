import os
import json
import docx2txt
import zipfile
import re
import csv

def clean(text):
    # Define only the specific punctuations to be removed
    punctuations = '/()[]{}~@#$%^&.*'
    
    # Remove sequences of specified punctuations
    text = re.sub('[%s]+' % re.escape(punctuations), '', text)
    
    # Remove both types of ellipses (manual three dots and special character)
    text = re.sub(r'\.\.\.|\…+', '', text)
    
    # Replace tab characters with a single space
    text = re.sub('\t', ' ', text)
    
    # Remove newline characters
    text = re.sub('\n', '', text)
    
    # Remove words containing digits
    text = re.sub(r'\w*\d\w*', '', text)
    
    # Remove non-breaking space characters
    text = re.sub('\xa0', '', text)
    
    return text

bad_zipfile_count = 0

def read_docx(file_path):
    global bad_zipfile_count
    try:
        return docx2txt.process(file_path)
    except zipfile.BadZipFile:
        bad_zipfile_count += 1
        print(f"File is not a zip file: {file_path}")
        return ""  # Return an empty string if the file is not a proper DOCX

# ... rest of your code ...

def process_lyricist_directory(lyricist_path, output_directory):
    """Processes all DOCX files in a lyricist's directory and creates a JSON file in the specified directory."""
    lyrics_dict = {}
    for filename in os.listdir(lyricist_path):
        if filename.endswith(".docx"):
            file_path = os.path.join(lyricist_path, filename)
            lyrics = read_docx(file_path)
            lyrics = clean(lyrics)
            lyrics_dict[filename] = lyrics.strip()

    # Create or update JSON file for the lyricist
    lyricist_name = os.path.basename(lyricist_path)
    json_filename = f"{lyricist_name}.json"
    json_file_path = os.path.join(output_directory, json_filename)  # Path to the output directory for JSON files
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(lyrics_dict, json_file, ensure_ascii=False, indent=4)

def process_all_lyricists(main_path, output_directory):
    """Recursively processes each lyricist's subfolder in the main directory and writes JSON to the specified directory."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for lyricist_name in os.listdir(main_path):
        lyricist_path = os.path.join(main_path, lyricist_name)
        if os.path.isdir(lyricist_path):
            process_lyricist_directory(lyricist_path, output_directory)

main_directory_path = "C:\\Users\\gbhav\\Downloads\\BanglaMusicDataset\\BanglaMusicStylo Dataset\\Data"
json_output_directory = "C:\\Users\\gbhav\\Downloads\\BanglaMusicDataset\\BanglaMusicStylo Dataset\\json_new"  # Define where you want the JSON files to be saved
process_all_lyricists(main_directory_path, json_output_directory)
print(f"BadZipFile encountered. Count: {bad_zipfile_count}")