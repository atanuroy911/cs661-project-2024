!pip install BERTopic
!pip install sentence_transformers
!pip install googletrans==4.0.0-rc1

!pip install -U bnlp_toolkit
!pip install datamapplot

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from bertopic.representation import KeyBERTInspired

import json
import os
from bnlp import CleanText

# Configure the CleanText utility from bnlp
bnlp_clean_text = CleanText(
   fix_unicode=True,
   unicode_norm=True,
   unicode_norm_form="NFKC",
   remove_url=False,
   remove_email=False,
   remove_emoji=False,
   remove_number=False,
   remove_digits=False,
   remove_punct=True,
   replace_with_url="<URL>",
   replace_with_email="<EMAIL>",
   replace_with_number="<NUMBER>",
   replace_with_digit="<DIGIT>",
   replace_with_punct=" ")

def clean_text(text):
    """Cleans the text using bnlp's CleanText and replaces/removes tab characters."""
    # Use bnlp's CleanText
    text = bnlp_clean_text(text)
    # Replace tabs with a space
    text = text.replace("\t", " ")
    # Further cleaning steps can be added here if necessary
    return text


def read_lyrics_from_json(json_file_path):
    """Read lyrics from a JSON file, clean them, and return them as a list of strings."""
    lyrics_list = []
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        lyrics_dict = json.load(json_file)
        # Clean each lyric string and add it to the lyrics list
        lyrics_list.extend(clean_text(lyric) for lyric in lyrics_dict.values())
    return lyrics_list


def read_lyrics_recursively(folder_path):
    all_lyrics = []
    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                # Construct full file path
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    lyrics_dict = json.load(json_file)
                    # Clean and extend all lyrics in the JSON file to the list
                    all_lyrics.extend([clean_text(lyric) for lyric in lyrics_dict.values()])
    return all_lyrics

from googletrans import Translator, LANGUAGES

def translate_text(input_dict, dest_lang='en'):
    # Create a translator object
    translator = Translator()

    # Output dictionary
    output_dict = {}

    # Iterate over the input dictionary
    for key, value_list in input_dict.items():
        # Prepare a list to store translated tuples
        translated_list = []

        for text, score in value_list:
            try:
                translation = translator.translate(text, dest=dest_lang)
                translated_text = translation.text

            except Exception as e:
                print("Translation failed:", e)
                translated_text = text  # Fallback to original text

            # Check if the length of the translated text is more than 14 characters
            if len(translated_text) < 25:
                translated_list.append((translated_text, score))
            else:
                print(f"Translated word '{text}' exceeds 25 characters.")
                translated_list.append((text, score))

        # Store the translated list in the output dictionary using the same key
        output_dict[key] = translated_list

    return output_dict

lyricist_json_paths = ['/kaggle/input/bangla-songs/Kazi Nazrul Islam.json']  # Add paths to your JSON files
all_lyrics = []
lyrics_root_path = '/kaggle/input/allsongs/Json_songs'
all_lyrics = read_lyrics_recursively(lyrics_root_path)

#for json_path in lyricist_json_paths:
#    all_lyrics.extend(read_lyrics_from_json(json_path))

print(len(all_lyrics))
print(all_lyrics[0])

sentence_model = SentenceTransformer("l3cube-pune/bengali-sentence-bert-nli")

#sentence_model.max_seq_length

sentence_model[0].auto_model.config.max_position_embeddings

import re
from bnlp import NLTKTokenizer, BengaliPOS
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic

# Initialize BNLP tools
bnltk = NLTKTokenizer()
bn_pos = BengaliPOS(tokenizer=bnltk.word_tokenize)

# Mapping function to convert tags to Universal POS tags
def map_tags(word_tag_list):
    mapping = {
        'N.*': 'NOUN',
        'V.*': 'VERB',
        'PPR.*': 'PRON',
        'PRF.*': 'PRON',
        'PRC.*': 'PRON',
        'PRL.*': 'PRON',
        'PWH.*': 'PRON',
        'JJ.*': 'ADJ',
        'JQ.*': 'NUM',
        'DAB.*': 'DET',
        'DRL.*': 'DET',
        'DWH.*': 'DET',
        'AMN.*': 'ADV',
        'ALC.*': 'ADV',
        'LV.*': 'VERB',
        'LC.*': 'PART',
        'CCD.*': 'CCONJ',
        'CSB.*': 'SCONJ',
        'CCL.*': 'PART',
        'CIN.*': 'INTJ',
        'CX.*': 'X',
        'PP': 'ADP',
        'PU': 'PUNCT',
        'RDF': 'X',
        'RDS': 'SYM',
        'RDX': 'X',
    }

    mapped_list = []
    for word, tag in word_tag_list:
        universal_tag = 'X'  # Default to 'X' for unmatched tags
        for pattern, uni_tag in mapping.items():
            if re.match(pattern, tag):
                universal_tag = uni_tag
                break
        mapped_list.append((word, universal_tag))

    return mapped_list

# Custom tokenizer function that uses BNLP tokenizer and POS tagger
def custom_tokenizer(text):
    word_tag_list = bn_pos.tag(text)
    mapped_tags = map_tags(word_tag_list)
    filtered_tokens = [word for word, tag in mapped_tags if tag in {'NOUN'}]
    #filtered_tokens = [word for word, tag in mapped_tags]
    return filtered_tokens

# Create CountVectorizer with the custom tokenizer
bn_vectorizer_model = CountVectorizer(tokenizer=custom_tokenizer)

# Initialize BERTopic with the custom CountVectorizer
#topic_model = BERTopic(vectorizer_model=vectorizer_model)

from umap import UMAP
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import MaximalMarginalRelevance

ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)

#For nazrul

main_model = KeyBERTInspired(top_n_words = 20)
aspect_model = MaximalMarginalRelevance(diversity=.96)
representation_model = [main_model, aspect_model]
umap_model = UMAP(n_neighbors=3, n_components=10, metric='cosine', low_memory=False)
topic_model = BERTopic(embedding_model=sentence_model, umap_model=umap_model,
                       representation_model = representation_model,
                       ctfidf_model=ctfidf_model,
                       vectorizer_model= bn_vectorizer_model,
                       min_topic_size = 11,
                       nr_topics = 7)


#For Rabindra

main_model = KeyBERTInspired()
aspect_model = MaximalMarginalRelevance(diversity=.92)
representation_model = [main_model, aspect_model]
representation_model = KeyBERTInspired()
umap_model = UMAP(n_neighbors=16,n_components=12, metric='cosine', low_memory=False)
topic_model = BERTopic(embedding_model=sentence_model,umap_model=umap_model,
                       representation_model = representation_model,
                       ctfidf_model=ctfidf_model,
                       vectorizer_model= bn_vectorizer_model,
                       nr_topics = 11)

#For all lyricists
representation_model = KeyBERTInspired()
topic_model = BERTopic(embedding_model=sentence_model,
                       representation_model = representation_model,
                       vectorizer_model= bn_vectorizer_model)


#For top 20 lyricists based on lyrics data available (in size)

main_model = KeyBERTInspired(top_n_words = 25)
aspect_model = MaximalMarginalRelevance(diversity=.77)
representation_model = [main_model, aspect_model]
umap_model = UMAP(n_neighbors=3, n_components=20, metric='cosine', low_memory=False)
topic_model = BERTopic(embedding_model=sentence_model, umap_model=umap_model,
                       representation_model = representation_model,
                       vectorizer_model= bn_vectorizer_model,
                       ctfidf_model=ctfidf_model,
                       min_topic_size = 20,
                       nr_topics = 20)

topics, prob = topic_model.fit_transform(all_lyrics)

Old_reps = topic_model.topic_representations_
topic_model.topic_representations_ = translate_text(topic_model.topic_representations_)

topic_model.get_topic_info()

from bnlp.corpus import _stopwords
stopwords = _stopwords.bengali_stopwords

#There is some problem in this part of the code
topic_model.topic_representations_ = Old_reps
vectorizer_model = CountVectorizer(tokenizer=custom_tokenizer, stop_words = stopwords)
topic_model.update_topics(all_lyrics, vectorizer_model= bn_vectorizer_model)
#topic_model.get_topic_info()

new_topics = topic_model.reduce_outliers(all_lyrics, topics, strategy="c-tf-idf")
topic_model.update_topics(all_lyrics, topics=new_topics)

topic_model.get_topic_info()

fig = topic_model.visualize_barchart(top_n_topics = 5, title = "Analysis of Top 5 Topics",
                                     autoscale = True)
fig.write_html("/kaggle/working/all_BC_noun.html")
fig

fig = topic_model.visualize_documents(docs = all_lyrics, title = "Songs and Topics")
fig.write_html("/kaggle/working/all_DOC_noun.html")
fig

fig = topic_model.visualize_document_datamap(docs = all_lyrics, fontfamily = 'Noto Serif Bengali',
                                      title_keywords = {'fontfamily': 'Noto Serif Bengali'},
                                    sub_title_keywords= {'fontfamily': 'Noto Serif Bengali'})

fig.savefig('/kaggle/working/all_MAP_noun.svg')

fig= topic_model.visualize_topics()
fig.write_html("/kaggle/working/all_TOPICS_noun.html")
fig

topic_model.visualize_distribution(prob)

topic_model.visualize_hierarchy()



