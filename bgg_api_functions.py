import requests
import xml.etree.ElementTree as ET
import pandas as pd


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
            if(nkids == 1):
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

def getBoxArt(ids):
    joined_ids = ','.join(map(str,ids))

    image_urls = []
    link = "https://api.geekdo.com/xmlapi2/thing?id={}&stats=1".format(joined_ids)

    np_img = 0
    r = requests.get(link)
    root = ET.fromstring(r.content)
    no_image = 'https://upload.wikimedia.org/wikipedia/commons/0/0a/No-image-available.png'
    tags = []
    for item in root.findall('item'):
        for x in item.iter('*'):
            tags.append(x.tag)
            if(x.tag == 'image'):
                image_urls.append(x.text)
        if('image' not in tags):
            image_urls.append(no_image)
        else:
            pass
        tags=[]



    #print(type(image_urls))
    print("Box Art acquired")
    #print(joined_ids)
    print(image_urls)
    #print(image_urls[0])
    return image_urls


def getInfo(csv, ids, df):

    format_ids = ','.join(map(str,ids))
    link = "https://api.geekdo.com/xmlapi2/thing?id={}&stats=1".format(format_ids)
    url, name, year, min, max = ([] for i in range(5))
    r = requests.get(link)
    root = ET.fromstring(r.content)


    for i in ids:
        url.append("https://boardgamegeek.com/boardgame/{}".format(i))
    for child in root.iter('*'):
        if(child.tag == 'yearpublished'):
            year.append(child.get('value'))
            #df = df.append({'Year':child.get('value')},ignore_index=True)
        elif (child.tag =='name'):
            if(child.get('type') == 'primary'):
                name.append(child.get('value'))
                #df = df.append({'Name':child.get('value')},ignore_index=True)
        elif(child.tag == 'minplayers'):
            min.append(child.get('value'))
            #df = df.append({'Min. Players': child.get('value')},ignore_index=True)
        elif(child.tag == 'maxplayers'):
            max.append(child.get('value'))
            #df = df.append({'Max Players': child.get('value')},ignore_index=True)
        else: pass

    for i in range(len(url)):
        df = df.append({'Name':name[i],'Year':year[i],'Min. Players':min[i], 'Max Players':max[i], 'Link':url[i]}, ignore_index=True)
    return df
