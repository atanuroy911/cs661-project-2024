import numpy as np
import pandas as pd
import cv2
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bnlp import BengaliCorpus as corpus

df = pd.read_csv('NewsData/1000DaysNews.csv')
print(df.columns)
print(df.shape)
df.head()


def clean(text):
    text = re.sub('[%s]' % re.escape(corpus.punctuations), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('\xa0', '', text)
    return text
cleaned_text = df['description'].apply(lambda x: clean(str(x)))


refined_sentence = " ".join(cleaned_text)


def get_mask(img_path):
    img = cv2.imread(img_path, -1)
    if img.shape[2] == 3:
        return img
    return cv2.bitwise_not(img[:, :, 3])


mask = get_mask("bdmap.png")
regex = r"[\u0980-\u09FF]+"
wc = WordCloud(width=800, height=400,mode="RGBA",background_color=None,colormap="hsv", mask=mask,stopwords = corpus.stopwords,
font_path="kalpurush.ttf",regexp=regex).generate(refined_sentence)
plt.figure(figsize=(15, 7))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
result = wc.to_file("Bengali_word_cloud.png")