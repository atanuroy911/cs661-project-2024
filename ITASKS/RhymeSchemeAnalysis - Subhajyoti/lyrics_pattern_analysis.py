import numpy as np
import re
import matplotlib.pyplot as plt
from bnlp.corpus import _stopwords
import ipywidgets as widgets
import os
from IPython.display import clear_output
import zipfile
import sys
import json
import scipy
from bnlp import BengaliCorpus as corpus


filepath = '../../Dataset/SongDB.json'

# To Plot the Vertical Bar Chart of Lyricist as well as Rhyme Scheme
n_top_rhymes = 6
n_top_singers = 6

# No of Author for whose entropy will be ploted in the Horizontal Bar Graph
n_author = 25

# Num of Rhymes to Plot
num_rhymes = 20


punctuations = corpus.punctuations
stopwords = _stopwords.bengali_stopwords
_vowels = corpus.vowels
with open(filepath) as f:
    data = json.load(f)


def clean(text):
	text = re.sub('[%s]' % re.escape(punctuations), '', text)
	# text = re.sub('\n', '', text)
	text = re.sub('\w*\d\w*', '', text)
	text = re.sub('\xa0', '', text)
	return text


def form_rhyme_dict(lyrics, rhyme_dict = dict()):
    x = lyrics.split('\n\n\n\n')
    for i in x:
        if len(i) == 0:
            continue
        rhyme = []
        last_chars = ''
        latest_rhyme_char_ASCII = 65
        y = i.split('\n\n')
        j = 0
        for _line in y:
            if len(_line) == 0 or _line == ' ':
                continue
            dep_vowels_flag = 0
            if _line[-1] in _vowels:
                new_last_char = _line[-2] + _line[-1]
                dep_vowels_flag = 1
            else:
                new_last_char = _line[-1]
            tmp = last_chars.find(new_last_char)
            last_chars = last_chars + new_last_char
            if tmp != (-1):
                rhyme.append(rhyme[tmp])
            else:
                rhyme.append(chr(latest_rhyme_char_ASCII))
                latest_rhyme_char_ASCII = latest_rhyme_char_ASCII + 1
            if dep_vowels_flag:
                rhyme.append(0)
        rhyme = [i for i in rhyme if i != 0]
        rhyme = ''.join(i for i in rhyme)
        if rhyme == '':
            continue
        tmp = (rhyme + rhyme).find(rhyme, 1, -1)
        if tmp != (-1):
            rhyme = rhyme[:tmp]
        if rhyme in rhyme_dict:
            rhyme_dict[rhyme] = rhyme_dict[rhyme] + 1
        else:
            rhyme_dict[rhyme] = 1
    return rhyme_dict

dict_list = dict()
for singer in list(data.keys()):
	singer_dict = dict()
	for song in data[singer]:
		lyrics = song['Lyrics']
		if len(lyrics) != 0:
			cleaned_lyrics = clean(lyrics)
			print(song)
			print(singer)
			singer_dict = form_rhyme_dict(cleaned_lyrics, singer_dict)
	dict_list[singer] = singer_dict


# Initialize an empty dictionary to store key sums
key_sums = {}

# Iterate through each dictionary
for sub_dict in dict_list.values():
    # Iterate through each key-value pair in the sub-dictionary
    for key, value in sub_dict.items():
        # Update the sum of the key in key_sums dictionary
        key_sums[key] = key_sums.get(key, 0) + value

_sum = []
for key, sum_value in key_sums.items():
    _sum.append(sum_value)



# Forming a dict of singer name and its corresponding number of songs
lyrics_count = dict()
for singer in data:
    lyrics_count[singer] = len(data[singer])
sorted_lyricist_count = dict(sorted(lyrics_count.items(), key = lambda key_val: key_val[1] , reverse = True))

sorted_unique_key_sums = dict(sorted(key_sums.items(), key = lambda key_val: key_val[1], reverse = True))



fig = plt.figure(figsize = (15, 7))
color_list = ['r', 'g', 'b', 'c', 'm', 'y']
bar_width = 0.10
x = np.arange(n_top_rhymes)
for i in range(0, n_top_singers):
    singer_name = list(sorted_lyricist_count.items())[i][0]
    singer_dict = dict_list[singer_name]
    total_lyrics = sum(list(singer_dict.values()))
    values = []
    for j in list(sorted_unique_key_sums.keys())[0:n_top_rhymes]:
        values.append(singer_dict[j] / total_lyrics)
    x = [y + bar_width for y in x]
    plt.bar(x , values, color = color_list[i-2], width = bar_width, label = singer_name, edgecolor ='grey')
plt.xlabel('Rhyme Scheme')
plt.ylabel('Count')
plt.xticks([r + (bar_width) for r in range(n_top_rhymes)], 
        list(sorted_unique_key_sums.keys())[:n_top_rhymes])
plt.title('Use of Top Most Rhyme Scheme amongst Top Most Authors')
plt.legend()
plt.savefig('Plot3.png', bbox_inches='tight')  # Save plot as PNG

plt.show()
        
"""
 As we have very skewed distributed of songs across, we have normalized the counts of rhymes across each author. Here we can see that the rhymes 'A' is most used.
 We can see that the rhyming scheme of Rabindranath and Kazi Nazrul Islam is consistent. However, the bar plot shows that the Folk Songs (Fokir Lalon Shah)
 follows different types of rhyming schemes.
"""




def calc_entropy(dict_list, sorted_lyricist_count, n_author):
    entropy_dict = dict()
    for singer in list(sorted_lyricist_count.keys())[0:n_author]:
        entropy_dict[singer] = scipy.stats.entropy(list(dict_list[singer].values()))
    return entropy_dict



def cal_entropy_and_plot(dict_list, sorted_lyricist_count, n_author):

    entropy_dict = calc_entropy(dict_list, sorted_lyricist_count, n_author)
    sorted_entropy_dict = dict(sorted(entropy_dict.items(), key = lambda key_val: key_val[1], reverse = True))

    # Plot a Horizontal Bar Plot
    y = list(sorted_entropy_dict.keys())[0:n_author]
    x = list(sorted_entropy_dict.values())[0:n_author]
    fig = plt.figure(figsize = (15, 7))
    plt.barh(y, x)
    plt.xlabel('Entropy')
    plt.ylabel('Lyricist')
    plt.title('Comparing Entropy of lyricist')
    plt.savefig('Plot2.png', bbox_inches='tight')  # Save plot as PNG

    plt.show()
    return None


cal_entropy_and_plot(dict_list, sorted_lyricist_count, n_author)



# Plot Histogram of Lyrics by Rabindranath Tagore
def plot_histogram(singer_name, num_rhymes = 20):
    singer_dict = dict_list[singer_name]
    sorted_data = sorted(singer_dict.items(), key = lambda key_val: key_val[1], reverse= True)[0:num_rhymes]
    y = [i[1] for i in sorted_data]
    x = [i[0] for i in sorted_data]
    fig = plt.figure(figsize = (15, 7))
    plt.barh(x, y)
    plt.xlabel('Count')
    plt.ylabel('Rhyme Schemes')
    plt.title('Rhyme Scheme Distribution of {}'.format(singer_name))
    plt.savefig(f'Plot1{singer_name}.png', bbox_inches='tight')  # Save plot as PNG
    plt.show()

    return None



plot_histogram('Rabindra Nath Tagore', num_rhymes)


plot_histogram('Kazi Nazrul Islam', num_rhymes)

plot_histogram('Fokir Lalon Shai', num_rhymes)

plot_histogram('Zia', num_rhymes)