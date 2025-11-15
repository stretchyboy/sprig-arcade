from jinja2 import Environment, FileSystemLoader
from types import SimpleNamespace
import os
import re

# @section: monkey patch
_original_system = os.system
def safe_system(cmd):
    rc = _original_system(cmd)
    if rc != 0:
        print(f"[ERROR] Command failed ({rc}): {cmd}")
        exit(rc)
    return rc
os.system = safe_system
# @endsection monkey patch

# @section: cleanup
os.system("rm -rf sprig")
os.system("rm -rf build")
os.system("rm -rf node-v24.11.1-linux-x64")
os.system("rm -rf package-lock.json")
# @endsection cleanup

# @section: setup
AUTHORS = ["anonymous", "sigfredo feat. whatware"]

os.mkdir("./build")
os.mkdir("./build/games")
os.mkdir("./build/assets")
os.system("git clone https://github.com/hackclub/sprig --depth 1 --branch main")

games = {}

env = Environment(loader = FileSystemLoader('templates'))

templates = SimpleNamespace()
templates.gallery = env.get_template('gallery.html.j2')
templates.game = env.get_template('game.html.j2')
# @endsection setup

# @section: node
os.system("wget -q https://nodejs.org/dist/v24.11.1/node-v24.11.1-linux-x64.tar.xz")
os.system("tar -xJf node-v24.11.1-linux-x64.tar.xz")
os.system("rm node-v24.11.1-linux-x64.tar.xz")
node_bin = "./node-v24.11.1-linux-x64/bin"
os.system(f"{node_bin}/npm install")
# @endsection node

# @section: process games
for game in os.listdir("./sprig/games"):
    if os.path.isdir(f"./sprig/games/{game}"):
        continue
    with open(f"./sprig/games/{game}", encoding="utf-8", errors="ignore") as gameFile:
        content = gameFile.read()
        gameNoExt = game.replace(".js", "")

        # @section: extract metadata
        try:
            title = re.search(r"@title:\s(.*)", content, re.IGNORECASE).group(1).strip()
            if title is None: continue

            author = re.search(r"@author:\s(.*)", content, re.IGNORECASE).group(1).strip()
            if author is None: continue

            description = re.search(r"@description:\s(.*)", content, re.IGNORECASE).group(1).strip()
            if description is None: continue
        except:
            continue
        # @endsection extract metadata

        # @section: filter by author
        if author.lower() in AUTHORS:
            print(f"[INFO]: Including game '{game}' by author '{author}'")
            
            with open(f"./build/games/{game}", "w", encoding="utf-8") as outFile:
                outFile.write(content)
        else:
            continue
        # @endsection filter by author
        
        # @section: create or copy image
        if os.path.exists(f"./sprig/games/img/{title}.png"):
            print(f"[INFO]: Copying existing image for game '{game}'")
            os.system(f"cp ./sprig/games/img/{title}.png ./build/games/{gameNoExt}.png")
        else:
            print(f"[INFO]: Generating image for game '{title} ({game})'")
            os.system(f"GAME={game} {node_bin}/node thumbnail.js")
        # @endsection create or copy image
        
        # @section: add game metadata
        games[gameNoExt] = {
            "title": title,
            "author": author,
            "description": description
        }
        # @endsection add game metadata

        # @section: render game page
        outPath = os.path.join('build', 'games', gameNoExt, 'index.html')
        os.makedirs(os.path.dirname(outPath), exist_ok=True)
        render = templates.game.render(slug=gameNoExt, game=games[gameNoExt])
        with open(outPath, 'w', encoding='utf-8') as outFile:
            outFile.write(render)
        # @endsection render game page

        print(f'[SUCCESS] Built page for {game}')
# @endsection process games

# @section: render gallery
render = templates.gallery.render(games=games)
with open(os.path.join('build', 'index.html'), 'w', encoding='utf-8') as outFile:
    outFile.write(render)

print('[SUCCESS] Built gallery page at build/index.html')
# @endsection render gallery

# @section: final cleanup
os.system("rm -rf sprig")
os.system("rm -rf node-v24.11.1-linux-x64")
os.system("rm -rf package-lock.json")
# @endsection final cleanup