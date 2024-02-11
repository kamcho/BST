import requests
def get_verses(bible_id, book, chapter):
    base_url = 'https://api.scripture.api.bible/v1/bibles'
    endpoint = f'{base_url}/06125adad2d5898a-01/chapters/{book}.{chapter}'

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
        
        return str(e)



def get__post_books():
    base_url = 'https://api.scripture.api.bible/v1/bibles'
    
    books = Books.objects.all().order_by('order')
    for book in books:
        endpoint = f'{base_url}/06125adad2d5898a-01/books/{ book.book_id }/chapters'

        headers = {
            'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a',
        }
    
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            response = response.json()
            chapters = response['data']
            
            for chapter in chapters:
                try:
                    number = int(chapter['number'])
                    obj = Chapters.objects.create(book=book, order=number)

                except:
                    pass
                
            
        except Exception as e:
            print(str(e))

# get__post_books()