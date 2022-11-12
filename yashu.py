from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from config import BOT_TOKEN, SUDO_USERS
from pathlib import Path
from fileinput import input

async def start(u: Update, c: CallbackContext):
    await u.message.reply_text(f"Hello ! {u.effective_user.mention_html()}, Am kang bot of Hades Network, only Sudos can use me !")

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
        return await m.reply_text("BRUH ! 🥲🥲\n\nReply to sticker !")
    if not m.reply_to_message.sticker:
        return await m.reply_text("BRUH ! 🥲🥲\n\nReply to sticker !")  
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
        await get_file.download("lmao.webm")
    elif format == "animated":
        get_file = await c.bot.get_file(sticid)
        x = await get_file.download()
    pack_name = f"Hades_of_{user.id}_{format}_{pack}_by_{c.bot.username}"
    try:
        await c.bot.get_sticker_set(pack_name)
        if format == "video":
            await c.bot.add_sticker_to_set(user_id=user.id, name=pack_name, emojis=emoji, webm_sticker=input("lmao.webm"))
        elif format == "animated":
            await c.bot.add_sticker_to_set(user_id=user.id, name=pack_name, emojis=emoji, tgs_sticker=open(x, "rb"))
        else:
            await c.bot.add_sticker_to_set(user_id=user.id, name=pack_name, emojis=emoji, png_sticker=sticid)
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
        await m.reply_text("your new pack is created with name" + " " + title)
        if format == "video":
            await c.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, webm_sticker=input("lmao.webm"))
        elif format == "animated":
            await c.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, tgs_sticker=open(x, "rb"))
        else:
            await c.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, png_sticker=sticid)
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
    if not m.reply_to_message.sticker:
        return await m.reply_text("reply to a stixker vruh! ")
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
    await m.reply_text(f"your pack is [here](t.me/addstickers/{pack_name})")

def Asynchorous():
    print("Asyncio bot started !\nYashuAlpha ✨💭❤️")
    Yashu = ApplicationBuilder().token(BOT_TOKEN).build()
    Yashu.add_handler(CommandHandler("hkang", kang))
    Yashu.add_handler(CommandHandler("dsticker", del_sticker))
    Yashu.add_handler(CommandHandler("getpack", get_pack))
    Yashu.add_handler(CommandHandler("start", start))

    Yashu.run_polling()

if YashuAlpha_oP:
    Asynchorous()
