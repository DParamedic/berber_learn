from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    filters,
    )

from app.bot_handler import conditions as cnds
from app.bot_handler import new_handler as handler

loop_handler = ConversationHandler(
    entry_points=[
            CallbackQueryHandler(handler.set_word_attr, pattern = '^' + cnds.ADD_WORD + '$'),
            CallbackQueryHandler(handler.search_word, pattern = '^' + cnds.SEARCH_WORD + '$'),
            CallbackQueryHandler(handler.set_dictionary_attr, pattern = '^' + cnds.ADD_DICT + '$'),
            CallbackQueryHandler(handler.select_dict, pattern = '^' + cnds.SEL_DICT + '$'),
            CallbackQueryHandler(handler.about, pattern = '^' + cnds.ABOUT + '$'),
            CallbackQueryHandler(handler.settings, pattern = '^' + cnds.SETTINGS + '$'),
            CallbackQueryHandler(handler.start_repetition, pattern = '^' + cnds.START_REPETITION + '$'),
    ],
    states={
        cnds.SET_DICT_ATTR: [
            CallbackQueryHandler(handler.set_main_language, pattern = '^' + cnds.INP_MAIN_LANGUAGE + '$'),
            CallbackQueryHandler(handler.set_translation_language, pattern = '^' + cnds.INP_TRANSLATE_LANGUAGE + '$'),
            CallbackQueryHandler(handler.sel_interval_list, pattern = '^' + cnds.SEL_INTERVAL_LIST + '$'),
            CallbackQueryHandler(handler.confirm_dict, pattern = '^' + cnds.CONFIRM_DICT + '$'),
        ],
        cnds.INP_MAIN_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_main_language)],
        cnds.INP_TRANSLATE_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_translation_language)],
        cnds.SEL_INTERVAL_LIST: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.select_list_interval)],
        
        cnds.CONDITION_ABOUT: CallbackQueryHandler(handler.confirm, pattern = '^' + cnds.CONFIRM + '$'),
        cnds.CONDITION_SETTINGS: CallbackQueryHandler(handler.confirm, pattern = '^' + cnds.CONFIRM + '$'),
    },
    fallbacks=[cnds.CANCEL,
        CallbackQueryHandler(handler.cancel, pattern = '^' + cnds.CANCEL + '$'),
    ],
    map_to_parent={
        cnds.CANCEL: cnds.ROOT,
        cnds.CONFIRM: cnds.ROOT,
    }
)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', handler.start)],
    states={
        cnds.ROOT: [CallbackQueryHandler(handler.start_headline, pattern = '^' + cnds.CANCEL + '$' + "|" + '^' + cnds.CONFIRM + '$')],
        cnds.ACTION: [loop_handler],
    },
    fallbacks=[CommandHandler('stop', handler.stop)],
)
pattern = '^' +  + '$'