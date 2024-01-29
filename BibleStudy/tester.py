
# Create your tests here.
import requests
# Create your views here.

uskey = '356aa3138554b86a1245ff03d2ebd78f'


BASE_URL = 'https://api.bible/v1/bibles'
BIBLE_VERSION_ID = '65eec8e0b60e656b-01'


def get_books_in_bible(bible_version_id):
    """Fetches books from api.bible for a given Bible version ID.

    Args:
        bible_version_id (str): The ID of the Bible version to retrieve books from.

    Returns:
        dict: The JSON response containing book data, or None if an error occurred.
    """

    url = f'https://api.scripture.api.bible/v1/bibles/65eec8e0b60e656b-01/books/MAT'
    headers = {'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a'}  # Replace with your actual API key

    try:
        response = requests.get(url, headers=headers, timeout=30)  # Increase timeout to 15 seconds
        print(response.status_code)  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        # books = data.get('data', [])  # Extract book data from the response

        return data

    except requests.RequestException as e:
        print(f"Failed to fetch books. Error: {e}")
        return None

# Example usage:
bible_version_id = 'de4e12af7f28f599-02'  # Replace with the desired Bible version ID
books = get_books_in_bible(bible_version_id)

print(books)
