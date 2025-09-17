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
            CallbackQueryHandler(handler.set_word_attr, pattern=f"^{cnds.R_ADD_WORD}$"),
            CallbackQueryHandler(handler.search_word, pattern=f"^{cnds.R_SEARCH_WORD}$"),
            CallbackQueryHandler(handler.set_dictionary_attr, pattern=f"^{cnds.R_ADD_DICT}$"),
            CallbackQueryHandler(handler.select_dictionary, pattern=f"^{cnds.R_SEL_DICT}$"),
            CallbackQueryHandler(handler.about, pattern=f"^{cnds.R_ABOUT}$"),
            CallbackQueryHandler(handler.settings, pattern=f"^{cnds.R_SETTINGS}$"),
            CallbackQueryHandler(handler.start_repetition, pattern=f"^{cnds.R_START_REPETITION}$"),
    ],
    states={
        cnds.C_SET_DICT_ATTR: [
            CallbackQueryHandler(handler.set_main_language, pattern=f"^{cnds.R_MAIN_LANGUAGE}$"),
            CallbackQueryHandler(handler.set_translation_language, pattern=f"^{cnds.R_TRANSLATE_LANGUAGE}$"),
            CallbackQueryHandler(handler.sel_interval_list, pattern=f"^{cnds.R_INTERVAL_LIST}$"),
            CallbackQueryHandler(handler.confirm_dict, pattern=f"^{cnds.R_CONFIRM_DICT}$"),
        ],
        cnds.C_INP_MAIN_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_main_language)],
        cnds.C_INP_TRANSLATE_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.input_translation_language)],
        cnds.C_SEL_INTERVAL_LIST: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.select_list_interval)],
    },
    fallbacks=[
        CallbackQueryHandler(handler.cancel, pattern=f"^{cnds.R_CANCEL}$"),
        CallbackQueryHandler(handler.confirm, pattern=f"^{cnds.R_CONFIRM}$"),
        CallbackQueryHandler(handler.confirm, pattern=f"^{cnds.R_CONDITION_ABOUT}$"),
        CallbackQueryHandler(handler.confirm, pattern=f"^{cnds.R_CONDITION_SETTINGS}$"),
    ],
    map_to_parent={
        cnds.R_CANCEL: cnds.C_ROOT,
        cnds.R_CONFIRM: cnds.C_ROOT,
        cnds.R_CONDITION_ABOUT: cnds.C_ROOT,
        cnds.R_CONDITION_SETTINGS: cnds.C_ROOT,
    }
)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', handler.start)],
    states={
        cnds.C_ROOT: [CallbackQueryHandler(handler.start_headline, pattern = f"^{cnds.R_CANCEL}$|^{cnds.R_CONFIRM}$")],
        cnds.C_ACTION: [loop_handler],
    },
    fallbacks=[CommandHandler('stop', handler.stop)],
    allow_reentry=True,
)
