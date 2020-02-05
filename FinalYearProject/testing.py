from train import chatbot
#from bs4 import BeautifulSoup
#from selenium import webdriver

while True:

    request = input('You:')

    # Get a response to the input text 'I would like to book a flight.'
    response = chatbot.get_response(request)

    print("  ", response)
