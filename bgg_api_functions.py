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
    itext = 'https://upload.wikimedia.org/wikipedia/commons/0/0a/No-image-available.png'
    for child in root.iter('*'):
        for x in child:
            if(x.tag=='image'):
                #print(x.text)
                np_img +=1
            if((np_img >0) & (x.tag =='image')):
                    image_urls.append(x.text)
            #else:
                #itext = child.text
                #pass#image_urls.append(itext)
        if(child.tag == 'image'):
            if (np_img > 0):
                pass#image_urls.append(child.text)
            else:
                image_urls.append(itext)
        np_img = 0
                #print(x.text)

        """if(child.tag == 'image'):
            itext = child.text
            image_urls.append(itext)
            print(child.text)"""
            #image_urls.append('None')

    #print(type(image_urls))
    print("Box Art acquired")
    #print(joined_ids)
    print(image_urls)
    #print(image_urls[0])
    return image_urls
