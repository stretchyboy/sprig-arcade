import os
import json

os.system("rm -rf build/assets")
os.system("cp -r assets build/assets")

with open('build/metadata.json', 'r',  encoding='utf-8') as file:
    data = json.load(file)

from jinja2 import Environment, FileSystemLoader
env = Environment(loader = FileSystemLoader('templates'))

gallery = env.get_template('gallery.html.j2')
game = env.get_template('game.html.j2')
for gameFilename in data:
    gameName = gameFilename.replace('.js', '')
    outPath = os.path.join('build', 'games', gameName, 'index.html')
    os.makedirs(os.path.dirname(outPath), exist_ok=True)
    print(f'Built page for {gameName} at {outPath}')
    
    render = game.render(slug=gameName, game=data[gameFilename])
    with open(outPath, 'w', encoding='utf-8') as outFile:
        outFile.write(render)

render = gallery.render(games=data)
with open(os.path.join('build', 'index.html'), 'w', encoding='utf-8') as outFile:
    outFile.write(render)
print('Built gallery page at build/index.html')