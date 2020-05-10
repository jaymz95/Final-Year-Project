from flask import Flask
import urllib.request
from lxml import etree, html
from xml.etree import ElementTree
from io import StringIO, BytesIO
from bs4 import BeautifulSoup, Tag
import codecs


def create_app():
    app = Flask(__name__)

    from .views import main
    app.register_blueprint(main)

    chatHtml = open("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html",'r')
    soup = BeautifulSoup(chatHtml, 'lxml')
    tag = soup.select('div[id="result"]')
    
    if len(tag) > 0:

        s = BeautifulSoup(features="lxml")
        new_div = s.new_tag('div', id="result")
        new_div.string='<a href="index.html" id="websiteName">Foo</a>'

        tag[0].contents = "ohhhhhprocessed_text[0]"
        tag[0].replaceWith(new_div)
       
    file="/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html"
    with open(file, 'w') as filetowrite:
        filetowrite.write(str(soup))

    tt = etree.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html")
    ttt = etree.tostring(tt.getroot())

    root = etree.fromstring(ttt)

    response_id = "response"
    userInput = "userInput"

    root = html.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html").getroot()

    # user input from views.py which gets it from the chat.html textarea
    userText = root.xpath("//textarea[@id = '%s']" % userInput) 
    if not userText:
        raise Exception("Toner does not exist")


    results = root.xpath("//h4[@id = '%s']" % response_id) 
    if not results:
        raise Exception("id 'response' does not exist")
    response = results[0]

    r = root.getroottree()

    r.write(open('FinalYearProject/templates/chat.html', 'wb'))

    return app
