from typing import Dict, List, Tuple
import requests
from requests.exceptions import HTTPError
import json
import string
import re
from bs4 import BeautifulSoup as bs


def check_url_schema(url: str) -> str:
    """
    checks to see if schema applied in url
    args:
        url: str - url of page to collect data from
    returns:
        url: str - formatted url
    """
    if not re.search('(http:\/\/)|(https:\/\/)', url):
        url = f"https://{url}"
    
    return url

def format_url(url: str) -> str:
    """
    format url: 
        remove trailing and leading whitespace
        make lowercase
        assign schema to url
    
    args:
        input: (str) - input url
    
    return:
        formatted_url (str)
    """
    formatted_url = check_url_schema(str(url).strip().lower())
    return formatted_url

def check_req_status(url: str, headers: Dict[str, str] = None) -> Tuple[bool, str]:
    """
    args:
        url: str - url of page to collect data from
        headers: dict[str, str], default None - chrome headers to avoid 403 forbidden. 
    returns:
        bool
    """
    try:
        url = format_url(url)
        response = requests.get(url, timeout=5, headers=headers)
            # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        return (False, f'HTTP error occurred: {http_err}')
    except Exception as err:
        return (False, f'Other error occurred: {err}')
    else:
        return (True, response.text)

def collect_url_text(url: str, headers: Dict[str, str] = None) -> Tuple[bool, List[str]]:
    """
    collects text from all html tags within body tag

    args:
        url: str - url of page to collect data from
        headers: dict[str, str], default None - chrome headers to avoid 403 forbidden. 
    returns:
        text_list: list[str] - text from html tags in list format or Error Message
    """
    if not headers:
        #Have to provide full path so it can run in docker container
        with open('config/variables.json','r') as f:
        # with open('config/variables.json','r') as f:
            headers = json.load(f)    
    status, resp = check_req_status(url, headers=headers)
    if status:
        soup = bs(resp, 'html.parser')
        #Avoid collecting text from JavaScript or Styling
        for s in soup(['script','style']):
            s.extract()
        text_list = soup.body.find_all(text=True)
        return (status, text_list)
    return  (status, [resp])

def normalize(value: str) -> str:
    """
    preprocess raw string: 
        remove trailing and leading whitespace
        make lowercase
        remove trailing punctuation
    
    args:
        value: (str) - value string
    
    return:
        formatted_string (str)
    """
    formatted_string = ''.join([c for c in value if not c.isdigit()])
    formatted_string = formatted_string.strip().lower().strip(string.punctuation)
    return formatted_string

def split_words(value: str) -> List[str]:
    """
    splits test string on whitespace into individual words
    
    args:
        value: (str) - value string
    
    return:
        word_list: (list[str])
    
    """
    
    word_list = value.split()
    return word_list

def sort_words_desc(word_dict: Dict) -> list[Tuple[str, int]]:
    """
    returns list of tuples (word, count) sorted in descending order from dict
    of dictionary of key (word) : value (count)
    """
    return sorted([(k,v) for k, v in word_dict.items()], key=lambda x: x[1], reverse=True)

def word_count_dict(url, headers=None):
    status, text_list = collect_url_text(url, headers=headers)
    if status:
        corpus = {}
        for elm in text_list:
            for w in split_words(elm):
                norm = normalize(w)
                if norm != '' and corpus.get(norm):
                    corpus[norm] += 1
                elif norm != '':
                    corpus[norm] = 1
        sorted_corpus = sort_words_desc(corpus)
        return (status, sorted_corpus)
    return (status, text_list)

