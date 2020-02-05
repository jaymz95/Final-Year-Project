from lxml import etree

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


root = etree.fromstring(data)

toner_id = "095205615111"

# find a toner
results = root.xpath("//t[@id = '%s']" % toner_id)
if not results:
    raise Exception("Toner does not exist")

toner = results[0]

# change the amount
amount = toner.find("amount")
amount.text = str(int(amount.text) + 1)

print(etree.tostring(root))