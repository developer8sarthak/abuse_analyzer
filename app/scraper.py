import requests
from bs4 import BeautifulSoup

class ContentScraper:
    def get_text_from_url(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Abuse-Validator-Bot/1.0)'}
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            text = soup.get_text(separator=' ')
            clean_text = ' '.join(text.split())
            return clean_text
        except Exception as e:
            raise Exception(f"Scraper Error: {str(e)}")