import requests
import json
from bs4 import BeautifulSoup
import re

genius_client_id = 'cSHZqVRH60I9GqbgI-EMEeCGm6EZD0hhiIcffqXCyGHWqzQ0nLJQarDscUhH3_HJ'
genius_secret_id = 'bJtcQAhAyV5yDBgqakLtYL0UJLD8UlfT7hrxLBMsvSEWOnPWcoSYpEcd3uhYi4QS9swjGDht4B3-nwEB-cVhjQ'
genius_client_access_token = 'DYw7-Hc_XXs6sv_Gao4xZAO0QwVwW9VS9Etjh35_C6Nbpn9964VAUtQlVRjpWP2j'
base_url = 'https://api.genius.com'

# use beautiful soup to extract lyrics from html page
def find_lyrics(url):
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
    return lyrics.strip("\n")

user_input = input('artist: ').replace(" ", "-")

path = 'search/'
request_uri = '/'.join([base_url, path])
print(request_uri + user_input)

params = {'q': user_input}

token = 'Bearer {}'.format(genius_client_access_token)
headers = {'Authorization': token}

r = requests.get(request_uri, params=params, headers=headers)
# print(r.text)

#link for most popular song for artist
y = json.loads(r.text)
URL = y['response']['hits'][0]['result']['url']
print(URL)

print(find_lyrics(URL))