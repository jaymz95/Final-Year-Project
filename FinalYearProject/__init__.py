from flask import Flask
import urllib.request
from lxml import etree, html
from io import StringIO, BytesIO
from bs4 import BeautifulSoup
import codecs

def create_app():
    app = Flask(__name__)

    from .views import main
    app.register_blueprint(main)

    tt = etree.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html")
    ttt = etree.tostring(tt.getroot())

    root = etree.fromstring(ttt)

    response_id = "response"
    userInput = "userInput"

    root = html.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html").getroot()
    element = root.get_element_by_id(response_id)

    userText = root.xpath("//textarea[@id = '%s']" % userInput) 
    if not userText:
        raise Exception("Toner does not exist")


    results = root.xpath("//h4[@id = '%s']" % response_id) 
    if not results:
        raise Exception("id 'response' does not exist")

    response = results[0]

    # change the amount
    # amount = response.find("div")

    r = root.getroottree()

    r.write(open('FinalYearProject/templates/chat.html', 'wb'))

    return app
