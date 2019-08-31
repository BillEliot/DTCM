from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.contrib.auth.hashers import make_password
import random

# Captcha
def getChar():
    return  chr(random.randint(65,90))
def getColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
def getColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
def genCaptcha():
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    font = ImageFont.truetype('Arial.ttf', 36)
    draw = ImageDraw.Draw(image)
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=getColor())
    captcha = ''
    for t in range(4):
        char=getChar()
        captcha += char
        draw.text((60 * t + 10, 10), char, font=font, fill=getColor2())
    
    encryCaptcha = make_password(captcha, None, 'pbkdf2_sha1')
    image.save('media/captchas/%s.jpg' % encryCaptcha.replace('/', '+'), 'jpeg')

    return encryCaptcha
