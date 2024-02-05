import requests
from .models import Books

# @transaction.atomic
def create_books_from_api(api_response):
    for index, book_data in enumerate(api_response, start=1):
        # Extracting data from the API response
        name = book_data['name']
        abbreviation = book_data['abbreviation']
        book_id = book_data['id']
        location = 'NT' if index > 39 else 'OT'  # Assuming 39 is the number of books in the Old Testament
        order = index
        chapters = 0  # You can set the actual number of chapters if available in the API response

        # Creating a Book object
        book = Books.objects.create(
            name=name,
            abbreviation=abbreviation,
            book_id=book_id,
            location=location,
            order=order,
            chapters=chapters
        )

        print(f"Book '{book}' created successfully!")

def get_all_books():
    base_url = 'https://api.scripture.api.bible/v1/bibles'
    endpoint = f'{base_url}/de4e12af7f28f599-02/books'

    headers = {
        'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a',
    }

    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for bad requests

        # Assuming the API returns data in JSON format
        books_data = response.json()['data']

        # Extract books from the response
        books = books_data
        create_books_from_api(books)

        return books

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

print(get_all_books())