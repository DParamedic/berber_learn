import re

from telegram.ext import ConversationHandler

(
    LOOP,
    SET_WORD_ATTR, INP_WORD, INP_TRANSLATE, INP_NOTE,
    DICT_ATTR, INP_MAIN_LANGUAGE, INP_TRANSLATE_LANGUAGE, SEL_INTERVAL_LIST,
    INP_SEARCH_VALUE_CH,
    RESET_WORD_ATTR, INP_WORD_CH, INP_TRANSLATE_CH, INP_NOTE_CH,
    INP_SEARCH_VALUE_DEL, CONFIRM_DEL,
    SEL_DICT,
) = range(17)
END = ConversationHandler.END

def standard_view(word: str) -> str:
    word = re.sub('ё', 'е', word.strip())
    return word.capitalize()

__all__ = [
    "LOOP",
    "SET_WORD_ATTR", "INP_WORD", "INP_TRANSLATE", "INP_NOTE",
    "DICT_ATTR", "INP_MAIN_LANGUAGE", "INP_TRANSLATE_LANGUAGE", "SEL_INTERVAL_LIST",
    "INP_SEARCH_VALUE_CH",
    "RESET_WORD_ATTR", "INP_WORD_CH", "INP_TRANSLATE_CH", "INP_NOTE_CH",
    "INP_SEARCH_VALUE_DEL", "CONFIRM_DEL",
    "SEL_DICT",
    "END",
]