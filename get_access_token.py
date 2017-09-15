from config import KEY, SECRET_KEY
import oauth2 as oauth

request_token_url = 'http://www.goodreads.com/oauth/request_token'
authorize_url = 'http://www.goodreads.com/oauth/authorize'
access_token_url = 'http://www.goodreads.com/oauth/access_token'

# Get Request token
consumer = oauth.Consumer(key=KEY, secret=SECRET_KEY)
client = oauth.Client(consumer)
response, content = client.request(request_token_url, 'GET')
request_token = dict(map(lambda x: tuple(x.split("=")),
                         content.decode().split("&")))

# Get User permission
authorize_link = '{0}?oauth_token={1}'.format(
    authorize_url, request_token['oauth_token'])
print(authorize_link)
wait_for_authorization = input()

# Get Access token
token = oauth.Token(request_token['oauth_token'],
                    request_token['oauth_token_secret'])
client = oauth.Client(consumer, token)
response, content = client.request(access_token_url, 'POST')
access_token = dict(map(lambda x: tuple(x.split("=")),
                        content.decode().split("&")))
print(access_token['oauth_token'])
print(access_token['oauth_token_secret'])
