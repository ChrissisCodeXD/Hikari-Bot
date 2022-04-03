import os
from io import BytesIO
import urllib.request
import pygifsicle
from PIL import ImageFont, ImageDraw, ImageFilter, ImageSequence, Image
import discord
import requests


async def get_banner(member, guild, background):
    response = requests.get(background)

    background = Image.open(BytesIO(response.content)).convert('RGBA').resize((1024, 500), Image.ANTIALIAS)

    mask = Image.open(f'../data/circle.png').convert('RGBA').resize((250, 250), Image.ANTIALIAS)

    font80 = ImageFont.truetype("./data/arialbd.ttf", 80)
    font40 = ImageFont.truetype("./data/arialbd.ttf", 40)
    font30 = ImageFont.truetype("./data/arialbd.ttf", 30)

    blurred = Image.new('RGBA', background.size)
    draw = ImageDraw.Draw(blurred)
    draw.ellipse((382, 25, 642, 285), fill="#000000")
    draw.text((512, 370), "WELCOME", fill="#000000", font=font80, anchor="ms")
    draw.text((512, 420), str(member).upper(), fill="#000000", font=font40, anchor="ms")
    draw.text((512, 460), f"YOU'RE OUR {guild.member_count}TH MEMBER", fill="#000000", font=font30,
              anchor="ms")
    blurred = blurred.filter(ImageFilter.BoxBlur(5))

    background.paste(blurred, blurred)

    draw = ImageDraw.Draw(background)
    draw.ellipse((382, 25, 642, 285), fill="#FFFFFF", outline="#FFFFFF")
    draw.text((512, 370), "WELCOME", fill="#FFFFFF", font=font80, anchor="ms")
    draw.text((512, 420), str(member).upper(), fill="#FFFFFF", font=font40, anchor="ms")
    draw.text((512, 460), f"YOU'RE OUR {guild.member_count}TH MEMBER", fill="#FFFFFF", font=font30,
              anchor="ms")

    if ".gif" in str(member.display_avatar_url):
        url = member.display_avatar_url
        filename = f"welcome_image_{guild.id}.gif"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        file = open(f'../data/Images/Cache/avatar_{member.id}.gif', "wb")
        file.write(response.content)
        file.close()
        avatar = Image.open(f"../data/Images/Cache/avatar_{member.id}.gif")

        frames = []
        for frame in ImageSequence.Iterator(avatar):
            background = background.copy()

            transparent_avatar = frame.convert('RGBA').resize((250, 250), Image.ANTIALIAS)

            background.paste(transparent_avatar, (387, 30), mask)

            frames.append(background)

        frames[0].save(f"../data/Images/Cache/{filename}", save_all=True, loop=0, append_images=frames[1:])

        try:
            pygifsicle.optimize(f"../data/Images/Cache/{filename}")
        except:
            pass

        avatar.close()

        # try:
        # os.remove(f"../data/Images/Cache/avatar_{member.id}.gif")
        # except:
        # pass

    else:

        filename = f"welcome_image_{guild.id}.png"
        response = requests.get(member.make_avatar_url(size=1024))
        data = BytesIO(response.content)

        avatar = Image.open(data).convert("RGBA")

        new_avatar = avatar.resize((250, 250), Image.ANTIALIAS)

        background.paste(new_avatar, (387, 30), mask)

        background.save(f"../data/Images/Cache/{filename}")

    return f"../data/Images/Cache/{filename}"
