import { baseEngine, palette } from "sprig/base";
import fs from "fs";
import { PNG } from "pngjs";

const evalGameScript = (script) => {
  const { api } = baseEngine();

  let legend = [];
  let map = null;
  let background = ".";

  const patchedApi = {
    ...api,
    setLegend: (...bitmaps) => {
      legend = bitmaps;
    },
    setBackground: (bg) => {
      background = bg;
    },
    setMap: (string) => {
      map = string;
    },
    onInput: () => {},
    afterInput: () => {},
    playTune: () => {},
    setTimeout: () => {},
    setInterval: () => {},
  };

  try {
    const fn = new Function(...Object.keys(patchedApi), script);
    fn(...Object.values(patchedApi));
  } catch (err) {}

  return {
    legend: Object.fromEntries(legend),
    map: map,
    background,
  };
};

const makeSpriteBitmap = (grid) => {
  const result = [];
  const colors = Object.fromEntries(palette);
  grid
    .trim()
    .split("\n")
    .forEach((row) => {
      row
        .trim()
        .split("")
        .forEach((color) => {
          const arr = colors[color];
          result.push(...arr);
        });
    });
  return result;
};

const blitSprite = (data, width, bitmap, tx, ty) => {
  for (let x = 0; x < 16; x++)
    for (let y = 0; y < 16; y++) {
      const sx = tx * 16 + x;
      const sy = ty * 16 + y;

      if (bitmap[(y * 16 + x) * 4 + 3] < 255) continue;

      data[(sy * width + sx) * 4 + 0] = bitmap[(y * 16 + x) * 4 + 0];
      data[(sy * width + sx) * 4 + 1] = bitmap[(y * 16 + x) * 4 + 1];
      data[(sy * width + sx) * 4 + 2] = bitmap[(y * 16 + x) * 4 + 2];
      data[(sy * width + sx) * 4 + 3] = bitmap[(y * 16 + x) * 4 + 3];
    }
};

const drawGameImage = (src) => {
  const { legend, map, background } = evalGameScript(src);
  if (!map) {
    throw new Error("No map found");
  }

  const mapWidth = map.trim().split("\n")[0].trim().length;
  const mapHeight = map.trim().split("\n").length;

  const data = new Uint8Array(mapWidth * mapHeight * 16 * 16 * 4);
  map
    .trim()
    .split("\n")
    .forEach((row, y) => {
      row
        .trim()
        .split("")
        .forEach((sprite, x) => {
          if (background !== ".") {
            blitSprite(
              data,
              mapWidth * 16,
              makeSpriteBitmap(legend[background]),
              x,
              y,
            );
          }
          if (sprite === ".") return;
          blitSprite(
            data,
            mapWidth * 16,
            makeSpriteBitmap(legend[sprite]),
            x,
            y,
          );
        });
    });

  return { data, width: mapWidth * 16, height: mapHeight * 16 };
};

function saveAsPNG(path, width, height, data) {
  const png = new PNG({ width, height });
  png.data = Buffer.from(data);
  png.pack().pipe(fs.createWriteStream(path));
}

const generateImage = async (name) => {
  let imgFilePath = `./build/games/${name}.png`;
  let gameContentString = loadGameContentFromDisk(name);
  let gameImage = checkImgExists(name);
  if (gameImage) return;

  try {
    const { data, width, height } = drawGameImage(gameContentString);
    saveAsPNG(imgFilePath, width, height, data);
  } catch (error) {
    console.error(error);
    const image = await fetch(
      "https://cloud-i203j2e6a-hack-club-bot.vercel.app/1confused_dinosaur.png",
    );
    fs.writeFileSync(imgFilePath, Buffer.from(await image.arrayBuffer()));
  }
};

function checkImgExists(name) {
  let imgPath = `./build/games/${name}.png`;
  return fs.existsSync(imgPath);
}

function loadGameContentFromDisk(name) {
  let gameContentPath = `./build/games/${name}.js`;
  if (!fs.existsSync(gameContentPath)) return null;
  return fs.readFileSync(gameContentPath).toString();
}

generateImage(process.env.GAME.replace(".js", ""));
console.log(`[SUCCESS] Generated image for ${process.env.GAME}`);
