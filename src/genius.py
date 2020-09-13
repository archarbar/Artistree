import requests
import json
from bs4 import BeautifulSoup
import re
import csv

genius_client_id = 'cSHZqVRH60I9GqbgI-EMEeCGm6EZD0hhiIcffqXCyGHWqzQ0nLJQarDscUhH3_HJ'
genius_secret_id = 'bJtcQAhAyV5yDBgqakLtYL0UJLD8UlfT7hrxLBMsvSEWOnPWcoSYpEcd3uhYi4QS9swjGDht4B3-nwEB-cVhjQ'
genius_client_access_token = 'DYw7-Hc_XXs6sv_Gao4xZAO0QwVwW9VS9Etjh35_C6Nbpn9964VAUtQlVRjpWP2j'
base_url = 'https://api.genius.com'
token = 'Bearer {}'.format(genius_client_access_token)
headers = {'Authorization': token}

def find_artist(artistName):
    song_path = 'search/'
    song_request_uri = '/'.join([base_url, song_path])

    params = {'q': artistName}

    song_request = requests.get(song_request_uri, params=params, headers=headers)
    # print(r.text)

    #link for most popular song for artist
    y = json.loads(song_request.text)
    try:
        artist = y['response']['hits'][0]['result']['primary_artist']
    except:
        return None
    return artist

# use beautiful soup to extract lyrics from html page
def find_lyrics(artist):
    song_lyrics = []

    artistID = str(artist['id'])
    artist_path = 'artists/'
    artist_request_uri = base_url + '/' + artist_path + artistID + '/songs?sort=popularity&per_page=30'
    artist_request = requests.get(artist_request_uri, headers=headers)
    z = json.loads(artist_request.text)
    for song in z['response']['songs']:
        url = ''.join(['https://genius.com', song['path']])
        page = requests.get(url)
        if page.status_code == 404:
            print("Song URL returned 404.")
            return None

        # Scrape the song lyrics from the HTML
        html = BeautifulSoup(page.text, "html.parser")

        # Determine the class of the div
        old_div = html.find("div", class_="lyrics")

        if old_div:
            lyrics = old_div.get_text()
        else:
            lyrics = ''
            for tag in html.find_all('div'):
                for attribute, value in list(tag.attrs.items()):
                    if attribute == 'class' and 'Lyrics__Root' in str(value):
                        lyrics = tag
                        break
                if lyrics:
                    break
            else:
                print("Couldn't find the lyrics section.")
                return None

            lyrics = lyrics.get_text('\n').replace('\n[', '\n\n[')

        lyrics = re.sub(r'(\[.*?\])*', '', lyrics)
        lyrics = re.sub('\n{2}', '\n', lyrics)  # Gaps between verses
        song_lyrics.append(lyrics.strip("\n"))
    return song_lyrics

def clean_lyrics(songs):
    names = []

    for song in songs:
        # use finditer because re.findall can't match capture groups
        # match all capitalized words/numbers of groups of capitalized words/numbers separated by spaces (to match artist names)
        composite_names = re.finditer(r'([A-Z]+[^A-z]+)+|([A-Z0-9][A-z0-9]*([\ ][A-Z0-9][A-z0-9]*)*)', song)
        for name in composite_names:
            name = name.group().strip('., "!?')
            names.append(name)
    return names

def find_nicknames(artist):
    if artist is None:
        return None
    artistID = str(artist['id'])
    artist_path = 'artists/'
    artist_request_uri = base_url + '/' + artist_path + artistID
    artist_request = requests.get(artist_request_uri, headers=headers)
    x = json.loads(artist_request.text)
    # return all nicknames for wanted artist
    return x['response']['artist']['alternate_names']

def create_graph(names, artist):
    connections = {}
    artist_path = 'artists/'

    # loop through list of capitalized words from song and compare with names and nicknames in csv file
    for name in names:
        with open('nicknames2.csv', 'r', encoding='utf-8') as csvfile:
            content = csv.reader(csvfile, delimiter=',')
            for row in content:
                # if name found, update dictionary of connections
                if name in row:
                    mention = row[0].strip()
                    if mention in connections:
                        connections[mention][0] += 1
                    else:
                        connections[mention] = [1]
    for connection in connections:
        connections[connection].append(artist['image_url'])
    return connections

def find_connection(artistName):
    artist = find_artist(artistName)
    songs = find_lyrics(artist)
    return create_graph(clean_lyrics(songs), artist)

if __name__ == '__main__':

    ############# DOWNLOAD NICKNAMES FROM GENIUS API ##############
    # with open('../ArtistCSV/1.csv', 'r', encoding='utf-8') as csvfile:
    #     rr = csv.reader(csvfile)
    #     for row in rr:
    #         nicknames = find_nicknames(find_artist(row))
    #         if nicknames is None:
    #             continue
    #         with open('nicknames2.csv','a', encoding='utf-8') as nf:
    #             wr = csv.writer(nf)
    #             wr.writerow(row + nicknames)

    user_input = input('artist: ').replace(" ", "-")
    print(find_connection(user_input))
