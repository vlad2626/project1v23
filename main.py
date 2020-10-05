import json
import requests
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from pprint import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd

nltk.download("punkt")
nltk.download("stopwords")


api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")

api_key = api_key_dict["my_key"]
my_articles = " "

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Well come to New york times Articles\n Project 1 6159250")

option = st.selectbox(
    "what section would you like to look into",
    ["arts", "automobiles", "books", "business", "fashion", "food", "health", " home", "insider", "magazine", "movies", "nyregion"
     "obituaries", "opinion", "politics", "realestate" , "science", "sports","sundayreview", "technology", "theater", "t-magazine","travel" , "upshot", "us", "world"]
)
st.write("You have selected " + option)
str = option

l= len(str)

sub = str[0:l]


url = "https://api.nytimes.com/svc/topstories/v2/"+sub+".json?api-key=" + api_key

response = requests.get(url).json()

main_functions.save_to_file(response, "JSON_Files/response.json")





my_articles = main_functions.read_from_file("JSON_Files/response.json")



str1 = " "

for i in my_articles["results"]:
    str1 = str1 + i["abstract"]

words = word_tokenize(str1)
word_no_punc = []

for j in words:
    if j.isalpha():
        word_no_punc.append(j.lower())

stopwords = stopwords.words("english")
clean_words = []

for k in word_no_punc:
    if k not in stopwords:
        clean_words.append(k)


fdist = FreqDist(clean_words)

str3 = fdist.most_common(10)
#st.write(" the most common 10 words used")


# chart_data = pd.DataFrame(
#     str3
# )

chart_data = pd.DataFrame(
     str3,

 )




if st.checkbox("click here for the most frequent words"):
            st.line_chart(chart_data)
#st.line_chart(chart_data)




wordcloud= WordCloud().generate(str1)

plt.figure(figsize=(12,12))
plt.imshow(wordcloud)
plt.axis("off")
if st.checkbox("click here to generate word cloud"):
    st.pyplot(figsize=(12,12))


my_articles2= " "
st.title(" PART B - MOST POPULAR ARTICLES")
option2 =st.selectbox("what is you preffered set of articles",
                      ["shared", "emailed", "viewed"])
option3 = st.selectbox("how long you want to collect data for(days)",
                       ["1", "7", "30"])

url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + option2 +"/" + option3+ ".json?api-key=" + api_key



response2 = requests.get(url2).json()

main_functions.save_to_file(response2, "JSON_Files/response2.json")

my_articles2 = main_functions.read_from_file("JSON_Files/response2.json")

pop = " "
for m in my_articles2["results"]:
    pop = pop + m["abstract"]

words2 = word_tokenize(pop)
clean_words2 = []
word_no_punc2= []

for p in words2:
    if p.isalpha():
        word_no_punc2.append(p.lower())

for z in word_no_punc2:
    if z not in stopwords:
        clean_words2.append(z)

fdist2 =FreqDist(word_no_punc2)

mostCom = fdist2.most_common(10)
#pprint(mostCom)
wordcloud2 = WordCloud().generate(pop)

plt.imshow(wordcloud2)
plt.axis("off")


if st.checkbox("click here for wordloud"):
    st.pyplot(figsize=(12, 12))
