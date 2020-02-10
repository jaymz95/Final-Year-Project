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

    
    page = codecs.open("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html", 'r')
    
    tt = etree.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html")
    ttt = etree.tostring(tt.getroot())

    root = etree.fromstring(ttt)

    toner_id = "response"
    userInput = "userInput"

    root = html.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html").getroot()
    element = root.get_element_by_id(toner_id)

    userText = root.xpath("//textarea[@id = '%s']" % userInput) 
    if not userText:
        raise Exception("Toner does not exist")


    results = root.xpath("//h4[@id = '%s']" % toner_id) 
    if not results:
        raise Exception("Toner does not exist")

    toner = results[0]

    # change the amount
    amount = toner.find("div")
    #amount.text = str("Where AM I??????????????????????????????????????")

    r = root.getroottree()

    r.write(open('FinalYearProject/templates/chat.html', 'wb'))

    #res = "response"

    # find a toner
    #results = root.xpath("//t[@id = '%s']" % res)
    #if not results:
    #    raise Exception("Toner does not exist")

    #toner = results[0]

    # change the amount
    #div = toner.find("div")
    #div.text = str(1)

    #print(etree.tostring(root))

    return app
