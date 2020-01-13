import requests
import xml.etree.ElementTree as ET

def query(link):
    r = requests.get(link)
    root = ET.fromstring(r.content)

    name = []
    id = []
    year = []
    type = []
    nkids = 0

    for child in root.iter('*'):
        if(child.tag == 'item'):
            id.append(child.get('id'))
            type.append(child.get('type'))
        for primary in child.findall('name'):
            name.append(primary.get('value'))
        """for pub in child.findall('yearpublished'):
            year.append(pub.get('value'))"""
        for x in child:
            for j in x:
                nkids += 1
                #print(j)
            #print(nkids)
            if(nkids == 1):
                #print(x)
                year.append("NA")
            elif(nkids == 2):
                for pub in x.findall('yearpublished'):
                    year.append(pub.get('value'))
            #print(x)
            nkids=0

    #print(nchild)
    """
    for i in range(len(name)):
        print(name[i] + ", " + year[i] + ": " + id[i] + "; " + type[i])
    """
    return(name, year, id, type)
