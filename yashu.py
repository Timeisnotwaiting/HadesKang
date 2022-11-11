from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config import BOT_TOKEN, SUDO_USERS

async def start(u: Update, c: CallbackContext):
    await u.message.reply_text(f"Hello ! {u.effective_user.mention_html()}, Am kang bot of Hades Network, only Sudos can use me !")

ALPHA = False

ARGS = None

ENTERED = False

async def kang(u: Update, c: CallbackContext):
    global ALPHA
    global ARGS
    global ENTERED
    m = u.effective_message
    user = u.effective_user
    if not user.id in SUDO_USERS:
        return
    text = c.args
    if len(text) != 2:
        return await m.reply_text("/hkang [emoji] [packnum]")
    emoji = text[0]
    pack = text[1]
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
    pack_name = f"Hades_of_{user.id}_by_{context.bot.username}_{format}_{pack}"
    x = context.bot.get_stickerset(pack_name)
    if not x:
        await m.reply_text("Seems like new pack !"\n\nSet name of new pack by using <code>/setpname</code> [name]")
        ALPHA = True
        if ENTERED:
            title = ARGS
            if format == "video":
                context.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, webm_sticker=sticid)
            elif format == "animated":
                context.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, tgs_sticker=sticid)
            else:
                context.bot.create_new_sticker_set(user_id=user.id, name=pack_name, title=title, emojis=emoji, png_sticker=sticid)
        
    
    
    
