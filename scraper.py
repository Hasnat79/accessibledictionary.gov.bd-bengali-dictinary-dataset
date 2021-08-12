

from bs4 import BeautifulSoup as bs
import requests
import json
from tqdm import tqdm
import re

def save_data(title,data):
    with open(title,'w', encoding = 'utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)


def generate_alphabet_links_and_page_info(site):
    '''
    Returns the alphabet page links and available pages

    :param site(str): bengali to english home page link
    :return alphabet_links_and_page_numbers(dictionary): key-> alphabet, value-> number of pages
    '''
    print("generate_alphabet_links_and_page_info(site) running...")
    alphabet_links_and_page_numbers={}

    r = requests.get(site)

    # convert to a beautiful soup object
    soup = bs(r.content,features="html.parser")


    alphabet_box = soup.find(class_="alphabet")
    alphs = alphabet_box.find_all('a')
    for index, row in enumerate(alphs):
        link = row.get('href')
        r = requests.get(link)
        soup = bs(r.content,features="html.parser")

        if soup.find(class_="pagination"):

            pagitation_box = soup.find(class_="pagination")
            page_numbers = pagitation_box.find_all('li')

            no_of_pages = int(page_numbers[-2].get_text())
        else:
            no_of_pages = 1
        print(f" linked and pages parsed for alphabet: {link[-1]}")
        alphabet_links_and_page_numbers[link] = no_of_pages

    return alphabet_links_and_page_numbers


def parser(alphabet_links_and_page_numbers):
    '''
    Returns the dataset of words and meanings

    :param alphabet_links_and_page_numbers (dictionary): key-> alphabet, value-> number of pages
    :return dictionary_info(dictionary): key-> word, value-> meaning_text_chunk
    '''

    dictionary_info = {}

    for link,pages in alphabet_links_and_page_numbers.items():
        print(f"parsing words and meanings for alphabet: {link[-1]}")
        alph=link[-1]
        for page in range(1,pages+1):
            site = f"https://accessibledictionary.gov.bd/bengali-to-english/?alp={alph}&page={page}"
            r = requests.get(site)
            soup = bs(r.content,features="html.parser")

            article_box = soup.find(class_="dicDisplay")
            word_list = article_box.find("ul")
            words = word_list.find_all("li")
            for w in words:
                # print(w.text, end="\n\n\n")
                w.contents.pop(0)
                w.contents.pop(2)
                # print(w.text,end="\n\n\n")
                dictionary_info[w.text.split("English definition")[0]]=w.text.split("English definition")[1]

    return dictionary_info







bengali_to_english_dictionary_site = "https://accessibledictionary.gov.bd/bengali-to-english/"

alphabet_links_and_page_numbers = generate_alphabet_links_and_page_info(bengali_to_english_dictionary_site)

dictionary_info = parser(alphabet_links_and_page_numbers)

save_data("accessible_dictionary_initial_dataset.json",dictionary_info)

# print(alphabet_links_and_page_numbers)













