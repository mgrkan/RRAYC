from PIL import Image, ImageDraw, ImageFont
import pathlib
import textwrap
import os
from conf import RESOURCES, SAMPLE_INPUTS
reddit_ss = "comment"
post = "post"
upImage = pathlib.Path(RESOURCES + "/images/upvoteIcon.png")
watermark = pathlib.Path(RESOURCES + "/images/bg_watermark.png")
font = RESOURCES + "/fonts/verdana.ttf"

def createSS(text, upimg, downimg, author):
    text_str = "".join(text)
    wrapped = textwrap.fill(text= text_str, width= 100)
    up = Image.open(upimg)
    down = Image.open(downimg)
    img = Image.new('RGB', (1920, 1080), color = 'rgb(26, 26, 27)')
    wm = Image.open(watermark)
    img.paste(wm, (0, 0))
    fnt = ImageFont.truetype(font, 24)
    d = ImageDraw.Draw(img)
    d.multiline_text((350, 320), wrapped, fill=(255,255,255), font=fnt )
    d.text((350, 262), "Posted by u/{}".format(author), fill=(128,128,128), font=fnt )
    img.paste(up, (270, 262))
    img.paste(down, (270, 320))
    mkdir = pathlib.Path(SAMPLE_INPUTS + '/imgs/' + reddit_ss)
    os.mkdir(mkdir)
    imgdir = pathlib.Path(SAMPLE_INPUTS + '/imgs/' + reddit_ss + "/" + reddit_ss + '.png')
    img.save(imgdir)

def createPostSS(text, subName, subIcon, upimg, downimg, upvotes, author):
    text_str = "".join(text)
    wrapped = textwrap.fill(text= text_str, width= 100)
    up = Image.open(upimg)
    down = Image.open(downimg)
    icon = Image.open(subIcon)
    img = Image.new('RGB', (1920, 1080), color = 'rgb(26, 26, 27)')
    wm = Image.open(watermark)
    img.paste(wm, (0, 0))
    fnt = ImageFont.truetype(font, size=24)
    upvote_font = ImageFont.truetype(font, size=15)
    d = ImageDraw.Draw(img)
    d.multiline_text((350, 320), wrapped, fill=(255,255,255), font=fnt )
    img.paste(up, (270, 262))
    img.paste(down, (270, 330))
    img.paste(icon, (350, 262))
    
    d.text((410, 269), "r/{}".format(subName), fill=(255, 255, 255), font=fnt)
    d.text((280, 310), upvotes, fill=(255, 255, 255), font=upvote_font)
    d.text((560, 269), "· Posted by u/{}".format(author), fill=(128,128,128), font=fnt )
    mkdir = pathlib.Path(SAMPLE_INPUTS + '/imgs/1' + post)
    os.mkdir(mkdir)
    imgdir = pathlib.Path(SAMPLE_INPUTS + '/imgs/1' + post + "/" + "1" + post + '.png')
    img.save(imgdir)
