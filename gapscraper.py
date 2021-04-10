import time
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from private.config import user, password, security_question

# ------------------------------ CONSTANTS ------------------------------
# Access URL
URL = r'https://secure.tdameritrade.com/screener/stocks'
LOGIN_URL = r'https://auth.tdameritrade.com/auth?response_type=code&client_id=MOBI%40AMER.OAUTHAP&redirect_uri=https%3A%2F%2Fsecure.tdameritrade.com%2FauthCafe'
page = requests.get(URL)

# defines location of Chrome Driver
executable_path = {'executable_path': r'/Users/Quinton/Desktop/Financial/StockBot/resources/chromedriver'}

# Create instance of browser (iot to watch browser, Headless = False)
browser = Browser('chrome', **executable_path, headless=False)
# -----------------------------------------------------------------------

# ------------------------------ FUNCTIONS ------------------------------
# Returns whether the user is logged in
def loggedIn():
    page = requests.get(URL).text

    manipPage = BeautifulSoup(page, 'html.parser')

    if manipPage.title.text == 'TD Ameritrade Login':
        print('Currently on Login Page')
        status = False
    elif manipPage.title.text == 'TD Ameritrade':
        print('Logged In')
        status = True
    else:
        print('ERROR: WRONG SITE')
        status = 'ERROR'
    return status

# Logs user in
def logIn(url, username, password):
    # Build URL
    myurl = requests.Request('GET', url).prepare().url

    # go to the URL
    browser.visit(myurl)

    # Fill User ID and Password
    browser.find_by_id("username").first.fill(username)
    browser.find_by_id('password').first.fill(password)
    browser.find_by_id('accept').first.click()

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
    time.sleep(5)

# Returns list of tickers that have gapped
def scrapeTickers(url):
    # Build URL
    myurl = requests.Request('GET', url).prepare().url

    # go to the URL
    browser.visit(myurl)
    
    # wait to load
    time.sleep(10)

    # Used for testing, to check the html
    #sourceCode = browser.html

    # Find the link for the 2to20 Gap Up scanner
    with browser.get_iframe('main') as iframe:
        iframe.find_by_xpath('//a[@class="screenName"]').click()

    # wait to load
    time.sleep(2)

    # Find the list of gappers
    with browser.get_iframe('main') as iframe:
        iframe.DO_SOMETHING()
    
    browser.quit()

def scrapeProcess():
    LoggedIn = loggedIn()
    
    # Am I logged in?  If so, scrape and return tickers
    if LoggedIn == True:
        return scrapeTickers(URL)
    # if not, login using splinter, Browser
    elif LoggedIn == False:
        logIn(LOGIN_URL, user, password)
        scrapeProcess()
    elif LoggedIn == 'ERROR':
        print('This is a redundant error because an error was printed in loggedIn()')
# -----------------------------------------------------------------------


# -------------------------- RETURN VARIABLES ---------------------------
tickers = scrapeProcess()
# -----------------------------------------------------------------------


# ------------------------------- TESTING -------------------------------
'''logIn(LOGIN_URL, user, password)

log = loggedIn()

scrapeTickers(URL)'''
# -----------------------------------------------------------------------


