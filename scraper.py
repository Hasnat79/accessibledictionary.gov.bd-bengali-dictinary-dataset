from bs4 import BeautifulSoup as bs
import requests
import json
from tqdm import tqdm
import re

site="https://accessibledictionary.gov.bd/bengali-to-english/?alp=%E0%A6%85"
r=requests.get(site)

#convert to a beautiful soup object

soup = bs(r.content)

#print out the HTML

contents = soup.prettify()

# print(contents)

alphabet_links=[]
alphabet_box =soup.find(class_="alphabet")
alphs=alphabet_box.find_all('a')
for index,row in enumerate(alphs):
    link=row.get('href')
#     print(link)
    alphabet_links.append(link)

# alphabet_links


''' alph_and_page_numbers_info dictionary 
    key= link of each alphabet
    value= number of pages available for that alphabet(int)
'''
#---------------------------------------
# alph_and_page_numbers_info = {}
#
# # pagitation_box=soup.find(class_="pagination")
# # page_numbers=pagitation_box.find_all('li')
# # page_numbers[-2].get_text()
# for index, link in enumerate(alphabet_links):
#     r = requests.get(link)
#     soup = bs(r.content)
#
#     if soup.find(class_="pagination"):
#
#         pagitation_box = soup.find(class_="pagination")
#         page_numbers = pagitation_box.find_all('li')
#
#         no_of_pages = int(page_numbers[-2].get_text())
#     else:
#         no_of_pages = 1
#     alph_and_page_numbers_info[link] = no_of_pages
#
#     print(f"Case no: {index}: done")

# alph_and_page_numbers_info

#--------------------------------------------------------

alph = alphabet_links[0][-1]
# print(alph)
page = 1

site = f"https://accessibledictionary.gov.bd/bengali-to-english/?alp={alph}&page={page}"

dictionary_info = {}

r = requests.get(site)
soup = bs(r.content)

# print(soup.title.get_text()

article_box = soup.find(class_="dicDisplay")
word_list = article_box.find("ul")
words = word_list.find_all("li")
for w in words:
    # print(w.text, end="\n\n\n")
    w.contents.pop(0)
    w.contents.pop(2)
    # print(w.text,end="\n\n\n")
    dictionary_info[w.text.split("English definition")[0]]=w.text.split("English definition")[1]

print(dictionary_info)

def save_data(title,data):
    with open(title,'w', encoding = 'utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

save_data("accessible_dictionary_data_.json",dictionary_info)




