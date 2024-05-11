#(©)CodeXBotz





from pyrogram import Client, filters
from datetime import datetime, timedelta
import re,random,requests
#from pyrogra.types import ReplyKeyboardMarkup
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


import os,requests
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


async def is_token_valid(mid, token):

    tstr=datetime.now()
    ox=open(f"verify.txt",'r')
    prt= ox.read().splitlines()
    ox.close()
    os.system(f"sed -i '/{token}/d' verify.txt")
    if token in prt:
        result=datetime.now() + timedelta(hours=24)
        print(result)
        os.system(f'echo "{result.strftime("%Y:%m:%d:%H:%M")}" > {mid}.txt')
        return True
    else:
        return False



async def time_checker(yearx,monthx,dayx,hourx,mintx):

    tchk=datetime.now()
    y=tchk.strftime("%Y")
    m=tchk.strftime("%m")
    d=tchk.strftime("%d")
    h=tchk.strftime("%H")
    mi=tchk.strftime("%M")
    kk=datetime(int(y),int(m),int(d),int(h),int(mi))
    ik=datetime(int(yearx),int(monthx),int(dayx),int(hourx), int(mintx))
    if ik > kk:
        return True





@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    vfy=False
    id = message.from_user.id
    try:
        o=open(f'{id}.txt','r')
        s=o.read().split(":")
        o.close()
        vfy=await time_checker(s[0],s[1],s[2],s[3],s[4])
    except:
        pass
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    if "verify_" in message.text:
        _, token = message.text.split("_", 1)
        vfy=await is_token_valid(id,token)
        if vfy:
            return await message.reply("✅ Your token successfully verified and valid for: 24 Hour")
        else :
            return await message.reply("Your token is invalid or Expired. Try again by clickking /start")
    text = message.text
    if len(text)>7 and vfy:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    elif vfy :
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
    else:
        import string,json
        token=  ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        uc=f'https://telegram.me/video_corn_bot?start=verify_{token}'
        shor = f'https://inshorturl.com/api?api=14693d406d11d167bf57232fa66034268f203141&url={uc}'
        response = requests.get(shor, headers={'Connection': 'close'})
        js = json.loads(response.content)
        urlx = js['shortenedUrl']


        btn = [
                    [InlineKeyboardButton("Click here take token", url=urlx)],
                    [InlineKeyboardButton('>> HOW TO TAKE FREE TOKEN Tutorial ', url='https://t.me/japanese_live_actionz/31') ]
                ]
        await message.reply_text('Your Ads token is expired, refresh your token and try again.\n\nToken Timeout: 24 hours \nWhat is the token?\n\nThis is an ads token. If you pass 1 ad, you can use the bot for 24 Hour after passing the ad.' ,reply_markup=InlineKeyboardMarkup(btn))

        tym=datetime.now()
        os.system(f'echo "{token}" >> verify.txt')


    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "Join Channel",
                url = client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'CLICK HERE TO GET',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
