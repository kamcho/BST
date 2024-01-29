import requests
from bs4 import BeautifulSoup
def get_matthew_3():
    api_key = '1cfeb0d5fb47d89b7bb6cef9e8427f6a'  # Replace 'YOUR_API_KEY' with your actual API key from bibleapi.co
    base_url = f'https://api.scripture.api.bible/v1/bibles/65eec8e0b60e656b-01/chapters/MAT.10'

    headers = {'api-key': '0427945137760de29cd975e25a5b6e36'}

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()
      
        

        text_content = data['data']['content']
        print(text_content)
        
        
        soup = BeautifulSoup(text_content, 'html.parser')

        # Extracting text content from the <p> elements
        verse_texts = [p.get_text() for p in soup.find_all('p', class_='p')]

        # Joining the verse texts into a single string
        all_verses_as_string = "\n".join(verse_texts)
        # print(all_verses_as_string)
        return text_content

    except requests.exceptions.RequestException as err:

        print(f"Error fetching Bible verse: {err}")
        return 10, 'NOT AVAILABLE. RELOAD'

get_matthew_3()