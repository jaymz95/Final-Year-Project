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
    
    data = """<?xml version="1.0"?>
    <printer>
        <t id="095205615111"> <!-- 7545 Magenta -->
            <toner>7545 Magenta Toner</toner>
            <amount>3</amount>
        </t>
        <t id="095205615104"> <!-- 7545 Yellow -->
            <toner>7545 Yellow Toner</toner>
            <amount>7</amount>
        </t>
    </printer>"""

    tt = etree.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html")
    ttt = etree.tostring(tt.getroot())

    url = "https://lionbridge.ai/datasets/15-best-chatbot-datasets-for-machine-learning/"
    #pages = html.fromstring(urllib.request.urlopen(page).read())

    #soupp  = BeautifulSoup(urllib.request.urlopen(url).read())

    #broken_html = "chat.html"

    #parser = etree.HTMLParser()
    #tree   = etree.parse(StringIO(soupp.get_text()), parser)

    #result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
    #print("99999999999999999999999999999999")
    #print(result)
    print(99999999999999999999999999999999999999999999999999999999999999999999999999999999999)
    #print(page.read())

    #soup = BeautifulSoup(page.read())
    print("----------------------------------------------------------------------------------")
    #print(pages)

    root = etree.fromstring(ttt)
    #print(page.read())

    toner_id = "response"

    # find a toner
    # h4 is because we are looking for a tag "response" in a h4 tag
    results = root.xpath("//h4[@id = '%s']" % toner_id) 
    if not results:
        raise Exception("Toner does not exist")

    toner = results[0]

    # change the amount
    amount = toner.find("div")
    amount.text = str("Where AM I??????????????????????????????????????")

    print(etree.tostring(root))
    #et = etree.ElementTree(root)
    #et.write(sys.stdout, pretty_print=True)
    r = root.getroottree()
    

    f= open("guru99.txt","w+")

    #for i in range(10):
    #    f.write("This is line %d\r\n" % (i+1))

    #f.close() 

    #with open('test.html', 'wb+') as myfile:
    #    myfile.write("What")

    r.write(open('FinalYearProject/templates/chat.html', 'wb'))

    res = "response"

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


  