from telegram.ext import ConversationHandler

# C_[A-Z]+[_]?[A-Z]+ - состояния (Conditions): int
# R_[A-Z]+[_]?[A-Z]+ - возвраты (Returns): str

R_END = ConversationHandler.END

(
    C_ACTION,
    C_SET_DICT_ATTR,
    C_INP_MAIN_LANGUAGE, C_INP_TRANSLATE_LANGUAGE, C_SEL_INTERVAL_LIST,
    C_SEL_DICT, C_CHOICE_ACTION_WITH_DICT, C_CONFIRM_DEL_DICT,
    C_EMPTY,
) = range(9)

(
    R_ADD_WORD,
    R_SEARCH_WORD,
    R_ADD_DICT,
    R_MAIN_LANGUAGE, R_TRANSLATE_LANGUAGE, R_INTERVAL_LIST, R_CONFIRM_DICT,
    R_MANAGE_DICT, R_SEL_DICT, R_DEL_DICT, R_CONFIRM_DD, R_UNDO_DD,
    R_ABOUT,
    R_SETTINGS,
    R_START_REPETITION,
    R_CONFIRM,
    R_CANCEL,
) = map(str, range(13))