from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from config import BOT_TOKEN, SUDO_USERS
from pathlib import Path
from fileinput import input
from PIL import Image
import math

# ?

def convert(source):
    des = source.with_suffix(".webp")
    image = Image.open(source)
    image.save(des, format="webp")
    return des   

def resize(kangsticker):
     im = Image.open(kangsticker)
     maxsize = (512, 512)
     if (im.width and im.height) < 512:
         size1 = im.width
         size2 = im.height
         if im.width > im.height:
             scale = 512 / size1
             size1new = 512
             size2new = size2 * scale
         else:
             scale = 512 / size2
             size1new = size1 * scale
             size2new = 512
         size1new = math.floor(size1new)
         size2new = math.floor(size2new)
         sizenew = (size1new, size2new)
         im = im.resize(sizenew)
     else:
         im.thumbnail(maxsize)
     im.save(kangsticker, "PNG")

async def start(u: Update, c: CallbackContext):
    await u.message.reply_text(f"Hello ! {u.effective_user.first_name}, Am sticker bot of Spoiled Network, only Sudos can use me !")

YashuAlpha_oP = True

async def kang(u: Update, c: CallbackContext):
    m = u.effective_message
    user = u.effective_user
    if not user.id in SUDO_USERS:
        return
    text = c.args
    if len(text) < 2:
        return await m.reply_text("/hkang [emoji] [packnum] [packname]")
    emoji = text[0]
    pack = text[1]
    title = text[2:] if len(text) > 2 else None
    if title:
        tot = ""
        for spl in title:
            tot += spl + " "
        title = tot
    if not m.reply_to_message:
        return await m.reply_text("BRUH ! 🥲🥲\n\nReply to sticker or a photo!")
    if not m.reply_to_message.sticker and not m.reply_to_message.photo:
        return await m.reply_text("BRUH ! 🥲🥲\n\nReply to sticker or a photo!")  
    if m.reply_to_message.photo:
        file_id = m.reply_to_message.photo[-1].file_id
        get_file = await c.bot.get_file(file_id)
        await get_file.download("yashu.png")
        resize("yashu.png")
        x = "yashu.png"
        format = "normal"
        png = True
    else:
        png = False
        type = m.reply_to_message.sticker
        if type.is_video:
            format = "video"
        elif type.is_animated:
            format = "animated"
        else:
            format = "normal"
        sticid = type.file_id
        if format == "video":
            get_file = await c.bot.get_file(sticid)
            x = await get_file.download()
        elif format == "animated":
            get_file = await c.bot.get_file(sticid)
            x = await get_file.download()
    pack_name = f"Hades_of_{user.id}_{format}_{pack}_by_{c.bot.username}"
    try:
        await c.bot.get_sticker_set(pack_name)
        if format == "video":
            await c.bot.add_sticker_to_set(user_id=user.id, name=pack_name, emojis=emoji, webm_sticker=open(x, "rb"))
        elif format == "animated":
            await c.bot.add_sticker_to_set(user_id=user.id, name=pack_name, emojis=emoji, tgs_sticker=open(x, "rb"))
        else:
            await c.bot.add_sticker_to_set(user_id=user.id, name=pack_name, emojis=emoji, png_sticker=open(x, "rb") if png else sticid)
        edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{pack_name}"
                            )
                        ]
                    ]
                )
        return await m.reply_text(f"Sticker is added !\n\nEmoji : {emoji}", reply_markup=edited_keyboard)
    except:
        if not title:
            return await m.reply_text("/hkang [emoji] [packnum] [packname]")
        if format == "video":
            await c.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, webm_sticker=open(x, "rb"))
        elif format == "animated":
            await c.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, tgs_sticker=open(x, "rb"))
        else:
            await c.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, png_sticker=open(x, "rb") if png else sticid)
        await m.reply_text("your new pack is created with name" + " " + title)
        edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{pack_name}"
                            )
                        ]
                    ]
                )
        return await m.reply_text(f"Sticker is added !\n\nEmoji : {emoji}", reply_markup=edited_keyboard)

async def del_sticker(u: Update, c: CallbackContext):
    m = u.effective_message
    user = u.effective_user
    if not user.id in SUDO_USERS:
        return
    if not m.reply_to_message:
        return await m.reply_text("reply to a stixker vruh! ")
    if not m.reply_to_message.sticker:
        return await m.reply_text("reply to a stixker vruh! ")
    try:
        sn = m.reply_to_message.sticker.set_name
        sn = sn.split("_")
        ind = sn.index("of")
        ind = ind + 1
        ind = sn[ind]
        if user.id != int(ind):
            return await m.reply_text("You can't delete this sticker !")
    except:
        return await m.reply_text("You can't delete this sticker !")
    try:
        await c.bot.delete_sticker_from_set(m.reply_to_message.sticker.file_id)
        await m.reply_text("deleted !")
    except Exception as e:
        await m.reply_text(f"can't delete.. \n\n{e}")

async def get_pack(u: Update, c: CallbackContext):
    m = u.effective_message
    user = u.effective_user
    if not user.id in SUDO_USERS:
        return
    text = c.args
    if len(text) != 2:
        return await m.reply_text("/getpack [format] [packnum]")
    pack_name = f"Hades_of_{user.id}_{text[0]}_{text[1]}_by_{c.bot.username}"
    edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{pack_name}"
                            )
                        ]
                    ]
                )
    await m.reply_text(f"your pack is here !", reply_markup=edited_keyboard)

async def img_resizer(u: Update, c: CallbackContext):
    m = u.effective_message
    if m.reply_to_message:
        if m.reply_to_message.photo:
            file = m.reply_to_message.photo[-1].file_id
            get = await c.bot.get_file(file)
            await get.download("alpha.png")
            i = Image.open("alpha.png")
            i = i.resize((100, 100))
            i.save("alpha.png", "PNG")
            await m.reply_document(open("alpha.png", "rb"))

usage = "/splkang [emoji] [packnum] [packname]\n\n/splkang [packnum] [packname]\n\nNote : if emoji is not provided, sticker will be added as their corresponding emoji !"

async def copy_pack(u: Update, c: CallbackContext):
    m = u.effective_message
    user = u.effective_user
    if not user.id in SUDO_USERS:
        return
    if not m.reply_to_message:
        return await m.reply_text("BRUH ! 🥲🥲\n\nReply to sticker !")
    if not m.reply_to_message.sticker:
        return await m.reply_text("BRUH ! 🥲🥲\n\nReply to sticker !")  
    args = c.args
    if len(args) < 2:
        return await m.reply_text(usage)
    if len(args) > 1:
        try:
            emoji = args[0]
            packnum = int(args[1])
            title = args[2:]
        except:
            try:
                emoji = None
                packnum = int(args[0])
                title = args[1:]
            except:
                return await m.reply_text(usage)
    if title:
        tot = ""
        for spli in title:
            tot += spli + " "
        title = tot
    type = m.reply_to_message.sticker
    if type.is_video:
        format = "video"
    elif type.is_animated:
        format = "animated"
    else:
        format = "normal"
    pack_name = f"Hades_of_{user.id}_{format}_{packnum}_by_{c.bot.username}"
    try:
        x = await c.bot.get_sticker_set(pack_name)
        return await m.reply_text("Pack already exists with this number !")
    except:
        stic_list = (await c.bot.get_sticker_set(type.set_name)).stickers
        numb = len(stic_list)
        ok = await m.reply_text(f"{len(stic_list)} Stickers found, creating pack...")
        sticid = stic_list[0].file_id
        get_file = await c.bot.get_file(sticid)
        x = await get_file.download()
        if not emoji:
            emoji = stic_list[0].emoji
        if format == "video":
            await c.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, webm_sticker=open(x, "rb"))
        elif format == "animated":
            await c.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, tgs_sticker=open(x, "rb"))
        else:
            await c.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, png_sticker=open(x, "rb")) 
        not_ok = await m.reply_text("Pack created, adding stickers...")
        await ok.delete()
        stic_list.remove(stic_list[0])
        a = 0
        suk = 0
        for stic in stic_list:
            sticid = stic.file_id
            get_file = await c.bot.get_file(sticid)
            x = await get_file.download()
            if not emoji:
                emoji = stic.emoji
            if format == "video":
                await c.bot.add_sticker_to_set(user_id=user.id, name=pack_name, emojis=emoji, webm_sticker=open(x, "rb"))
            elif format == "animated":
                await c.bot.add_sticker_to_set(user_id=user.id, name=pack_name, emojis=emoji, tgs_sticker=open(x, "rb"))
            else:
                await c.bot.add_sticker_to_set(user_id=user.id, name=pack_name, emojis=emoji, png_sticker=open(x, "rb"))
            a += 1
            if suk == 5:
                try: 
                    id = not_ok.message_id
                    await c.bot.edit_message_text(chat_id=m.chat.id, message_id=id, f"Progress : {a} / {len(stic_list)}")
                    suk = 0
                except:
                    pass
        await not_ok.delete()
        edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{pack_name}"
                            )
                        ]
                    ]
                )
        await m.reply_text(f"your pack is here !", reply_markup=edited_keyboard)


def x():
    Yashu = ApplicationBuilder().token(BOT_TOKEN).build()
    Yashu.add_handler(CommandHandler("hkang", kang))
    Yashu.add_handler(CommandHandler("dsticker", del_sticker))
    Yashu.add_handler(CommandHandler("getpack", get_pack))
    Yashu.add_handler(CommandHandler("start", start))
    Yashu.add_handler(CommandHandler("resize", img_resizer))
    Yashu.add_handler(CommandHandler("splkang", copy_pack))
    print("Asyncio bot started !\nYashuAlpha ✨💭❤️")
    Yashu.run_polling()

#loop.run_until_complete(x())

x()

