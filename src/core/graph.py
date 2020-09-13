import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup
import requests
from PIL import Image


def __getArtistImageURL(artistName):
    url = f'https://en.wikipedia.org/wiki/{artistName}'
    # get contents from url
    content = requests.get(url).content
    # get soup
    soup = BeautifulSoup(content, 'html.parser')  # choose lxml parser
    # find the tag : <img ... >
    image_tag = soup.find_all('img')[1]
    # print out image urls
    return f"https:{image_tag['src']}"


def __getImgFromURL(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def getGraph(enteredArtistName, connections):
    G = nx.Graph()
    for artistName in connections:
        url = connections[artistName][1]
        G.add_node(artistName,
                   image=__getImgFromURL(url))
        if artistName != enteredArtistName:
            G.add_edge(enteredArtistName, artistName)

    pos = nx.circular_layout(G)
    fig = plt.figure(figsize=(G.size(), G.size()))
    ax = plt.subplot(111)
    ax.set_aspect('equal')
    nx.draw_networkx_edges(G, pos, ax=ax)

    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)

    trans = ax.transData.transform
    trans2 = fig.transFigure.inverted().transform

    # this is the image size
    piesize = 0.1
    p2 = piesize / 2.0
    for n in G.nodes():
        # figure coordinates
        xx, yy = trans(pos[n])
        # axes coordinates
        xa, ya = trans2((xx, yy))
        a = plt.axes([xa - p2, ya - p2, piesize, piesize])
        a.set_aspect('equal')
        a.imshow(G.nodes()[n]['image'])
        a.axis('off')
    ax.axis('off')
    img = BytesIO()
    plt.savefig(img)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(img.getvalue()).decode('utf8')
    img.seek(0)
    plt.clf()
    return pngImageB64String

