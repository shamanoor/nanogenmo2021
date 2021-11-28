import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
import pickle

import os

'''
    REQUIRED:
        Make a way to select a paragraph from all of the Project Gutenberg Detective Fiction stories
            Ideas of how to do this:
                * First create paragraphs from each of the stories, but keep them with their original document
                * 
'''

def create_paragraphs_list(data : str) -> list:
    # Function to split string into paragraphs, a paragraph is defined as a piece of text that is separated by two
    # or more spaces
    split_paragraphs = lambda x: x.split('\n\n')
    return [paragraph.replace('\n', '').replace('      ', ' ') for paragraph in split_paragraphs(data) if
                  len(paragraph) > 0]


def get_keywords_from_document(corpus : str, vocabulary : dict) -> dict:
    '''
    :param corpus: a list of paragraphs from which we will extract keywords
    :return: dict with index the keywords
    '''
    # Get keywords from each paragraph and add them as keys to the dict, and append the paragraph to the values list

    # Get stopwords into list
    with open('stopwords.txt', 'r') as f:
        stopwords = f.read().splitlines()

    # Step 5: Get top N keywords based on score
    vectorizer = TfidfVectorizer(max_df=0.8, ngram_range=(1, 1), vocabulary=vocabulary, stop_words=stopwords)
    vectorizer.fit(corpus)
    words_freq = vectorizer.get_feature_names()

    print(len(words_freq))

    # get counts of frequencies and return that as a dict with word:freq

    return words_freq



def get_vocabulary(corpus: str) -> list:
    """
    Count number of ocurences of a word
    :param document:
    :return:
    """
    countvect = CountVectorizer(stop_words='english')
    matrix = countvect.fit_transform(corpus)

    vocabulary = [word for word in countvect.get_feature_names_out()]

    counts = dict(zip(vocabulary, matrix.toarray().sum(axis=0)))
    counts = {k : v for k, v in sorted(counts.items(), key=lambda item: item[1])}

    return counts


def compute_vocabulary() -> dict:
    """
    TODO: put the code from if __init__ == "__main__" here
        and rename this to get_vocabulary and the other one to compute_vocabulary
    :return:
    """
    return

def compute_keywords() -> dict:
    """
    TODO: put the code from if __init__ == "__main__" here
        and rename this to get_keywords and the other one to compute_keywords
    :return:
    """
    return


def index_reddit():
    with open('data/reddit_tifu/df_tifu.pkl', 'rb') as f:
        tifu_data = pickle.load(f)

    print(tifu_data)




def build_tifu_index(index_keys: list = None, tifu_data: list = None) -> dict:
    with open('gutenberg_index.pkl', 'rb') as f:
        index = pickle.load(f)

    index_keys = list(index.keys())
    print(type(index_keys))
    print(index_keys)

    with open('build_indexes/data/reddit_tifu/df_tifu.pkl', 'rb') as f:
        tifu_data = pickle.load(f)

    tifu_data = tifu_data['documents'].tolist()

    # Step 2: Find some reddit post that somehow builds upon the previously selected paragraph
    # Ah, we can use the same index? And then add the fields from reddit...?


    reddit_idx = {}
    print("Finished reading data")
    print("Tifu_data: ", tifu_data[1])
    for post in tifu_data:
        print("post: ", post)
        for key in index_keys:
            if key in post:
                print(f"Found key {key} in a paragraph")
                if key not in reddit_idx.keys():
                    reddit_idx[key] = [post]
                else:
                    reddit_idx[key].append(post)

    with open('tifu_index.pkl', 'wb') as f:
        pickle.dump(reddit_idx, f)

    for k, v in reddit_idx.items():
        for value in v:
            print(k, value)

    return reddit_idx

if __name__ == "__main__":
    # preprocessed_dirs = ['preprocessed/gutenberg/' + dir for dir in os.listdir('preprocessed/gutenberg')]
    # print(preprocessed_dirs)
    # print(len(preprocessed_dirs))
    #
    #
    # # we process the preprocessed dirs per 10 stories
    # start_idx = 0
    # end_idx = 10
    #
    # # Build vocabulary by looping over all documents
    # complete_vocabulary = {}
    # # we need this later
    # while end_idx < len(preprocessed_dirs):
    #     # create one large string with current window's story txt's
    #     document = []
    #     print("start_idx: ", start_idx)
    #     print("end_idx: ", end_idx)
    #
    #     # process per 10 stories
    #     # loop over directory to create a paragraph list for all of them
    #     for file in preprocessed_dirs[start_idx:end_idx]:
    #         with open(file, 'r', encoding='utf-8') as f:
    #             story = f.read()
    #             document.append(story)
    #
    #     # join the corpus with two newline characters
    #     document = '\n\n'.join(document)
    #     document = document.replace('_', ' ')
    #     # make document small caps only
    #     document = document.lower()
    #
    #     corpus = create_paragraphs_list(document)
    #
    #     vocabulary = get_vocabulary(corpus)
    #
    #     complete_vocabulary = {k: complete_vocabulary.get(k, 0) + vocabulary.get(k, 0) for k in set(complete_vocabulary) | set(vocabulary)}
    #
    #     start_idx = end_idx
    #
    #     if end_idx == 10 * (len(preprocessed_dirs) // 10) and len(preprocessed_dirs) > 10 * (len(preprocessed_dirs)//10):
    #         end_idx = end_idx + len(preprocessed_dirs) % 10 - 1
    #     else:
    #         end_idx += 10
    #
    # # Sort the complete vocabulary
    # complete_vocabulary = {k : v for k, v in sorted(complete_vocabulary.items(), key=lambda item: item[1])}
    #
    #
    # # Only keep keywords which appear at least 100 times
    # # Get the keywords
    # vocabulary = {k:v for k,v in complete_vocabulary.items() if v >= 100}
    #
    # with open('vocabulary.txt', 'w') as f:
    #     for k, v in vocabulary.items():
    #         f.writelines(k + ', ' + str(v) + '\n')
    #
    #
    # complete_keywords = {}
    # # Get keywords
    # start_idx = 0
    # end_idx = 10
    #
    # while end_idx < len(preprocessed_dirs):
    #     # create one large string with current window's story txt's
    #     document = []
    #
    #     # process per 10 stories
    #     # loop over directory to create a paragraph list for all of them
    #     for file in preprocessed_dirs[start_idx:end_idx]:
    #         with open(file, 'r', encoding='utf-8') as f:
    #             story = f.read()
    #             document.append(story)
    #
    #     # join the corpus with two newline characters
    #     document = '\n\n'.join(document)
    #     document = document.replace('_', ' ')
    #     # make document small caps only
    #     document = document.lower()
    #
    #     corpus = create_paragraphs_list(document)
    #
    #     # We pass only our vocabulary keys, i.e. the actual words of our vocabulary
    #     keywords = get_keywords_from_document(corpus, vocabulary.keys())
    #
    #     complete_keywords = {k: vocabulary.get(k, 0) for k in
    #                            set(complete_keywords) | set(keywords)}
    #
    #     start_idx = end_idx
    #
    #     if end_idx == 10 * (len(preprocessed_dirs) // 10) and len(preprocessed_dirs) > 10 * (
    #             len(preprocessed_dirs) // 10):
    #         end_idx = end_idx + len(preprocessed_dirs) % 10 - 1
    #     else:
    #         end_idx += 10
    #
    # with open('keywords.txt', 'w') as f:
    #     for k, v in complete_keywords.items():
    #         f.writelines(k + ', ' + str(v) + '\n')
    #
    #
    # full_corpus = ''
    # for file in preprocessed_dirs[start_idx:end_idx]:
    #     with open(file, 'r', encoding='utf-8') as f:
    #         story = f.read()
    #         full_corpus += ' \n\n\n' + story
    #
    # corpus_paragraphs = create_paragraphs_list(full_corpus)
    # index = {}
    # for paragraph in corpus:
    #     # Look for paragraphs that have the keyword, and append them to the list...
    #     for k, v in complete_keywords.items():
    #         if k in paragraph:
    #             if k in index.keys():
    #                 index[k].append(paragraph)
    #             else:
    #                 index[k] = [paragraph]
    #
    # for k, v in index.items():
    #     for value in v:
    #         print(k, value)
    #         print("***********8")
    #
    # with open('index.txt', 'w') as f:
    #     for k, v in index.items():
    #         for value in v:
    #             f.writelines(k + ', ' + str(value) + '\n')
    #
    #
    # with open('gutenberg_index.pkl', 'wb') as f:
    #     pickle.dump(index, f)
    # # nltk.download('stopwords')
    # # nltk.download('wordnet')
    # # nltk.download('punkt')

    index_reddit()