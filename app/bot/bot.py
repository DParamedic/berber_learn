from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

from pydantic import BaseModel

AFTER_START, INP_WORD, INP_TRANSLATE, ROAD_FORK, CHANGE_MOD, DEL_MOD = range(6)
C_INP_SEARCH_VALUE, D_INP_SEARCH_VALUE = range(6, 8)
C_INP_WORD, C_INP_TRANSLATE, C_INP_TRANSLATE_2, C_INP_TRANSLATE_3, C_INP_NOTES = range(8, 13)
END = ConversationHandler.END

class InfoWord(BaseModel):
    word: str
    translate: str
    translate_2: str | None
    translate_3: str | None
    notes: str | None
    count: int = 0
    page_name: int = 0
    
    def representation(self):
        return f'{self.word} -- {self.translate}, ({self.translate_2}, {self.translate_3}).\nПояснения: {self.notes}'
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text='Привет!'
    )
    # insert_user(chat_id)
    
    return AFTER_START


# after_start
async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите слово: ')
    
    return INP_WORD

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Здесь пока ничего нет, но вы ждите.')
    
    return AFTER_START

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Здесь пока ничего нет, но вы ждите.')
    
    return AFTER_START

async def change_added_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите слово, которое планируете изменить.')
    
    return C_INP_SEARCH_VALUE

async def delete_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите слово, которое планируете удалить.')
    
    return D_INP_SEARCH_VALUE


# inp_word
async def input_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_word = update.message.text
    await update.message.reply_text(
        f'Введено слово: {new_word}.\n'
        'Введите перевод: '
    )
    
    return INP_TRANSLATE

# inp_translate
async def input_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_translate = update.message.text
    await update.message.reply_text(
        f'Введено слово: {new_translate}'
    )
    
    return ROAD_FORK

# read_fork
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Done.')
    
    return AFTER_START

async def change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'{''}.\nДополняй или изменяй.')
    
    return CHANGE_MOD

# change_mod
async def change_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите новое слово: ')
    
    return C_INP_WORD

async def change_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите новый перевод: ')
    
    return C_INP_TRANSLATE

async def change_translate_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите новый дополнительный перевод: ')
    
    return C_INP_TRANSLATE_2

async def change_translate_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите новый дополнительный перевод: ')
    
    return C_INP_TRANSLATE_3

async def change_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите новую заметку: ')
    
    return C_INP_NOTES
# + confirm

# c_inp_word
async def c_input_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_word = update.message.text
    await update.message.reply_text(
        f'Введено слово: {new_word}.'
    )
    
    return CHANGE_MOD

# c_inp_translate
async def c_input_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_word = update.message.text
    await update.message.reply_text(
        f'Введен перевод: {new_word}.'
    )
    
    return CHANGE_MOD

# c_inp_translate_2
async def c_input_translate_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_word = update.message.text
    await update.message.reply_text(
        f'Введен дополнительный перевод: {new_word}.'
    )
    
    return CHANGE_MOD

# c_inp_translate_3
async def c_input_translate_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_word = update.message.text
    await update.message.reply_text(
        f'Введен дополнительный перевод: {new_word}.'
    )
    
    return CHANGE_MOD

# c_inp_notes
async def c_input_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_word = update.message.text
    await update.message.reply_text(
        f'Введено примечание: {new_word}.'
    )
    
    return CHANGE_MOD


# c_inp_search_value
async def c_input_search_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_word = update.message.text
    await update.message.reply_text(
        f'Идет поиск: {new_word}...'
    )
    
    if True:
        return CHANGE_MOD
    else:
        await update.message.reply_text(
            f'Не найдено слово: {new_word}.'
        )
        return C_INP_SEARCH_VALUE

# d_inp_search_value
async def d_input_search_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_word = update.message.text
    await update.message.reply_text(
        f'Идет поиск: {new_word}...'
    )
    
    if False:
        return DEL_MOD
    else:
        await update.message.reply_text(
            f'Не найдено слово: {new_word}.'
        )
        return D_INP_SEARCH_VALUE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('That`s all.')
    
    return END

def ber_bot(token: str):
    application = ApplicationBuilder().token(token).build() # token
    
    # def app_span(application):
    #     print('Start')
    #     yield
    #     application.run_polling()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AFTER_START: [
                CommandHandler('add_word', add_word),
                CommandHandler('about', about),
                CommandHandler('settings', settings),
                CommandHandler('change_added_word', change_added_word),
                CommandHandler('delete_word', delete_word),
                ],
            
            INP_WORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_word)],
            INP_TRANSLATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_translate)],
            
            ROAD_FORK: [
                CommandHandler('confirm', confirm),
                CommandHandler('change', change),
                CommandHandler('add_more', change),
                ],
            
            CHANGE_MOD: [
                CommandHandler('change_word', change_word),
                CommandHandler('change_translate', change_translate),
                CommandHandler('change_translate_2', change_translate_2),
                CommandHandler('change_translate_3', change_translate_3),
                CommandHandler('change_notes', change_notes),
                CommandHandler('confirm', confirm),
            ],
            
            C_INP_WORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, c_input_word)],
            C_INP_TRANSLATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, c_input_translate)],
            C_INP_TRANSLATE_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, c_input_translate_2)],
            C_INP_TRANSLATE_3: [MessageHandler(filters.TEXT & ~filters.COMMAND, c_input_translate_3)],
            C_INP_NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, c_input_notes)],
            
            C_INP_SEARCH_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, c_input_search_value)],
            D_INP_SEARCH_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, d_input_search_value)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    
    application.run_polling()
