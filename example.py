from config import KEY, SECRET_KEY, MY_TOKEN, MY_TOKEN_SECRET
from string import Template
import oauth2 as oauth
import xml.dom.minidom
import urllib


def get_books_on_shelf_by_page(**data):
    req = 'http://www.goodreads.com/review/list?format=xml&v=2&id={user_id}&sort=author&order=a&key={key}&page={page}&per_page=100&shelf={shelf}'.format(
        **data, key=KEY)
    body = urllib.parse.urlencode({}).encode()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response, content = client.request(req, 'GET', body, headers)
    return content


def book_info(book):
    book_id = book.getElementsByTagName('id')[0].firstChild.nodeValue
    book_title = book.getElementsByTagName('title')[0].firstChild.nodeValue
    return book_id, book_title


# Example use: Get user info
consumer = oauth.Consumer(key=KEY, secret=SECRET_KEY)
token = oauth.Token(MY_TOKEN, MY_TOKEN_SECRET)
client = oauth.Client(consumer, token)

# User id
response, content = client.request(
    'http://www.goodreads.com/api/auth_user', 'GET')
userxml = xml.dom.minidom.parseString(content)
user_id = userxml.getElementsByTagName('user')[0].attributes['id'].value

# Books user has on to-read shelf
current_page = 1
books_page = 1
books_total = 0
while books_page:
    content = get_books_on_shelf_by_page(
        user_id=user_id, page=current_page, shelf="read")
    content_xml = xml.dom.minidom.parseString(content)
    books_page = 0
    for book in content_xml.getElementsByTagName('book'):
        book_id, book_title = book_info(book)
        try:
            print(book_id, book_title.encode('utf-8'))
        except UnicodeEncodeError:
            print("ERROR")
        books_page += 1
        books_total += 1
    print("{} ON PAGE {}".format(books_page, current_page))
    current_page += 1
print("{} BOOKS IN TOTAL".format(books_total))
