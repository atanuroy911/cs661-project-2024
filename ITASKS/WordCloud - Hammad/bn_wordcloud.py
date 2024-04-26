import numpy as np
import pandas as pd
import cv2
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# from bnlp.corpus import stopwords, punctuations
from bnlp.corpus import _stopwords
from bnlp.corpus import corpus
import docx2txt
import ipywidgets as widgets
import os
from IPython.display import clear_output
import zipfile
import sys
import locale

locale.setlocale(locale.LC_ALL, '')

punctuations = corpus.BengaliCorpus.punctuations
stopwords = _stopwords.bengali_stopwords
def clean(text):
	text = re.sub('[%s]' % re.escape(punctuations), '', text)
	text = re.sub('\n', '', text)
	text = re.sub('\w*\d\w*', '', text)
	text = re.sub('\xa0', '', text)
	return text

def get_mask(img_path):
	img = cv2.imread(img_path, -1)
	if img.shape[2] == 3:
		return img
	return cv2.bitwise_not(img[:, :, 3])

def generate_wordcloud(singer):
	path = ''
	path = os.path.join(path, '..')
	path = os.path.join(path, '..')
	path = os.path.join(path, 'Dataset')
	path = os.path.join(path, 'Data')
	path = os.path.join(path, singer)
	print(path)
	lyrics = ''
	for song in os.listdir(path):
		tmp = os.path.join(path, song)
		try:
			lyrics += docx2txt.process(tmp)
			# save lyris to a file
			with open('lyrics.txt', 'w') as f:
				f.write(lyrics)
		except zipfile.BadZipFile:
			pass

	cleaned_lyrics = clean(lyrics)
	mask = get_mask("circle.png")
	regex = r"[\u0980-\u09FF]+"
	wc = WordCloud(width=800, height=400,mode="RGBA",background_color="Black", colormap="hsv", mask=mask, stopwords = stopwords, font_path="Kalpurush.ttf",regexp=regex).generate(cleaned_lyrics)
	#plt.figure(figsize=(15, 7))
	#plt.imshow(wc, interpolation='bilinear')
	#plt.axis("off")
	#plt.show()
	result = wc.to_file("Bengali_word_cloud.png")

singer = sys.argv[1]
generate_wordcloud(singer)
