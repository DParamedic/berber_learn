from telegram.ext import ConversationHandler

# C_[A-Z]+[_]?[A-Z]+ - состояния (Conditions): int
# R_[A-Z]+[_]?[A-Z]+ - возвраты (Returns): str

R_END = ConversationHandler.END

(
    C_ROOT, C_ACTION,
    C_SET_DICT_ATTR,
    C_INP_MAIN_LANGUAGE, C_INP_TRANSLATE_LANGUAGE, C_SEL_INTERVAL_LIST,
) = range(6)

(
    R_ADD_WORD,
    R_SEARCH_WORD,
    R_ADD_DICT,
    R_MAIN_LANGUAGE, R_TRANSLATE_LANGUAGE, R_INTERVAL_LIST, R_CONFIRM_DICT,
    R_SEL_DICT,
    R_ABOUT, R_CONDITION_ABOUT,
    R_SETTINGS, R_CONDITION_SETTINGS,
    R_START_REPETITION,
    R_CONFIRM,
    R_CANCEL,
) = map(str, range(15))