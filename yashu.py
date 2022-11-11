from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

async def start(u: Update, c: CallbackContext):
    await u.message.reply_text(f"Hello ! {u.effective_user.mention_html()}, Am kang bot of Hades Network, only Sudos can use me !")

async def kang(u: Update, c: CallbackContext):
    m = u.effective_message
    user = u.effective_user
    text = c.args
    
