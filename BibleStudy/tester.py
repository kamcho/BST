import requests

from BibleStudy.models import BibleVersesKJV
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
        
        
        raise AttributeError
bible_books = [
    {'name': 'Genesis', 'chapters': 50, 'order': 1},
    {'name': 'Exodus', 'chapters': 40, 'order': 2},
    {'name': 'Leviticus', 'chapters': 27, 'order': 3},
    {'name': 'Numbers', 'chapters': 36, 'order': 4},
    {'name': 'Deuteronomy', 'chapters': 34, 'order': 5},
    {'name': 'Joshua', 'chapters': 24, 'order': 6},
    {'name': 'Judges', 'chapters': 21, 'order': 7},
    {'name': 'Ruth', 'chapters': 4, 'order': 8},
    {'name': '1 Samuel', 'chapters': 31, 'order': 9},
    {'name': '2 Samuel', 'chapters': 24, 'order': 10},
    {'name': '1 Kings', 'chapters': 22, 'order': 11},
    {'name': '2 Kings', 'chapters': 25, 'order': 12},
    {'name': '1 Chronicles', 'chapters': 29, 'order': 13},
    {'name': '2 Chronicles', 'chapters': 36, 'order': 14},
    {'name': 'Ezra', 'chapters': 10, 'order': 15},
    {'name': 'Nehemiah', 'chapters': 13, 'order': 16},
    {'name': 'Esther', 'chapters': 10, 'order': 17},
    {'name': 'Job', 'chapters': 42, 'order': 18},
    {'name': 'Psalms', 'chapters': 150, 'order': 19},
    {'name': 'Proverbs', 'chapters': 31, 'order': 20},
    {'name': 'Ecclesiastes', 'chapters': 12, 'order': 21},
    {'name': 'Song of Solomon', 'chapters': 8, 'order': 22},
    {'name': 'Isaiah', 'chapters': 66, 'order': 23},
    {'name': 'Jeremiah', 'chapters': 52, 'order': 24},
    {'name': 'Lamentations', 'chapters': 5, 'order': 25},
    {'name': 'Ezekiel', 'chapters': 48, 'order': 26},
    {'name': 'Daniel', 'chapters': 12, 'order': 27},
    {'name': 'Hosea', 'chapters': 14, 'order': 28},
    {'name': 'Joel', 'chapters': 3, 'order': 29},
    {'name': 'Amos', 'chapters': 9, 'order': 30},
    {'name': 'Obadiah', 'chapters': 1, 'order': 31},
    {'name': 'Jonah', 'chapters': 4, 'order': 32},
    {'name': 'Micah', 'chapters': 7, 'order': 33},
    {'name': 'Nahum', 'chapters': 3, 'order': 34},
    {'name': 'Habakkuk', 'chapters': 3, 'order': 35},
    {'name': 'Zephaniah', 'chapters': 3, 'order': 36},
    {'name': 'Haggai', 'chapters': 2, 'order': 37},
    {'name': 'Zechariah', 'chapters': 14, 'order': 38},
    {'name': 'Malachi', 'chapters': 4, 'order': 39},
    {'name': 'Matthew', 'chapters': 28, 'order': 40},
    {'name': 'Mark', 'chapters': 16, 'order': 41},
    {'name': 'Luke', 'chapters': 24, 'order': 42},
    {'name': 'John', 'chapters': 21, 'order': 43},
    {'name': 'Acts', 'chapters': 28, 'order': 44},
    {'name': 'Romans', 'chapters': 16, 'order': 45},
    {'name': '1 Corinthians', 'chapters': 16, 'order': 46},
    {'name': '2 Corinthians', 'chapters': 13, 'order': 47},
    {'name': 'Galatians', 'chapters': 6, 'order': 48},
    {'name': 'Ephesians', 'chapters': 6, 'order': 49},
    {'name': 'Philippians', 'chapters': 4, 'order': 50},
    {'name': 'Colossians', 'chapters': 4, 'order': 51},
    {'name': '1 Thessalonians', 'chapters': 5, 'order': 52},
    {'name': '2 Thessalonians', 'chapters': 3, 'order': 53},
    {'name': '1 Timothy', 'chapters': 6, 'order': 54},
    {'name': '2 Timothy', 'chapters': 4, 'order': 55},
    {'name': 'Titus', 'chapters': 3, 'order': 56},
    {'name': 'Philemon', 'chapters': 1, 'order': 57},
    {'name': 'Hebrews', 'chapters': 13, 'order': 58},
    {'name': 'James', 'chapters': 5, 'order': 59},
    {'name': '1 Peter', 'chapters': 5, 'order': 60},
    {'name': '2 Peter', 'chapters': 3, 'order': 61},
    {'name': '1 John', 'chapters': 5, 'order': 62},
    {'name': '2 John', 'chapters': 1, 'order': 63},
    {'name': '3 John', 'chapters': 1, 'order': 64},
    {'name': 'Jude', 'chapters': 1, 'order': 65},
    {'name': 'Revelation', 'chapters': 22, 'order': 66},
]


def get__post_books():
    
    books = Books.objects.all().order_by('order')
    for book in bible_books:
        book_id = books.get(order=book['order'])
        book_id.chapters = book['order']
        book.save()
        
       
    

# get__post_books()