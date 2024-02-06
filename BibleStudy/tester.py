import json

from BibleStudy.models import KingJamesVersionI

# Read JSON file
def add_verse():
    with open('D:\CMS\Church\BibleStudy\kjv.json') as json_file:
        data = json.load(json_file)

    # Iterate over the 'row' items in the JSON data
    for item in data['resultset']['row']:
        # Extract values from the 'field' list
        id,book, chapter, verse, text = item['field']
        print(book,chapter, verse, text)

        KingJamesVersionI.objects.create(
            book=book,
            chapter=chapter,
            verse=verse,
            text=text
       
        )
# add_verse()