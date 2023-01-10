"""Description: This file contains functions to filter pandas dataframes"""

# Import libraries
import pandas as pd


# Helper functions
def format_date(df, format):
    """Format pubdate column of dataframe

    Args:
        df (dataframe): dataframe to be filtered
        format (string): date format

    Returns:
        dataframe: filtered dataframe
    """
    # Convert pubdate string into a datetime object
    df['pubdate'] = pd.to_datetime(df.pubdate, format='%Y-%m-%d %H:%M:%S')
    # Make a copy of the dataframe
    format_date_df = df.copy()
    # Make the pubdate column conform to the format string
    format_date_df['pubdate'] = format_date_df['pubdate'].dt.strftime(format)

    return format_date_df

# example code
# format_date(df, '%Y-%m-%d')


def search_date(df, pubdate):
    """Filter dataframe by date

    Args:
        df (dataframe): dataframe to be filtered
        pubdate (string): date to filter by

    Returns:
        dataframe: filtered dataframe
    """
    # Convert pubdate column to datetime format
    df['pubdate'] = pd.to_datetime(df.pubdate, format='%Y-%m-%d %H:%M:%S')
    # Filter dataframe by pubdate
    search_date_df = df[df['pubdate'].dt.strftime('%Y-%m-%d') == pubdate]

    return search_date_df

# example code
# search_date(df, '2022-03-15')


def search_keyword(df, col, keywords):
    """Filter dataframe by keyword

    Args:
        df (dataframe): dataframe to be filtered
        col (string): column to filter by
        keywords (list): keywords to filter by

    Returns:
        dataframe: filtered dataframe
    """
    # Convert keywords list to string
    keywords_str = '|'.join(keywords)
    # Filter dataframe by keywords
    search_keyword_df = df[df[col].str.contains(keywords_str, na=False)]

    return search_keyword_df

# example code
# search_keyword(df, 'content', ['apple', 'banana'])
