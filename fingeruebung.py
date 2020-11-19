import os
import json
import spacy
import networkx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

nlp = spacy.load("en_core_web_sm")



def treewalk_for_xml_files(rootdir):
    L = []
    filelist = []
    for root, dirs, files in os.walk(rootdir):
        L.append((root,dirs,files))

    for i in L:
        if(i[2] != []):
            for k in i[2]:
                if(k.find(".xml") != -1):
                    print(i[0]+"\\"+k)
                    filelist.append(i[0]+"\\"+k)
    return filelist


def retrieve_data(file):
    tree = ET.parse(file)
    root = tree.getroot()
    a = ET.Element('ENTRY')
    a.tail = '\n'
    b = ET.SubElement(a, 'DATA')
    b.append(root[1])
    b.tail = '\n'
    b.set("source", file)
    c = ET.SubElement(b,'TEXT')
    c.text = root[0].text
    c.tail = '\n'
    d = ET.SubElement(b,'TOKENS')
    d.tail = '\n'
    f = ET.SubElement(b,'SENTENCES')
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
    for sent in doc.sents:
        g = ET.SubElement(f,'SENTENCE')
        g.text = str(sent.text)
        g.set('length', str(len(sent.text)))
        g.tail = '\n'
    return a

def write_xml():
    filelist = treewalk_for_xml_files('Traning')
    a = ET.Element('SpacePlusPos')
    for file in filelist:
        a.append(retrieve_data(file))
    new_root = ET.ElementTree(a)
    new_root.write('combined_data.xml')

def count_elements(list):
    literal = []
    count = []
    for entry in list:
        try:
            pos = literal.index(entry)
            count[pos]+=1
        except ValueError:
            literal.append(entry)
            count.append(1)
    return [(literal[x],count[x]) for x in range(0,len(literal))]

def auswertung():
    tree = ET.parse('combined_data.xml')
    list1 = [x.tag for x in tree.findall('.//TAGS/*')]
    list1 = count_elements(list1)
    list2 = [x.get('pos') for x in tree.findall('.//TOKEN')]
    list2 = count_elements(list2)
    list3 = [x.get('length') for x in tree.findall('.//SENTENCE')]
    list3 = count_elements(list3)
    list3.sort(key=lambda x: int(x[0]))
    list4 = [x.get('relType') for x in tree.findall('.//TAGS/QSLINK')]
    list4 = count_elements(list4)
    list5 = [x.get('text') for x in tree.findall('.//TAGS/MOTION')]
    list5 = count_elements(list5)
    list5.sort(key=lambda x: int(x[1]))
    list5.reverse()
    print("Auswertung:")
    print("Anzahl PoS Tags:")
    for x in list2:
        print(x)
    print('\n')    
    print("SpacialEntities: " + str([i[1] for i in list1 if i[0] == 'SPATIAL_ENTITY'].pop()))
    print("Places: " + str([i[1] for i in list1 if i[0] == 'PLACE'].pop()))
    print("Motions: " + str([i[1] for i in list1 if i[0] == 'MOTION'].pop()))
    print("Signals: " + str([i[1] for i in list1 if i[0] == 'SPATIAL_SIGNAL'].pop() + [i[1] for i in list1 if i[0]== 'MOTION_SIGNAL'].pop()))
    print("QsLinks: " + str([i[1] for i in list1 if i[0] == 'QSLINK'].pop()))
    print("OLinks: " + str([i[1] for i in list1 if i[0] == 'OLINK'].pop()))
    print('\nQsLink Typen:')
    for x in list4:
        print(x)
    plt.plot([int(x[0]) for x in list3],[x[1] for x in list3])
    plt.show()
    print('\nQSLINKS und OLINKS Trigger:')
    entries = tree.findall('.//ENTRY')
    links = []
    spatial_signals = []
    for e in entries:
        qsolinks = e.findall('.//TAGS/QSLINK')
        qsolinks += e.findall('.//TAGS/OLINK')
        ssignal = e.findall('.//TAGS/SPATIAL_SIGNAL')
        for qs in qsolinks:
            tmp = [x.get('text') for x in ssignal if x.get('id') == qs.get('trigger')]
            ss = "" if len(tmp) == 0 else tmp.pop()
            try:
                pos = links.index(qs.get('relType'))
                try:
                    pos2 = spatial_signals[pos].index(ss)
                except ValueError:
                    spatial_signals[pos].append(ss)
            except ValueError:
                links.append(qs.get('relType'))
                spatial_signals.append([ss])
    for e in [(links[x],spatial_signals[x]) for x in range(0,len(links))]:
        print(e)
    print("Die 5 häufigsten MOVEMENT Verben:")
    print(list5[:5])
    
write_xml()
auswertung()
