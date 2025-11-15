import os
import re
import json

AUTHORS = ["anonymous", "sigfredo feat. whatware"]

# monkey patch os.system to exit on failure
_original_system = os.system
def safe_system(cmd):
    rc = _original_system(cmd)
    if rc != 0:
        print(f"[ERROR] Command failed ({rc}): {cmd}")
        exit(rc)
    return rc

os.system = safe_system

os.system("rm -rf sprig build node* package-lock.json")

os.system("git clone https://github.com/hackclub/sprig --depth 1 --branch main")

os.mkdir("./build")

os.system("wget https://nodejs.org/dist/v24.11.1/node-v24.11.1-linux-x64.tar.xz && tar -xJf node-v24.11.1-linux-x64.tar.xz && rm node-v24.11.1-linux-x64.tar.xz")
node_bin = "./node-v24.11.1-linux-x64/bin"
os.system(f"{node_bin}/npm install sprig@1.1.3 pngjs@7.0.0")

metadata = {}

for i in os.listdir("./sprig/games"):
    if os.path.isdir(f"./sprig/games/{i}"):
        continue
    with open(f"./sprig/games/{i}", encoding="utf-8", errors="ignore") as gameFile:
        content = gameFile.read()

        titlem = re.search(r"@title\s*[:\-]?\s*(.+?)(?:\s*\*/|\r?\n|$)", content, re.IGNORECASE)
        title = titlem.group(1).strip() if titlem else None
        if title is None: continue

        authorm = re.search(r"@author\s*[:\-]?\s*(.+?)(?:\s*\*/|\r?\n|$)", content, re.IGNORECASE)
        author = authorm.group(1).strip() if authorm else None
        if author is None: continue

        addedOnm = re.search(r"@addedOn\s*[:\-]?\s*(.+?)(?:\s*\*/|\r?\n|$)", content, re.IGNORECASE)
        addedOn = addedOnm.group(1).strip() if addedOnm else None
        if addedOn is None: continue

        descriptionm = re.search(r"@description\s*[:\-]?\s*(.+?)(?:\s*\*/|\r?\n|$)", content, re.IGNORECASE)
        description = descriptionm.group(1).strip() if descriptionm else None
        if description is None: continue

        image = i.replace(".js", ".png")

        if author.lower() in AUTHORS:
            print(f"[INFO]: Including game '{i}' by author '{author}'")
            os.mkdir("./build/games") if not os.path.exists("./build/games") else None
            with open(f"./build/games/{i}", "w", encoding="utf-8") as outFile:
                outFile.write(content)
            if os.path.exists(f"./sprig/games/img/{title}.png"):
                print(f"[INFO]: Copying existing image for game '{i}'")
                with open(f"./sprig/games/img/{title}.png", "rb") as imgFile:
                    imgData = imgFile.read()
                    with open(f"./build/games/{image}", "wb") as outImgFile:
                        outImgFile.write(imgData)
            else:
                print(f"[INFO]: Generating image for game '{i}'")
                os.system(f"GAME={i} {node_bin}/node thumbnail.js")
                        
            metadata[i] = {
                "title": title,
                "author": author,
                "addedOn": addedOn,
                "description": description,
                "image": f"{image}" if os.path.exists(f"./build/games/{image}") else None
            }
            
with open("./build/metadata.json", "w", encoding="utf-8") as metaFile:
    json.dump(metadata, metaFile, indent=4)