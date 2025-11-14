# Sprig Arcade

First set of issues are over here https://github.com/UTCSheffield/sprig-arcade-fork/issues

We are now going to build in python & jinja with an aim to build on github pages.

## General Idea

```mermaid
block-beta
columns 3
  block:git
  columns 1
    sprig[("https://github.com/hackclub/sprig")]
    clone[["Clone / pull main"]]
    sprig --> clone
  end
  block:builddata
  columns 1
    games[/"list = Read games.txt"/]
    loop[["For each game in /js/games/*.js"]]
    read[["game = Parse metadata"]]
    check{"Is game in list?"}
    gamejs[\"Copy game js to /build/games "\]
    imagejs[\"Copy game thumbnail to /build/games "\]
    append{{"append game to metadata"}}
    write[\"Write metadata.json"\]
    games --> loop
    loop --> read
    read --> check
    check -- "Yes" --> gamejs
    gamejs --> append
    append --> write
  end
  block:buildpages
    columns 1
    data[/"data = read metadata.json"/]
    space
    gamet[["load game page template"]]
    space
    loop2[["Foreach game in data"]]
    
    space
    filepath[["filepath ='/build/games/{game}/index.html'"]]
    space
    gamepage[\"Render game page to filepath"\]
    space
    galleryt[["load gallery page template"]]
    space
    index[\"Render gallery page to index.html file in /build "\]
    
    data --> gamet
    gamet --> loop2
    loop2 --> filepath
    filepath --> gamepage
    gamepage --> galleryt
    galleryt --> index
  end

clone --> games
write --> data

style builddata fill:#EFE
style buildpages fill:#EEF


```

