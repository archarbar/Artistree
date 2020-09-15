# Artistree

## About
Music is an international language that everyone can experience and enjoy. Artistree is all about music's astonishingly intertwined world. Whether it be a feature on a song, a shout out, or even a diss track resulting from a feud, Artistree has got you covered. Every time an artist mentions another artist in one of their songs, Artistry will analyse the lyrics from that Artist and when it finds another artist, it will graph that relation. This way, it is incredibly easy to visualize and picture connexions between Artists, through their lyrics. In other words, it will show a tree graph of different artists, hence "artist"+"tree"="artistree". Going through all of an artist's songs and lyrics allows us to piece this complicated puzzle together and present it in a fashionable manner. We can also see how much contact and influence an artist has over another and has in general. These artists show us that music is not a solitary adventure.

## How To Use It?
Simple head to [the website](http://mathusan.ca/) and enter your favorite artist. Have fun checking out all their connections to other artists!

## How Was It Made?
The background Image for the website and the logo were all made by us using Adobe Photoshop.

On Friday (11th september 2020), we were still debating on what to make for the PennApps XXI Music Hackathon since we didn't have any good ideas. That's when Victor had the idea of making a website that shows connexions between artists through their lyrics. We all loved it, since we are avid fans of Hip Hop and a lot of rappers mention other rappers in their songs.

We used bootstrap and what we know of CSS and HTML to make the submit page in about 2 hours on Saturday Morning. Then, the form sends a POST request to a PHP file which would take the submitted artist's name and run a python file with the artist as an argument. Then the output of that python file would be saved in the original PHP file which would relay the output to javascript which will finally modify an HTML element to display the data.

We used the Genius API to find lyrics of artists and images of artists. We used the "10,000 MTV's Top Music Artists" dataset to filter out the lyrics and find actual Artist names. We added numerous steps in the python script to filter out useless words and to also check for artist's names with multiple components. There were a lot of edge cases.

Since the JSON data sent by the Python script couldn't be used with d3.js (data visualization library), we had to transform the data into a javascript Object, read it and then create another appropriate javascript Object that d3.js could read. For d3.js to work, we had to do numerous tweaks and fixes to the Object and it still wouldn't work for 2-3 hours. Meanwhile, we were also trying to make the website using Heroku and a Flask backend in case this LAMP-stack version with d3.js wouldn't work. We spent hours reading the documentation for d3.js and finally found multiple solutions to our several problems in the span of 3 hours and fixed it. Since this version was better than the flask version, we decided to use this for the Hackathon. We did an all-nighter and finished everything including the logo at around 6:00 AM on Sunday (13th september 2020).

## Made By
Mathusan Chandramohan, Victor Zhong, Kleard Mama, Sangwoo Han
