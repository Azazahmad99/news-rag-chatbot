import requests
from bs4 import BeautifulSoup
import time
import streamlit as st
from datetime import date
today = date.today()
formatted_date = today.strftime("%Y-%m-%d")

@st.cache_resource
def get_news_link(news_channel):
    if news_channel == "Times Of India" :
        return "https://timesofindia.indiatimes.com/" 
    elif news_channel == "India Today" :
        return  "https://www.indiatoday.in/"
    elif news_channel == "Hindustan News" :
        return  "https://www.hindustantimes.com/"
    elif news_channel == "Moneycontrol (Stock Market)" :
        return "https://www.moneycontrol.com/news/business/stocks/"
    elif news_channel == "Economic Times (Stock Market)" :
        return "https://economictimes.indiatimes.com/markets/stocks"
    else :
        return  "https://www.ndtv.com/"

#### extract links
@st.cache_resource
def extract_all_links(target_url) :  
    '''
    This Functions will extract all the news links present in target_url
    '''
    all_articale_links = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
        response = requests.get(target_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            if '/articleshow/' in href or '/news/' in href or '/briefs/' in href:
                full_url = ""
                if href.startswith('/'):
                    full_url = target_url + href
                elif href.startswith('http'):
                    full_url = href

                if full_url and full_url not in all_articale_links:
                    all_articale_links.append(full_url)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the main page: {e}")
    except Exception as e:
        print(f"An error occurred while extracting links: {e}")
    return all_articale_links


@st.cache_resource
### extract text from links
def extract_text_from_url(url):
    """
    Extracts all text content from a given URL.

    Args:
        url (str): The URL of the webpage to extract text from.

    Returns:
        str: All the text content from the webpage, or None if an error occurs.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get all text content, removing script and style tags
        text_parts = soup.stripped_strings
        full_text = "\n".join(text_parts)
        return full_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return None


@st.cache_resource
def save_text_to_file(text, filename):    
    """
    Saves the given text content to a text file.

    Args:
        text (str): The text content to save.
        filename (str, optional): The name of the file to save to.
                                   Defaults to "extracted_text.txt".
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")
    

@st.cache_resource
def news_collection_from_url(news_article_links) :
    "This function will collect all the news from url's"
    if news_article_links :
        extracted_text = ''
        for i,link in enumerate(news_article_links) :
            print(f"Extracting text from: ({i+1}/{len(news_article_links)}) Link - {link}")
            text = extract_text_from_url(link)
            if text:
                extracted_text += f"\n\n--- Text from {link} ---\n\n{text}"
                time.sleep(1)
        return extracted_text
    
    else :
        print("No news article links were found to extract text from.")
