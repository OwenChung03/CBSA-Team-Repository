"""This file contains functions to update the finbert9 categories and finbert tone for the dataset"""


# Import libraries
# pip install transformers
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, pipeline # tested in transformers==4.18.0
import filter

# Load the dataset
filename = 'set1(cleansed+translated).csv'
df = pd.read_csv(filename)

# get the english headline column
mysamplelist = df["headline_en"].values.tolist()

# load the finbert sentiment
finbert_esg = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-esg-9-categories',num_labels=9)
tokenizer_esg = BertTokenizer.from_pretrained('yiyanghkust/finbert-esg-9-categories')
nlp_esg = pipeline("text-classification", model=finbert_esg, tokenizer=tokenizer_esg, device=0)
# get the finbert esg categories and score
esg = []
esg_score = []
for sample in mysamplelist:
    results = nlp_esg(sample)
    esg.append(results[0]['label'])
    esg_score.append(results[0]['score'])
# ensure the length of esg and esg_score are the same
assert len(esg) == len(esg_score)

# load the finbert tone
finbert_sentiment = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer_sentiment = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
nlp_sentiment = pipeline("sentiment-analysis", model=finbert_sentiment, tokenizer=tokenizer_sentiment, device=0)
# get the finbert sentiment and score
sentiment = []
sentiment_score = []
for sample in mysamplelist:
    results = nlp_sentiment(sample)
    sentiment.append(results[0]['label'])
    sentiment_score.append(results[0]['score'])
# ensure the length of sentiment and sentiment_score are the same
assert len(sentiment) == len(sentiment_score)

# save the finbert categories and finbert tone to a dataframe
cat_9 = pd.DataFrame(list(zip(esg, esg_score, sentiment, sentiment_score)), columns=['esg_9_categories','esg_9_categories_score','sentiment','sentiment_score'])

# export the dataframe to a csv file
path = '/content/drive/My Drive/AC/cat_9.csv'
with open(path, 'w', encoding = 'utf-8-sig') as f:
    cat_9.to_csv(f)
    