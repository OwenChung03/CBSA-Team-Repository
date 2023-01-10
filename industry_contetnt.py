"""This file shows how the texts related to any one of the 12 pre-labeled industries is extracted from the dataset"""


# Import libraries
import pandas as pd
import numpy as np
from numpy import nan
import filter

# Load dataset
filename = 'set1(cleansed+translated+labeled).csv'
df = pd.read_csv(filename)
df['pubdate'] = pd.to_datetime(df.pubdate, format='%Y-%m-%d %H:%M:%S')
df.head()

# Load the 12 pre-labeled industries and their keywords
filename2 = 'HSIClass.xlsx'
df_concat = pd.read_excel(filename2, sheet_name=5)
df_concat

"""The column headings as you may notice are the 12 pre-labeled industries we just mentioned with some slight changes. Please notice they have no space, no '_', no capital letters and they end with 's'.
*   Energy🔋 - **energies**
*   Materials💎 - **materials**
*   Industrials🏭 - **industrials**
*   Consumer Discretionary🎮 - **nonconsumers**
*   Consumer Staples🌽 - **consumers**
*   Healthcare🩺 - **healths**
*   Telecommunications☎️ - **telecommuniations**
*   Utilities⛴, - **utilities**
*   Financials💰 - **finances**
*   Properties & Construction🏗 - **properties**
*   Information Technology📲 - **infotechnologies**
*   Conglomerates🏢 - **conglomerates**

In each column, we stored the keywords used to identify the corresponding industry. If you want to know how keywords come from, you may continue to read. First thing to know is texts filtered with those keywords will be stored in an excel workbook and then the texts inside the excel workbook will proceed some text classification and sentiment analysis. The results will further use to calculate industry-esg-hotness and industry-esg-sentiment indices. We want those indices to represent each industry in Hong Kong but not each industry in general. This brings us to **half of the keywords are company's name and stock code of HSI constituents**. For example: '0012.HK' also include 「恒基」, 「恒地」, 'HENDERSON LAND' belongs to properties column and is one of the HSI constituents. 

---

Go through the following spreadsheet 'constituents_list' for the whole company keyword list
--> https://docs.google.com/spreadsheets/d/1Xmm0sVDyIN5uiKVrqjbtDGMuJaBavAMn/edit#gid=922012296

Reference: https://www.hsi.com.hk/chi/indexes/all-indexes/hsi

---

---

Go through the following spreadsheet 'constituents_list' for the whole company keyword list
--> https://docs.google.com/spreadsheets/d/1Xmm0sVDyIN5uiKVrqjbtDGMuJaBavAMn/edit#gid=1009457428

Reference: https://www.hsi.com.hk/static/uploads/contents/zh_hk/dl_centre/brochures/B_HSICSc.pdf

---
Key selection criterias:
- Neutral words
- Representativeness (One way to test this is to actually google it to see if relevant news pops up)
- Overlapping (For example: 「電」 always occurs in the content of the industry of utilities (「發電站」,「電力」,「供電」). We can simply use 「電」 to search all those words in the parentheses. However, we know that other words like: 「電話」,「電池」,「電視」,「電單車」 will also be seaarched out but not related to the target industry. We avoid overlapping.)

Assumptions: We assumed a piece of text consists any of a word in a column, then the content is something about that industry. But it may not be the case. For example: a sentence 「零售人力資源出現需求」 consists of the word 「資源」 is considered as energies (i.e. energy) even for us it is more about the Consumer Discretionary and Consumer Staples.

Important notes:

Limitations: Unfortunately, we are not able to quantify the relevance of a word
"""

# Get the keyword list for each industry as a dictionary
industries12 = ['conglomerates', 'utilities', 'materials',	'properties',	'industrials',	'consumers', 
                'energies',	'infotechnologies',	'healths',	'finances',	'telecommunications',	'nonconsumers']
concat_dicts = {}
for industry in industries12:
    # arr is a variable for temporary use only
    arr = df_concat[industry].to_numpy() # DataFrame to numpy array
    arr = arr[np.logical_not(pd.isna(arr))] # remove nan
    concat_dicts[industry] = arr.tolist() # convert arr to list and store in a dictionary

# Export the extracted texts related to the 12 industries to an excel workbook
for col_head in industries12:
    search_keyword_df = filter.search_keyword(df, 'headline', concat_dicts[col_head])
    search_keyword_df = search_keyword_df[['docid','comment_count','like_count','dislike_count','love_count','haha_count','wow_count','angry_count',
                                         'sad_count','share_count','view_count','emoji_count','headline','headline_en','pubtype','pubdate','content',
                                         'esg_9_categories','esg_9_categories_score','sentiment_code','sentiment_score']]
    search_keyword_df.reset_index(inplace = True)
    with pd.ExcelWriter('industry_content.xlsx',mode='a') as writer:
        search_keyword_df.to_excel(writer, sheet_name=col_head)