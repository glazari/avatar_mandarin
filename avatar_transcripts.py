import requests
import time
from xpinyin import Pinyin
import pandas as pd
import re


def get_episode_transcript(episode_name, df_index=1):
    url =  'http://avatar.wikia.com/wiki/Transcript:%s'
    url = url % episode_name

    resp = requests.get(url)
    
    html = resp.content
    dfs = pd.read_html(html)
    df = dfs[df_index]
    df.columns = ['character','speech']
    return df


class WordCounter():
    def __init__(self):
        self.frequency = {}

    def update_word(self, word):
        word = word.lower()
        cur_count = self.frequency.pop(word, 0)
        self.frequency[word] = cur_count + 1

    def update_string(self, string):
        words = string.split()
        for word in words:
            self.update_word(word)



def get_top_words(words):
    counter = WordCounter()
    
    def filter_chars(word):
        remove_chars = ['。',' ','，','！','？','.']
        for char in remove_chars:
            word = word.replace(char,'')
        return word

    words = [filter_chars(w) for w in words] 
    words = [w for w in words if w != '']
    for word in words:
        counter.update_word(word)
    
    top_words = sorted(counter.frequency.items(), key=lambda x: x[1], reverse=True)
    return top_words


def make_word_df(top_words):
    words = []
    for word, count in top_words:
        pinyin = get_pin_yin(word)
        en = translate(word)
        item = (word, pinyin, en, count)
        words.append(item)
        print(*item)
        time.sleep(0.5)
    word_df = pd.DataFrame(words, columns=['word','pinyin','english','word_count'])
    return word_df

# segment chinese text 
################################################################################

import jieba

sentence = "我想说更好的中文，但很难，因为我是波兰人"
def segment_chinese_text(sentence):
    segments = jieba.cut(sentence)
    return list(segments)
    

def space_words(sentence):
    segments = segment_chinese_text(sentence)
    spaced_text = ' '.join(segments)
    return spaced_text

# get pinin from chinese text
################################################################################
def get_pin_yin(text):
    p = Pinyin()
    pinyined = p.get_pinyin(text, splitter='', tone_marks='marks')
    return pinyined

# translate from english to chinese
################################################################################
from mtranslate import translate

def translate_text(text):
    chinese_text = translate(text, 'zh')
    return chinese_text


# increment df with chinese


def get_pure_speech(speech):
    parts = re.split('[\[\]]',speech)
    speech_parts = parts[::2]
    pure = ''.join(speech_parts)
    return pure
