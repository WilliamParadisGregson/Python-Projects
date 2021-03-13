from gfxhat import lcd,  fonts
from PIL import Image, ImageFont, ImageDraw
from click import getchar

def generateDictionary(theDictionary):
    with open("font3.txt") as font:
        for line in font:
            line = line.replace("\n", "")
            line = line.split(",")
            theDictionary[line[1]] = line[0]


def onPie():
    while True:
        key = getchar()
        lcd.show()
        keys = list(weirdDictionary.keys())
        vals = list(weirdDictionary.values())
        value = vals[keys.index(key)]

        width, height = lcd.dimensions()
        image = Image.new('P', (width, height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(fonts.AmaticSCBold, 20)
        w, h = font.getsize(value)
        draw.text((1, 1), value, 1, font)
        for x1 in range(1, 1 + w):
            for y1 in range(1, 1 + h):
                pixel = image.getpixel((x1, y1))
                lcd.set_pixel(x1, y1, pixel)
        lcd.show()


weirdDictionary = {}
generateDictionary(weirdDictionary)
onPie()
