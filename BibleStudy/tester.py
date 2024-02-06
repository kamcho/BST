import requests
from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
def get_verses():
    base_url = 'https://api.scripture.api.bible/v1/bibles'
    endpoint = f'{base_url}/de4e12af7f28f599-02/books/GEN/chapters'

    headers = {
        'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a',
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()

        # Assuming the API returns data in JSON format
        books_data = response.json()
        print(books_data)
        

        return books_data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

get_verses()