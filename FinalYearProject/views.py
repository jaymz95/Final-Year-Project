from flask import Blueprint, render_template, request
from lxml import etree, html
from io import StringIO, BytesIO
import random
from chatterbot import ChatBot
#from .model import chatbot

# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('chat.html')
    if request.method == 'POST':
        userInput = request.form['text']
        processed_text = chatbot.get_response(userInput)
        
        return render_template('chat.html', processed_text=processed_text)   
    else:
        return render_template('chat.html')