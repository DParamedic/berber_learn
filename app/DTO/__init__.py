from typing import Generator
from app.models import Word_Translate
from collections import namedtuple

from app.DTO.validDTO import (
    Valid_Dictionary,
    Valid_Language,
    Valid_Word,
    Valid_Word_Translate,
    Valid_User,
    Valid_Interval,
    Valid_Interval_List,
    Valid_Link_Interval_List,
    Valid_User_Settings,
)
from app.DTO.extraDTO import (
    Extra_Dictionary,
    Extra_Language,
    Extra_Word,
    Extra_Word_Translate,
)

TreePathANdContentView = namedtuple(
    "TreePathANdContentView",
    ["dictionary_name", "word_name", "translations"],
)

def convert_to_tree(
    database_query: list[Word_Translate]
) -> dict[str, dict[str, dict[str, tuple]]]:
    root = {}
    for word_translate in database_query:
        dictionary_name = (
            word_translate.dictionary.language.main_language
            + ", "
            + word_translate.dictionary.language.translation_language
        )
        if dictionary_name not in root:
            root[dictionary_name] = {}
        dictionary = root[dictionary_name]
        word_name = word_translate.word.content
        if word_name not in dictionary:
            dictionary[word_name] = {}
        word = dictionary[word_name]
        translate_name = word_translate.translate.content
        if translate_name not in word:
            word[translate_name] = (
                word_translate.dictionary_id,
                word_translate.word_id,
                word_translate.translate_id,
                word_translate.dictionary.interval_list_id,
                word_translate.count,
            )
    return root

def convert_tree_to_generator(
    tree: dict[str, dict[str, dict[str, tuple]]]
) -> Generator[type[tuple], None, None]:
    for dictionary_name, dictionary in tree.items():
        for word_name, word in dictionary.items():
            yield TreePathANdContentView(dictionary_name, word_name, word)
