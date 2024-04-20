import os
import csv

# Function to get list of all song files
def get_song_files(directory):
    song_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith("song"):
                song_files.append(os.path.join(root, file))
    return song_files

# Function to extract author, song name, file name, and file path from file path
def extract_song_data(file_path):
    author = os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path)
    song_name = os.path.splitext(file_name)[0].split("_", 1)[1]  # Extract song name after first underscore
    return author, song_name, file_name, file_path

# Function to write song data to CSV
def write_to_csv(song_data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Author", "Song Name", "File Name", "File Path"])
        writer.writerows(song_data)

# Main function
def main():
    input_directory = "Data"
    output_file = "SongList.csv"

    # Get list of all song files
    song_files = get_song_files(input_directory)

    # Extract author, song name, file name, and file path from each file
    song_data = []
    for file in song_files:
        author, song_name, file_name, file_path = extract_song_data(file)
        song_data.append([author, song_name, file_name, file_path])

    # Write song data to CSV
    write_to_csv(song_data, output_file)
    print("CSV file generated successfully.")

if __name__ == "__main__":
    main()
