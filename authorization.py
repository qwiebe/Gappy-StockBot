# Import methods (?right terminology?)
import time
import urllib
import requests
import json
from splinter import Browser
from config import user, password, client_id, security_question

#################################################################################
#   TO DO:  - implement Refresh Token (decoded_content['refresh_token'])        #
#             must compare time of token creation to current date.              #
#             This way, the automation process won't excecute after every test  #
#           - Research how to write to .json file to store refresh_token        #
#################################################################################


# -------------------- AUTH AUTOMATION --------------------
# defines location of Chrome Driver
executable_path = {'executable_path': r'/Users/Quinton/Desktop/Financial/StockBot/resources/chromedriver'}

# Create instance of browser (iot to watch browser, Headless = False)
browser = Browser('chrome', **executable_path, headless=False)

# Components to build URL
url = 'https://auth.tdameritrade.com/auth?'
client_code = client_id + '@AMER.OAUTHAP'
payload = {'response_type':'code', 'redirect_uri':'https://localhost/test', 'client_id':client_code}

# Build URL
myurl = requests.Request('GET', url, params = payload).prepare().url

# go to the URL
browser.visit(myurl)

# fill out the Log-In form
browser.find_by_id("username").first.fill(user)
browser.find_by_id("password").first.fill(password)
browser.find_by_id("accept").first.click()
time.sleep(1)

# Get the Text Message Box
browser.find_by_text('Can\'t get the text message?').first.click()

# Get the Answer Box
browser.find_by_value("Answer a security question").first.click()

# Answer the Security Questions.
if browser.is_text_present('What is your maternal grandmother\'s first name?'):
    browser.find_by_id('secretquestion').first.fill(security_question['abuela'])

elif browser.is_text_present('What is your mother\'s middle name?'):
    browser.find_by_id('secretquestion').first.fill(security_question['momMiddle'])

elif browser.is_text_present('What was your high school mascot?'):
    browser.find_by_id('secretquestion').first.fill(security_question['hsMascot'])

elif browser.is_text_present('What was the name of your junior high school?'):
    browser.find_by_id('secretquestion').first.fill(security_question['juniorHigh'])

browser.find_by_id("accept").first.click()

# Sleep and Accept Terms
time.sleep(1)
browser.find_by_id('accept').first.click()

# Retreive authorization url
auth_url = browser.url

# decode auth_url and retrieve Auth code
auth_code = urllib.parse.unquote(auth_url.split('code=')[1])

# close the browser
browser.quit()

# check if auth_code was retrieved
#print(auth_code)


# AUTHENTICATION ENDPOINT

# define the endpoint url
url = r'https://api.tdameritrade.com/v1/oauth2/token'

# define headers
headers = {'Content-Type':'application/x-www-form-urlencoded'}

# define payload
payload = {'grant_type': 'authorization_code',
            'access_type': 'offline',
            'code': auth_code,
            'client_id': client_id,
            'redirect_uri': 'https://localhost/test'}

# post the data to get token
authReply = requests.post(url, headers = headers, data = payload)

decoded_content = authReply.json()
#print(decoded_content)

# grab the access_token
access_token = decoded_content['access_token']

headers = {'Authorization': 'Bearer {}'.format(access_token)}