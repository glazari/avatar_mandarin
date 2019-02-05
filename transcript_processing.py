import pandas as pd
import time
import re
import os

import avatar_transcripts

input_folder = 'episode_transcripts'
translated_folder = 'episode_transcripts_processed/translated'
with_pinyin_folder = 'episode_transcripts_processed/with_pinyin'
top_words = 'episodes_transcripts_processed/top_words'

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

def get_outfile(out_folder, file):
    h, t = os.path.split(file)
    h, f = os.path.split(h)
    out_file = os.path.join(out_folder, f, t)
    return out_file

def apply_transformation(in_folder, out_folder, transformation):
    for file in files_from(in_folder):
        out_file = get_outfile(out_folder, file)
        if os.path.exists(out_file):
            continue
        print(file)
        df = pd.read_csv(file)
        df = transformation(df)
        df.to_csv(out_file, index=False)
    
################################## part 1 #####################################

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

def translate_df(df):
    df = filter_character_speech(df)
    df = filter_pure_speech(df)
    df = add_chinese_translation(df)
    return df

def part1_translate_dfs(input_folder, translated_folder):
    apply_transformation(input_folder, translated_folder, translate_df)

################################## part 2 #####################################

def space_chinese_words(df):
    df['chinese_speech'] = df['chinese_speech'].apply(
            avatar_transcripts.space_words
            )
    return df


def add_pinyin(df):
    df['pinyin'] = df['chinese_speech'].apply(
            avatar_transcripts.get_pinyin
            )
    return df


def increment_chinese(df):
    df = space_chinese_words(df)
    df = add_pinyin(df)
    return df

def part2_increment_chinese_dfs(translated_folder, with_pinyin_folder):
    apply_transformation(
            translated_folder, 
            with_pinyin_folder,
            increment_chinese
    )


################################## part 3 #####################################
