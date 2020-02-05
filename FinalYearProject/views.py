from flask import Blueprint, render_template
from lxml import etree, html
from io import StringIO, BytesIO
#from bs4 import BeautifulSoup
#from selenium import webdriver

main = Blueprint('main', __name__)


#html_doc = 'chat.html'

#soup = BeautifulSoup(html_doc, 'html.parser')
#soup.find(id="response")





@main.route('/')
def index():
    return render_template('chat.html')