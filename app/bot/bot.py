from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
    )

from app.bot import *
from app.bot.DialogHandler import DialogHandler
from app.bot.CustomContext import CustomContext

def berber_bot(token: str):
    context_types = ContextTypes(context=CustomContext)
    application = ApplicationBuilder().token(token).context_types(context_types).build()
    handler = DialogHandler()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handler.start)],
        states={
            LOOP: [
                CommandHandler('add_word', handler.add_word),
                CommandHandler('ch_word', handler.change_word),
                CommandHandler('del_word', handler.delete_word),
                CommandHandler('add_dict', handler.add_dict),
                CommandHandler('sel_dict', handler.select_dict),                
                CommandHandler('about', handler.about),
                CommandHandler('settings', handler.settings),
                CommandHandler('test', handler.test),                
                ],
            SET_WORD_ATTR: [
                CommandHandler('set_word', handler.set_new_word),
                CommandHandler('set_translate', handler.set_new_translate),
                CommandHandler('set_notes', handler.set_new_note),
                CommandHandler('confirm', handler.confirm_new_word),
            ],
            INP_WORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_word)],
            INP_TRANSLATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_translate)],
            INP_NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_note)],
            DICT_ATTR: [
                CommandHandler('set_main_lang', handler.set_main_language),
                CommandHandler('set_tr_lang', handler.set_translation_language),
                CommandHandler('set_interval_list', handler.set_interval_list),
                CommandHandler('confirm', handler.confirm_dict),
            ],
            INP_MAIN_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_main_language)],
            INP_TRANSLATE_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_translation_language)],
            SEL_INTERVAL_LIST: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.select_list_interval)],
            INP_SEARCH_VALUE_CH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_search_value_ch)],
            RESET_WORD_ATTR: [
                CommandHandler('reset_word', handler.reset_word),
                CommandHandler('reset_translate', handler.reset_translate),
                CommandHandler('reset_notes', handler.reset_note),
                CommandHandler('confirm', handler.confirm_changed_word),
            ],
            INP_WORD_CH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_word_ch)],
            INP_TRANSLATE_CH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_translate_ch)],
            INP_NOTE_CH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_note_ch)],
            INP_SEARCH_VALUE_DEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_search_value_del)],
            CONFIRM_DEL: [
                CommandHandler('y', handler.confirm_del),
                CommandHandler('n', handler.revoke_del),
            ],
            SEL_DICT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_selected_dict)],
        },
        fallbacks=[CommandHandler('cancel', handler.cancel)]
    )

    application.add_handler(conv_handler)
    application.run_polling()
