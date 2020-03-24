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

    # soup = soup("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html")

    # reply = soup.find('html/body/div/h4/div')
    # reply['content'] = "text/html; charset=UTF-8"
    # reply['http-equiv'] = "Content-Type"
    # title.insert_after(reply)
    # tag.name = 'html/body/div/h4/div'
    # tag.string.replace_with("No longer bold")

    chatHtml = open("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html",'r')
    soup = BeautifulSoup(chatHtml, 'lxml')
    #print(soup)
    tag = soup.select('h4[id="response"]')
    #tag = soup.find(id='response')

    # from BeautifulSoup import BeautifulSoup, Tag
    # soup = BeautifulSoup("<b>Argh!<a>Foo</a></b><i>Blah!</i>")
    # tag = Tag(soup, "div", [("id", result)])
    # tag.insert(0, "ohhhhhprocessed_text[0]")
    # soup.a.replaceWith(tag)
    # print soup
    # <b>Argh!<newTag id="1">Hooray!</newTag></b><i>Blah!</i>
    
    if len(tag) > 0:
        print(len(tag))
        print("TAG: +++++++++++++++++++", tag[0])

        s = BeautifulSoup()
        new_div = s.new_tag('div')
        new_div.string='<a href="index.html" id="websiteName">Foo</a>'
        #new_div.prettify(formatter="html")
        #print(new_div.prettify(formatter="html"))
        n = new_div.encode(formatter=None)
        print(new_div)

        # root = ElementTree.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html").getroot()
        # bodyEl = root.find('body/div/h4')
        # c = ElementTree.Element("div")
        # c.text = "3"

        # bodyEl.insert(1, c)
        # ElementTree.dump(root)
        # print("\n\n\n\n\n\n\n\n\n\n\n")
        # print(str(ElementTree.dump(root)))


        #tag[0].contents = "ohhhhhprocessed_text[0]"
        # di = Tag(tag, "div", [("id", 1)])
        # di.insert(0, "ohhhhhprocessed_text[0]")
        #tag[0].div.replaceWith(n)

    #print(soup)
    # >>> <a href="index.html" id="websiteName">Foo</a>
    chath = ElementTree.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html").getroot()
    bodyEl = chath.find('body/div/h4')
    c = ElementTree.Element("div")
    c.text = "3"

    bodyEl.insert(1, c)
    ElementTree.dump(chath)
    print("\n\n\n\n\n\n\n\n\n\n\n")
    files = str(ElementTree.dump(chath))

    #tag.string.replace_with("ohhhhhprocessed_text[0]")
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    print(str(ElementTree.dump(chath)))
    print("here")
    print(ElementTree.tostring(chath, encoding="unicode", method="html", short_empty_elements=False))
    print("there")

    #print soup
    #33

    file="/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html"
    with open(file, 'w') as filetowrite:
        filetowrite.write(ElementTree.tostring(chath, encoding="unicode", method="html"))

    tt = etree.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html")
    ttt = etree.tostring(tt.getroot())

    root = etree.fromstring(ttt)

    response_id = "response"
    userInput = "userInput"

    root = html.parse("/home/jaymz95/Desktop/Final-Year-Project/FinalYearProject/templates/chat.html").getroot()
    #element = root.get_element_by_id(response_id)

    # user input from views.py which gets it from the chat.html textarea
    userText = root.xpath("//textarea[@id = '%s']" % userInput) 
    if not userText:
        raise Exception("Toner does not exist")


    results = root.xpath("//h4[@id = '%s']" % response_id) 
    if not results:
        raise Exception("id 'response' does not exist")
    #root.xpath("//h4[@id = '%s']" % response_id) = processed_text
    response = results[0]

    # change the amount
    # amount = response.find("div")

    r = root.getroottree()

    r.write(open('FinalYearProject/templates/chat.html', 'wb'))

    return app
