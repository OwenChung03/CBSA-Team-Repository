# Develop sectoral indices to study ESG sentiment and ESG hotness across 12 industries in Hong Kong
## Abstract:
This report, as a part of our holistic research, aims to provide real estate companies with descriptions and estimates of ESG public perception and expectations. This involves sentiment analysis and materiality analysis. In the process, we have developed sectoral indices for comparison across industries. Our findings allow real estate companies to set a better tone for their ESG efforts and understand how stakeholders may react to various ESG actions.

## Methodology:
### Process overview
Data Cleansing → Data Structuring → Data Modeling → Data Grouping → Data Analysis → Data Visualisation 

### 1. Data Cleansing
We use AC2022_set1.xlsx.
We remove rows with NaN element in either their content column or headline column as they are not useful for us to analyze texts. We also remove duplicated headlines to avoid weighted results. You may review clean_set1.ipynb for detailed code
https://colab.research.google.com/drive/1WU9oGpxcGqJWikGTn9OJ3OGTL1CRp4_A
A cleansed version of AC2022_set1.xlsx is exported with the filename set1(cleansed).csv. Download or review here.
Data Structuring
Later we will fit texts to FinBERT, a financial domain-specific pre-trained language model. The model used training samples of short sentences in english 1. Most headlines in set1(cleansed).csv are in chinese. We translate all the headlines in set1(cleansed).csv to english and remove headlines longer than 400 characters. headline_en.xlsx stored all the translation results. You may review combine.ipynb for detailed code on concating headline_en col and removing headlines longer than 400 characters https://colab.research.google.com/drive/1dCumBWWNbojw2iKFdfWQO8YNw-y5ZS7u 
A translated version of set1(cleansed).csv is exported with the filename set1(cleansed+translated).csv. Download or review here.
Data Modeling
By far, we transformed AC2022_set1.xlsx to set1(cleansed+translated).csv which can be understanded as the cleansed and structured version of AC2022_set1.xlsx. In the process, we also removed columns that we certainly will not use in this model (i.e. engagements, non_view_engagements, author_name, pub_name, pub_code, region, url, fans_count) bringing size of the table from 351442 rows × 24 columns down to 195435 rows × 17 columns. Now, we fit all 195435 english headlines in the headline_en column to finbert-esg-9-categories and finbert-tone. For finbert-esg-9-categories, each headline is classified as one of the 9 categories (i.e. Climate Change, Natural Capital, Pollution and Waste, Human Capital, Product Liability, Community Relations, Corporate Governance,  Business Ethics & Values and Non-ESG) along with a score. As for finbert-tone, each headline is classified as one of the 3 categories (i.e. Positive, Negative and Neutral) along with a score. You may review finbert9_update.ipynb for detailed code on running the models
https://colab.research.google.com/drive/14QKInQNNcSeAYhxeYlZ7LhY08ZKawt43#scrollTo=bh7rVQ5ssK6s
The result is exported to cat9.xlsx.
A concatenated version of set1(cleansed+translated).csv and cat9.xlsx is exported with the filename set1(cleansed+translated+labeled).csv. Download or review here. The size of the table is 195435 rows × 23 columns.
Data Grouping
We are based on the Hang Seng Industry Classification System 2 to define 12 groups (or call it sectors/industries). They are Energy🔋, Materials💎, Industrials🏭, Consumer Discretionary🎮, Consumer Staples🌽, Healthcare🩺, Telecommunications☎️, Utilities⛴, Financials💰, Properties & Construction🏗, Information Technology📲 and Conglomerates🏢. We then filter relevant content to the group based on the occurrence of certain keywords in the headline. The keywords are stored in the 6th sheet of HSIClass.xlsx (‘concat_list’). In each column, we stored the keywords used to identify the corresponding industry of the column heading. 
The column headings as you may notice are the 12 industries we just mentioned with some slight changes. Notice they have no space, no '_', no capital letters and they end with 's'.
Energy🔋 - energies
Materials💎 - materials
Industrials🏭 - industrials
Consumer Discretionary🎮 - nonconsumers
Consumer Staples🌽 - consumers
Healthcare🩺 - healths
Telecommunications☎️ - telecommuniations
Utilities⛴, - utilities
Financials💰 - finances
Properties & Construction🏗 - properties
Information Technology📲 - infotechnologies
Conglomerates🏢 - conglomerates
You may review industry_content.ipynb for the detailed code on filtering for relevant headlines to each industry
https://colab.research.google.com/drive/1M0k0Pq_r9WIQ1RVQOUf4Ze25KoEFyPwV#scrollTo=0m07Tj_osFai
Note that search_keyword() is a function in our custom defined module filter. Check the usage of this function on filter.ipynb
https://colab.research.google.com/drive/1-TsprhC1n9G8kMlLvXizKI8moGhf1glX
An excel workbook containing 12 sheets is exported with the filename industry_content.xlsx. Each sheet is named by the column headings, which stores related headlines together with content, pubdate, esg_9_categories, etc. Download or review here. Open it and you will see the following.

After going through all the data processing steps (from step 1 to 4), we finally obtain industry_content.xlsx which we are going to analyze on. Before doing so, we intend to explain the keywords we used. We attempt to develop indices that represent each industry in Hong Kong but not each industry in general. This brings us to half of the keywords are the company's name and stock code of HSI constituents. 

Another half is based on selection criterias:
Neutral words
Representativeness (One way to test this is to actually google it to see if relevant news pop up)
Overlapping (For example: 「電」 always occurs in the content of the industry of utilities (「發電站」,「電力」,「供電」). We can simply use 「電」 to search all those words in the parentheses. However, we know that other words like: 「電話」,「電池」,「電視」,「電單車」 will also be searched out but not related to the target industry. We avoid this kind of overlapping.)

Remarks: We assume a headline consists of any word in the column, then the content is relevant to that industry. But it may not be the case. For example: a sentence 「零售人力資源出現需求」 consists of the word 「資源」 in energies column, then this sentence is regarded as Energy related even for us it is more about the Consumer Discretionary or Consumer Staples. Note that this sentence also consists of the word 「零售」in nonconsumers column. In such a case, this sentence is regarded as both Energy and Consumer Discretionary, form the overlapping situation I mentioned above.
Not all headlines are used. Headlines that are not grouped to any industry simply because they don’t consist of any word in the concat_list.
Data Analysis
Encode ‘Positive’, ‘Negative’ and ‘Neutral’ as 1,-1 and 0 respectively. Create a new column sentimen_code to store the results. 
Define esg related as a boolean representing TRUE(1) or FALSE(0) of the condition: esg_9_categories is not ‘Non-ESG’ and esg_9_categories_score  c, where c[0,1]
Define confirmation as a boolean representing TRUE(1) or FALSE(0) of the condition: sentiment_score  d, where d[0,1]
ESG sentiment = i=0mesg relatedi*sentimen_codei*confirmationii=0mesg relatedi*confirmationi, where m is the max row index
Example:
Set c=d=0.85
i
esg_9_categories
esg_9_categories_score
sentiment_code
sentiment_score
0
Non-ESG
0.3
1
0.92
1
Climate Change
0.83
-1
0.89
2
Climate Change
0.87
-1
0.99
3
Product Liability
1
0
0.85

m=3
ESG sentiment=( 0*1*1+0*-1*1+1*-1*1+1*0*1)/(0*1+0*1+1*1+1*1)=-½=-0.5
ESG sentiment is scaled from -1 to 1. The more positive it is, the more optimistic the public is about the sector’s ESG outlook. 
Define non esg as a boolean representing TRUE(1) or FALSE(0) of the condition: esg_9_categories is ‘Non-ESG’ and esg_9_categories_score  e, where e[0,1]
ESG hotness = i=0mesg relatedii=0mnon esgi, where m is the max row index
Set e=0
ESG hotness=(0+0+1+1)/(1+0+0+0)=2
ESG hotness is scale from 0 to +. The larger the number, the more dominant is ESG conversation compared to Non-ESG conversation.
Data Visualization
Set c=d=0.85
