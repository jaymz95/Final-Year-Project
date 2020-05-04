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
        from FinalYearProject.StackTest.dataset import query
        userInput = request.form['text']
        #processed_text = chatbot.get_response(userInput)
        processed_text = query(userInput)

        # append instead of overright
        return render_template('chat.html', processed_text=processed_text[0][0], stack_link=processed_text[1][0])   
    else:
        return render_template('chat.html')