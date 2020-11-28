from pyrogram import Client, filters
import os, shutil
from creds import my
from telegraph import upload_file
import logging

logging.basicConfig(level=logging.INFO)


TGraph = Client(
    "Image upload bot",
    bot_token = my.BOT_TOKEN,
    api_id = my.API_ID,
    api_hash = my.API_HASH
)


@TGraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(f"Hello {message.from_user.first_name},\nIm telegram to telegra.ph image uploader bot by @W4RR10R", True)
    
@TGraph.on_message(filters.photo)
async def getimage(client, message):
    tmp = os.path.join("/data",str(message.chat.id))
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    # imgdir = tmp + "/" + str(message.message_id) +".jpg"
    imgdir = os.path.join(tmp, str(message.message_id), '.jpg')
    dwn = await message.reply_text(f"Downloading... {imgdir}", True)          
    await client.download_media(
            message=message,
            file_name=imgdir
        )
    await dwn.edit_text("Uploading...")
    try:
        response = upload_file(imgdir)
    except Exception as error:
        await dwn.edit_text(f"Oops something went wrong\n{error},fl={imgdir}")
        return
    # await dwn.edit_text(f"https://telegra.ph{response[0]}")
    await dwn.edit_text(f"{my.PREFIX}{str(response[0]).replace('/file/','/')}")
    shutil.rmtree(tmp,ignore_errors=True)


TGraph.run()
