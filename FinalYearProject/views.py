from flask import Blueprint, render_template, request
from lxml import etree, html
from io import StringIO, BytesIO
import random
from chatterbot import ChatBot
#from bs4 import BeautifulSoup
#from selenium import webdriver
#from .model import chatbot
#from bs4 import BeautifulSoup
#from selenium import webdriver

#request = ""

# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')


#request = input('You:')
no = 1
# Get a response to the input text 'I would like to book a flight.'




main = Blueprint('main', __name__)


#html_doc = 'chat.html'

#soup = BeautifulSoup(html_doc, 'html.parser')
#soup.find(id="response")


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('chat.html')
    if request.method == 'POST':
        human1 = request.form['text']
        response = chatbot.get_response(human1)

        print("  ", response)
        processed_text = response
        return render_template('chat.html', processed_text=processed_text)   
    else:
        return render_template('chat.html')