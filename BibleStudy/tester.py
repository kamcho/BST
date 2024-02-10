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



def get__post_books(bible_id):
    base_url = 'https://api.scripture.api.bible/v1/bibles'
    endpoint = f'{base_url}/06125adad2d5898a-01/books'

    headers = {
        'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a',
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        response = response.json()
        books = response['data']
        count = 1
        # for book in books:
        #     Books.objects.create(name=book['name'],order=count book_id=book['id'], abbreviation=book['abbreviation'],location='OT', chapters=0)
            
        #     count+=1
           
    except Exception as e:
        print(str(e))

# get_books()