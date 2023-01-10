"""This file contains functions to combine the dataset"""


# Import libraries
import pandas as pd
import numpy as np
import datetime

# Define functions

# Load the original dataset
filename1 = 'set1(cleansed).csv'
df = pd.read_csv(filename1)
df['pubdate'] = pd.to_datetime(df.pubdate, format='%Y-%m-%d %H:%M:%S')

# Load the translated dataset
filename2 = 'headline_en.xlsx'
df1 = pd.concat(pd.read_excel(filename2, sheet_name=None), ignore_index=True)

# get translated headline column and rename it as headline_en
df1 = df1[['headline']]
df1.rename(columns={'headline': 'headline_en'}, inplace=True)

# add headline_en column to df
df['headline_en'] = df1

# get rid of rows with headline_en longer than 400 characters
df = df.loc[df["headline_en"].str.len() < 400]

# reorder columns
df = df[['docid', 'comment_count', 'like_count', 'dislike_count', 'love_count', 'haha_count', 'wow_count', 'angry_count',
         'sad_count', 'share_count', 'view_count', 'emoji_count', 'headline', 'headline_en', 'pubtype', 'pubdate', 'content']]


# output to csv
path = 'set1(cleansed+translated).csv'
with open(path, 'w', encoding='utf-8-sig') as f:
    df.to_csv(f)
