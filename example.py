from config import KEY, SECRET_KEY, MY_TOKEN, MY_TOKEN_SECRET
from string import Template
from time import sleep
import oauth2 as oauth
import xml.dom.minidom
import urllib

# N of requests
# 1 to get oauth user id
# 1 per 200 books to_read until empty page, I can store that


def get_books_on_shelf_by_page(**data):
    # 1 request
    req = 'http://www.goodreads.com/review/list?v=2&format=xml&v=2&id={user_id}&sort=author&key={key}&page={page}&per_page=200&shelf={shelf}'.format(
        **data, key=KEY)
    body = urllib.parse.urlencode({}).encode()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response, content = client.request(req, 'GET', body, headers)
    return content


def get_friends(**data):
    # 1 request
    req = 'http://www.goodreads.com/friend/user.xml?id={user_id}&page={page}'.format(
        **data)
    body = urllib.parse.urlencode({}).encode()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response, content = client.request(req, 'GET', body, headers)
    return content


def book_info(book):
    book_id = book.getElementsByTagName('id')[0].firstChild.nodeValue
    book_title = book.getElementsByTagName('title')[0].firstChild.nodeValue
    return book_id, book_title


def user_info(user):
    if user.hasChildNodes():
        user_id = user.getElementsByTagName('id')[0].firstChild.nodeValue
        user_name = user.getElementsByTagName('name')[0].firstChild.nodeValue
        return user_id, user_name


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
        user_id=user_id, page=current_page, shelf="to-read")
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
    print("{} BOOKS ON PAGE {}".format(books_page, current_page))
    current_page += 1
print("{} BOOKS TO READ IN TOTAL".format(books_total))


# Friends user has and books owned by friends
# id, name, link, image_url, friends_count
current_page = 1
friends_page = 1
friends_total = 0
owned_counter = 0

while friends_page:
    content = get_friends(user_id=user_id, page=current_page)
    content_xml = xml.dom.minidom.parseString(content)
    friends_page = 0
    for friend in content_xml.getElementsByTagName('user'):
        friend_info = user_info(friend)
        if friend_info:
            friend_id, friend_name = friend_info
            req = 'https://www.goodreads.com/owned_books/user?format=xml&id={}'.format(
                friend_id)
            body = urllib.parse.urlencode({}).encode()
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            r, c = client.request(req, 'GET', body, headers)
            cx = xml.dom.minidom.parseString(
                c).getElementsByTagName('owned_book')
            if cx:
                print("{} tiene libros".format(friend_name.encode('utf-8')))
                owned_counter += 1
            try:
                print(friend_id, friend_name.encode('utf-8'))
            except UnicodeEncodeError:
                print("ERROR")
            friends_page += 1
            friends_total += 1
    print("{} FRIENDS ON PAGE {}".format(friends_page, current_page))
    current_page += 1
print("{} TOTAL FRIENDS".format(friends_total))
print("{} FRIENDS WITH BOOKS".format(owned_counter))
