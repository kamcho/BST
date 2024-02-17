import requests
def post_books():
    base_url = 'https://api.scripture.api.bible/v1/bibles'
    endpoint = f'{base_url}/06125adad2d5898a-01/books'

    headers = {
        'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a',
    }
    # print(bible_id, book, chapter)
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
        counter = 1
        for book in data['data']:
            # bid = Books.objects.create(name=book['name'], abbreviation=book['abbreviation'],
            #                             book_id=book['id'], chapters=0, order=counter, location='OT')
            counter = counter+1

        return None
    except:
        pass