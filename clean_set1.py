"""This file contains functions to cleanse the dataset"""

# Import libraries
import pandas as pd


def load_dataset(filename):
    """Loads the dataset

    Args:
        filename (string): name of the dataset file

    Returns:
        dataframe: dataset
    """
    # Load the dataset
    df = pd.read_excel(filename)
    # Convert dates to datetime format
    df['pubdate'] = pd.to_datetime(df.pubdate, format='%Y-%m-%d %H:%M:%S')

    return df


def cleanse_dataset(df):
    """Cleanses the dataset

    Args:
        df (dataframe): dataframe to be cleansed

    Returns:
        dataframe: cleansed dataframe
    """
    # drop rows with NaN Values in content column
    df = df.dropna(axis=0, subset=['content'])
    # drop rows with NaN Values in headline column
    df = df.dropna(axis=0, subset=['headline'])
    # drop rows with duplicated Values in both headline and content columns
    df = df.drop_duplicates(subset=['content', 'headline'])

    return df


def save_cleaned_dataset(df, filename):
    """Saves the cleansed dataset

    Args:
        df (dataframe): dataframe to be saved
        filename (string): name of the file to be saved
    """
    # Save cleansed data
    path = filename
    with open(path, 'w', encoding='utf-8-sig') as f:
        df.to_csv(f)


# example code
# df = load_dataset('data/AC2022_set1.xlsx')
# df = cleanse_dataset(df)
# save_cleaned_dataset(df, 'data/set1(cleansed).csv')
