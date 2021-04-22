from PIL import Image, ImageDraw, ImageFont
import pathlib
from conf import RESOURCES, SAMPLE_INPUTS
import textwrap
import os
import random

watermark = pathlib.Path(RESOURCES + "/images/thumbbg.png") #BACKGROUND IMAGE WITH WATERMARK
font =  RESOURCES + "/fonts/BabySchoolItalic.ttf"
font2 = RESOURCES + "/fonts/MilkyNice.ttf"


def createThumb(text, imgName, avatar):
    trvalue = random.randint(0,255) #TITLE COLOR RED VALUE
    tgvalue = random.randint(0,255) #TITLE COLOR GREEN VALUE
    tbvalue = random.randint(0,255) #TITLE COLOR BLUE VALUE
    print("Title rgb values: ", trvalue, tgvalue, tbvalue)
    arvalue = random.randint(0,255) #ASKREDDIT COLOR RED VALUE
    agvalue = random.randint(0,255) #ASKREDDIT COLOR GREEN VALUE
    abvalue = random.randint(0,255) #ASKREDDIT COLOR BLUE VALUE
    print("Title rgb values: ", arvalue, agvalue, abvalue)
    text_str = "".join(text)
    wrapped = textwrap.fill(text= text_str, width= 20)
    img = Image.new('RGB', (1920, 1080), color = 'rgb(26, 26, 27)')
    wm = Image.open(watermark)
    img.paste(wm, (0, 0))
    avatar = Image.open(avatar)
    avatar = avatar.resize((600, 600)) #DEFAULT IS 256x256 WHICH IS TOO SMALL
    try:
        img.paste(avatar, (1920 - 600, 1080 - 600), mask=avatar ) #TO FILTER OUT CUSTOM PROFILE PICTURES. ONLY NEW SNOO AVATARS ARE TRANSPARENT
    except:
        pass
    fnt = ImageFont.truetype(font, 150)
    fnt2 = ImageFont.truetype(font2, 100)
    d = ImageDraw.Draw(img)
    d.multiline_text((90, 300), wrapped, fill=(trvalue,tgvalue,tbvalue), font=fnt ) #RANDOM COLORS FOR THUMBNAIL
    d.text((100, 80), "r/AskReddit", fill=(arvalue,agvalue,abvalue), font=fnt2 )
    imgdir = SAMPLE_INPUTS + "/thumbnail/" + imgName + ".png"
    img.save(imgdir)