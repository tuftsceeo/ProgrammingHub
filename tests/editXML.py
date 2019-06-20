import xml.etree.ElementTree as xml
import os

filename = (os.getcwd()+'/includes/XML_test.xml')
print(filename)
root = xml.Element("note")
userelement = xml.Element("terminalContent")
root.append(userelement)
uid = xml.SubElement(userelement, "uid")
uid.text = "1"
# root = xml.Element("note")
# userelement = xml.Element("terminalContent")
# uid = xml.SubElement(userelement, "uid")
# uid.text = "reply"