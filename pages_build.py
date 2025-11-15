# builds the pages after the first part of build.py has run.
# TODO : Isa get templates setup 
# templates/gallery.html.j2 #put the gallery html you have in here
# templates/game.html.j2 # put the game page code in here
# existing assests to go in the css amd scripts to copy into build later

# The following TODO items are straight out of the diagram


import os
import json

os.system("cp -r css build/css")

with open('build/metadata.json', 'r',  encoding='utf-8') as file:
    data = json.load(file)

from jinja2 import Environment, FileSystemLoader
env = Environment(loader = FileSystemLoader('templates'))


gallerytemp = env.get_template('gallery.html.j2')
gametemp = env.get_template('game.html.j2')
for gameFilename in data:
    gameName = gameFilename.replace('.js', '')
    outpath = os.path.join('build', 'games', gameName, 'index.html')
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    print(f'Built page for {gameName} at {outpath}')
    
    rendr = gametemp.render(slug=gameName, game=data[gameFilename])
    with open(outpath, 'w', encoding='utf-8') as outfile:
        outfile.write(rendr)






galleryhtml = gallerytemp.render(games=data)
with open(os.path.join('build', 'index.html'), 'w', encoding='utf-8') as outfile:
    outfile.write(galleryhtml)

    

