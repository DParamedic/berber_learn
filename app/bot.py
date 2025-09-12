from telegram.ext import ApplicationBuilder, ContextTypes

from app.bot_handler.CustomContext import CustomContext
from app.bot_handler.new_conv_handler import conv_handler

def berber_bot(token: str):
    context_types = ContextTypes(context=CustomContext)
    application = ApplicationBuilder().token(token).context_types(context_types).build()

    application.add_handler(conv_handler)
    application.run_polling()
