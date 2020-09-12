import requests
import json
from bs4 import BeautifulSoup
import re

genius_client_id = 'cSHZqVRH60I9GqbgI-EMEeCGm6EZD0hhiIcffqXCyGHWqzQ0nLJQarDscUhH3_HJ'
genius_secret_id = 'bJtcQAhAyV5yDBgqakLtYL0UJLD8UlfT7hrxLBMsvSEWOnPWcoSYpEcd3uhYi4QS9swjGDht4B3-nwEB-cVhjQ'
genius_client_access_token = 'DYw7-Hc_XXs6sv_Gao4xZAO0QwVwW9VS9Etjh35_C6Nbpn9964VAUtQlVRjpWP2j'
base_url = 'https://api.genius.com'

# use beautiful soup to extract lyrics from html page
def find_lyrics(songs):
    song_lyrics = []
    for url in songs:
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

def __getURL(artistName):
    song_urls = []
    song_path = 'search/'
    song_request_uri = '/'.join([base_url, song_path])

    params = {'q': user_input}

    token = 'Bearer {}'.format(genius_client_access_token)
    headers = {'Authorization': token}

    song_request = requests.get(song_request_uri, params=params, headers=headers)
    # print(r.text)

    #link for most popular song for artist
    y = json.loads(song_request.text)
    artist_id = y['response']['hits'][0]['result']['primary_artist']['id']

    artist_path = 'artists/'
    artist_request_uri = base_url + '/' + artist_path + str(artist_id) + '/songs?sort=popularity&per_page=30'
    artist_request = requests.get(artist_request_uri, params=params, headers=headers)

    z = json.loads(artist_request.text)
    for song in z['response']['songs']:
        url = ''.join(['https://genius.com', song['path']])
        song_urls.append(url)
    return song_urls

def clean_lyrics(lyrics):
    names = []
    # names = re.findall(r'[A-Z][A-z]*', lyrics)
    # composite_names = re.findall(r'[A-Z0-9][A-z0-9]*[\ ][A-Z0-9][A-z0-9]*', lyrics)
    composite_names = re.finditer(r'[A-Z0-9][A-z0-9]*([\ ][A-Z0-9][A-z0-9]*)*', lyrics)
    for name in composite_names:
        names.append(name.group())
    return names

if __name__ == '__main__':
    user_input = input('artist: ').replace(" ", "-")
    print(clean_lyrics(find_lyrics(__getURL(user_input))[0]))
