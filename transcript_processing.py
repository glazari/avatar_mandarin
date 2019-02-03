import pandas as pd
import time
import re
import os

import avatar_transcripts

def filter_character_speech(df):
    filtered_df = df[pd.notna(df['character'])]
    return filtered_df



def filter_pure_speech(df):
    df['speech']  = df['speech'].apply(get_pure_speech)
    return df

def get_pure_speech(speech):
    parts = re.split('[\[\]]',speech)
    speech_parts = parts[::2]
    pure = ''.join(speech_parts)
    pure = pure.strip()
    pure = pure.replace('  ', ' ')
    return pure

def add_chinese_translation(df):
    n=len(df)
    chinese_speeches = []
    for i, row in enumerate(df.itertuples()):
        print('%s/%s' % (i+1,n), end='\r')
        translation = avatar_transcripts.translate_text(row.speech)
        chinese_speeches.append(translation)
        time.sleep(0.1)
    df['chinese_speech'] = chinese_speeches
    return df

def files_from(folder):
    if os.path.isfile(folder):
        return [folder]
    files = []
    for f in os.listdir(folder):
        f_path = os.path.join(folder, f)
        if os.path.isdir(f_path):
            files.extend(files_from(f_path))
        else:
            files.append(f_path)
    return files

def translate_df(df):
    df = filter_character_speech(df)
    df = filter_pure_speech(df)
    df = add_chinese_translation(df)
    return df

input_folder = 'episode_transcripts'
translated_folder = 'episode_transcripts_processed/translated'
with_pinyin_folder = 'episode_transcripts_processed/with_pinyin'
top_words = 'episodes_transcripts_processed/top_words'

def part1_translate_dfs(input_folder, translated_folder):
    for file in files_from(input_folder):
        print(file)
        df = pd.read_csv(file)
        zh_df = translate_df(df)
        h, t = os.path.split(file)
        h, f = os.path.split(h)
        out_file = os.path.join(translated_folder, f, t)
        zh_df.to_csv(out_file, index=False)

