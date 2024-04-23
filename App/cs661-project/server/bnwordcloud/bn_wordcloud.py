import numpy as np
import pandas as pd
import cv2
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bnlp.corpus import _stopwords
from bnlp.corpus import corpus
import json
import os

# Setting locale for handling text data
import locale
locale.setlocale(locale.LC_ALL, '')

# Define punctuations and stopwords
punctuations = corpus.BengaliCorpus.punctuations
stopwords = _stopwords.bengali_stopwords

# Function to clean text
def clean(text):
    text = re.sub('[%s]' % re.escape(punctuations), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('\xa0', '', text)
    return text

# Function to get mask for word cloud
def get_mask(img_path):
    img = cv2.imread(img_path, -1)
    if img.shape[2] == 3:
        return img
    return cv2.bitwise_not(img[:, :, 3])

# Function to read lyrics from JSON file for a specific lyricist
def read_lyrics_for_lyricist(json_path, lyricist_name):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        lyricist_songs = []
        for lyricist, songs in data.items():
            if lyricist == lyricist_name:
                for song in songs:
                    lyricist_songs.append((song['Song Name'], song['Lyrics']))
                break  # No need to continue searching if lyricist is found
        return lyricist_songs

# Function to generate word cloud for all songs combined
def generate_combined_wordcloud(lyricist_name, song_data):
    lyrics = ''
    for song_name, song_lyrics in song_data:
        lyrics += song_lyrics

    cleaned_lyrics = clean(lyrics)
    mask = get_mask("./assets/circle.png")
    regex = r"[\u0980-\u09FF]+"
    wc = WordCloud(width=800, height=400, mode="RGBA", background_color="White", colormap="hsv", mask=mask, stopwords=stopwords, font_path="./assets/Kalpurush.ttf", regexp=regex).generate(cleaned_lyrics)
    result = wc.to_file(f"./generated/{lyricist_name}_combined_word_cloud.png")
    return (f"./generated/{lyricist_name}_combined_word_cloud.png")

# Function to generate word cloud for a single song
def generate_single_song_wordcloud(lyricist_name, song_name, song_lyrics):
    cleaned_lyrics = clean(song_lyrics)
    mask = get_mask("./assets/circle.png")
    regex = r"[\u0980-\u09FF]+"
    wc = WordCloud(width=800, height=400, mode="RGBA", background_color="White", colormap="hsv", mask=mask, stopwords=stopwords, font_path="./assets/Kalpurush.ttf", regexp=regex).generate(cleaned_lyrics)
    result = wc.to_file(f"./generated/{lyricist_name}_{song_name}_word_cloud.png")
    return (f"./generated/{lyricist_name}_{song_name}_word_cloud.png")

# Main function
def main(lyricist_name, song_name=None):
    # Path to the JSON file
    json_path = 'SongDB.json'

    # Read the data from JSON file for the specified lyricist
    song_data = read_lyrics_for_lyricist(json_path, lyricist_name)

    if song_name is None:
        # Generate word cloud for all songs combined
        result = generate_combined_wordcloud(lyricist_name, song_data)
    else:
        # Find the specified song
        for song in song_data:
            if song[0] == song_name:
                # Generate word cloud for the specified song
                result = generate_single_song_wordcloud(lyricist_name, song_name, song[1])
                break
        else:
            print(f"Song '{song_name}' not found for lyricist '{lyricist_name}'")
            return None

    return result

# if __name__ == "__main__":
#     # Get lyricist name from command line arguments
#     import sys
#     if len(sys.argv) < 2:
#         print("Usage: python script.py <Lyricist Name> [Song Name]")
#         sys.exit(1)
    
#     lyricist_name = sys.argv[1]
#     song_name = sys.argv[2] if len(sys.argv) == 3 else None
#     main(lyricist_name, song_name)
