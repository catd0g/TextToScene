import os
import json
import spacy
import xml.etree.ElementTree as ET

nlp = spacy.load("en_core_web_sm")

L = []
for root, dirs, files in os.walk('Traning'):
    L.append((root,dirs,files))

data = []

"""
for i in L:
    if(i[2] != []):
        for k in i[2]:
            if(k.find(".xml") != -1):
                print(i[0]+"\\"+k)
                tree = ET.parse(i[0]+"\\"+k)
                root = tree.getroot()
                print(root[0].text)
"""

def retrieve_data(file):
    tree = ET.parse(file)
    root = tree.getroot()
    a = ET.Element('SpaceEvalPlusPoS')
    b = ET.SubElement(a, 'DATA')
    b.set("source", file)
    c = ET.SubElement(b,'TEXT')
    d = ET.SubElement(b,'TOKENS')
    c.text = root[0].text
    c.tail = '\n'
    b.append(root[1])
    #print(b.findall('.//TAGS/METALINK'))
    doc = nlp(root[0].text)
    for token in doc:
        e = ET.SubElement(d,'TOKEN')
        e.set('text',token.text)
        e.set('lemma',token.lemma_)
        e.set('pos',token.pos_)
        e.set('tag',token.tag_)
        e.set('dep',token.dep_)
        e.set('shape',token.shape_)
        e.set('is_alpha', str(token.is_alpha))
        e.set('is_stop',str(token.is_stop))
        e.tail = '\n'
    new_root = ET.ElementTree(a)
    new_root.write("test.xml")
    return 

def write_xml(data):
    return


retrieve_data('Traning\RFC\Bicycles.xml')

