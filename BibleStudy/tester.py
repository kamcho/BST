import requests
def get_verses(bible_id, book, chapter):
    base_url = 'https://api.scripture.api.bible/v1/bibles'
    endpoint = f'{base_url}/{bible_id}/chapters/{book}.{chapter}'

    headers = {
        'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a',
    }
    print(bible_id, book, chapter)
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()


        # Assuming the API returns data in JSON format
        books_data = response.json()
        
        # print(books_data['data']['content'])
        
        return books_data['data']['content']

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# get_verses()