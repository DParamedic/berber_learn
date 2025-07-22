from telegram import Update
from telegram.ext import ContextTypes
import re

from app.database import async_session_maker
from app.bot import *

import app.auth.models
import app.dictionary.models
import app.settings.models

from app.auth.DTO import User as User_Pydantic
from app.dictionary.DTO import (
    Language as Language_Pydantic,
    Dictionary as Dictionary_Pydantic,
    Word as Word_Pydantic,
    Note as Note_Pydantic,
    Word_Translate as Word_Translate_Pydantic,
    )
from app.settings.DTO import (
    Interval as Interval_Pydantic,
    Interval_List as Interval_List_Pydantic,
    Link_Interval_List as Link_Interval_List_Pydantic,
    User_Settings as User_Settings_Pydantic
    )
from app.auth.repository import AuthRepository
from app.dictionary.repository import DictionaryRepository
from app.settings.repository import SettingsRepository
from app.bot.CustomContext import CustomContext

class DialogHandler:
    def __init__(self):
        pass
    
    async def start(self, update, context: CustomContext):
        await context.bot.send_message(
            chat_id=context.chat_id,
            text="Привет!",
        )
        async with async_session_maker() as connect:
            user = await AuthRepository(connect).get_user_by_telegram_id(
                context.chat_id
                )
            if not user:
                user = await AuthRepository(connect).create_user(
                    User_Pydantic.model_validate(
                        telegram_id=context.chat_id,
                    )
                )
            context.user_data_.set_dictionary(
                id=None, user_id=user.id)
        async with async_session_maker() as connect:
            interval_list = await SettingsRepository(connect).get_interval_list_by_name("classic")
            if not interval_list:
                interval_list = await SettingsRepository(connect).create_interval_list(
                    Interval_List_Pydantic.model_validate(
                        {
                            "name": "classic",
                        }
                    )
                )
        async with async_session_maker() as connect:
            for gradus in range(8):
                interval = await SettingsRepository(connect).get_interval_by_length(1 << gradus)
                if not interval:
                    interval = await SettingsRepository(connect).create_interval(
                        Interval_Pydantic.model_validate(
                            {
                                "length": 1 << gradus,
                            }
                        )
                    )
                link_interval_list = await SettingsRepository(connect).get_link_interval_list_by_ids(
                    interval_list.id,
                    interval.id,
                )
                if not link_interval_list:
                    await SettingsRepository(connect).create_link_interval_list(
                        Link_Interval_List_Pydantic.model_validate(
                            {
                                "interval_list_id": interval_list.id,
                                "interval_id": interval.id,
                            }
                        )
                    )
        await update.message.reply_text(
            "Доступные команды:\n"
            "/add_word\n"
            "/ch_word\n"
            "/del_word\n"
            "/add_dict\n"
            "/sel_dict\n"
            "/about\n"
            "/settings\n"
            "/cancel"
            )
        return LOOP

    # loop
    async def add_word(self, update, context: CustomContext):
        if not context.user_data_.dictionary.id:
            await update.message.reply_text("Не выбран словарь!")
            return LOOP
        await update.message.reply_text(
            "Вы в меню добавления атрибутов!\n"
            "Доступные команды:\n"
            "/set_word\n"
            "/set_translate\n"
            "/set_notes\n"
            "/confirm"
            )
        return SET_WORD_ATTR
    # set_word_attr
    async def set_new_word(self, update, context: CustomContext):
        await update.message.reply_text("Введите слово: ")
        return INP_WORD
    # inp_word
    async def input_word(self, update, context: CustomContext):
        word = re.sub('ё', 'е', update.message.text.strip().lower())
        if word:
            context.user_data_.set_word(content=word.capitalize())
            await update.message.reply_text(
                f"Введено слово: {context.user_data_.word.content}."
            )
        return SET_WORD_ATTR
    # set_word_attr
    async def set_new_translate(self, update, context: CustomContext):
        await update.message.reply_text(
            "Введите перевод или несколько переводов через запятую: "
            )
        return INP_TRANSLATE
    # inp_translate
    async def input_translate(self, update, context: CustomContext):
        translates = re.sub('ё', 'е', update.message.text.strip().lower())
        if translates:
            context.user_data_.translates_contents = [
                    translate.strip().capitalize()
                    for translate
                    in translates.split(',')
                ]
            await update.message.reply_text(
                f"Введены переводы: {context.user_data_.translates_contents}."
            )
        return SET_WORD_ATTR
    # set_word_attr
    async def set_new_note(self, update, context: CustomContext):
        await update.message.reply_text("Введите примечание: ")
        return INP_NOTE
    # inp_note
    async def input_note(self, update, context: CustomContext):
        context.user_data_.set_note(content=update.message.text)
        await update.message.reply_text(
            f"Введено примечание: {context.user_data_.note.content}.")
        return SET_WORD_ATTR
    # set_word_attr
    async def confirm_new_word(self, update, context: CustomContext):
        context.user_data_.set_word_translate(
            dictionary_id=context.user_data_.dictionary.id,
            interval_id=1,
            count = 0,
        )
        # добавить функцию добавления минимального интервала
        async with async_session_maker() as connect:
            word = await DictionaryRepository(connect).get_word_by_content(
                context.user_data_.word.content,
            )
            if not word:
                word = await DictionaryRepository(connect).create_word(
                    context.user_data_.word.validate()
                )
            del context.user_data_.word
            for idx, valid_translate in enumerate(context.user_data_.valid_translates):
                translate = await DictionaryRepository(connect).get_word_by_content(valid_translate.content)
                if not translate:
                    translate = await DictionaryRepository(connect).create_word(valid_translate)
                context.user_data_.translates[idx].id = translate.id
            if context.user_data_.note:
                note = await DictionaryRepository(connect).create_note(
                    context.user_data_.note.validate()
                )
                del context.user_data_.note
                context.user_data_.set_word_translate(
                    note_id=note.id)
            context.user_data_.set_word_translate(
                word_id=word.id,
                translate_ids=context.user_data_.translates_ids
            )
            del context.user_data_.translates
        async with async_session_maker() as connect:
            await DictionaryRepository(connect).create_word_translates(
                context.user_data_.word_translate.validate()
            )
        del context.user_data_.word_translate
        await update.message.reply_text("Запись в бд произведена успешно!")
        return LOOP
    # loop
    async def add_dict(self, update, context: CustomContext):
        await update.message.reply_text(
            "Вы в меню добавления атрибутов словаря!\n"
            "Доступные команды: \n"
            "/set_main_lang\n"
            "/set_tr_lang\n"
            "/set_interval_list\n"
            "/confirm"
            )
        return DICT_ATTR
    # dict_attr
    async def set_main_language(self, update, context: CustomContext):
        await update.message.reply_text(
            "Введите название основного языка.\n"
            "(Например, для англо-русского словаря это \"Английский\").\n"
            "Используйте любые удобные названия кроме пустого.)"
            )
        return INP_MAIN_LANGUAGE
    # inp_main_language
    async def input_main_language(self, update, context: CustomContext):
        if update.message.text:
            context.user_data_.set_language(main_language=update.message.text)
            await update.message.reply_text(
                f"Записано: {context.user_data_.language.main_language}")
            return DICT_ATTR
        else:
            await update.message.reply_text("Название пустое. Не подходит.")
            return INP_MAIN_LANGUAGE
    # dict_attr
    async def set_translation_language(self, update, context: CustomContext):
        await update.message.reply_text(
            "Введите название языка перевода.\n"
            "(Например, для англо-русского словаря это \"Русский\").\n"
            "Используйте любые удобные названия кроме пустого."
            )
        return INP_TRANSLATE_LANGUAGE
    # inp_translate_language
    async def input_translation_language(self, update, context: CustomContext):
        translation_language = update.message.text
        if translation_language:
            context.user_data_.set_language(
                translation_language=translation_language)
            await update.message.reply_text(
                f"Записано: {context.user_data_.language.translation_language}"
                )
            return DICT_ATTR
        else:
            await update.message.reply_text("Название пустое. Не подходит.")
            return INP_TRANSLATE_LANGUAGE
    # dict_attr
    async def set_interval_list(self, update, context: CustomContext):
        await update.message.reply_text(
            "Введите номер списка интервалов из представленных ниже.")
        async with async_session_maker() as connect:
            interval_lists = await SettingsRepository(
                connect).get_interval_lists_by_user(context.chat_id)
            context.user_data_.interval_ids = [
                interval_list.id
                for interval_list
                in interval_lists
            ]
            for idx, interval_list in enumerate(interval_lists):
                await update.message.reply_text(f"{idx + 1}: {interval_list.name}")
        return SEL_INTERVAL_LIST
    # sel_interval_list
    async def select_list_interval(self, update, context: CustomContext):
        input = update.message.text
        if input.isnumeric():
            context.user_data_.set_dictionary(
                interval_list_id=context.user_data_.interval_ids[int(input) - 1]
            )
            del context.user_data_.interval_ids
            await update.message.reply_text(
                f"Выбран список интервалов {input}")
            return DICT_ATTR
        else:
            await update.message.reply_text(f"Введен некорректный символ <{input}>")
            return SEL_INTERVAL_LIST
    # dict_attr
    async def confirm_dict(self, update, context: CustomContext):
        async with async_session_maker() as connect:
            language = await DictionaryRepository(connect).get_language_by_languages(
                context.user_data_.language.main_language,
                context.user_data_.language.translation_language,
            )
            if not language:
                language = await DictionaryRepository(connect).create_language(
                    context.user_data_.language.validate())
        del context.user_data_.language
        context.user_data_.set_dictionary(language_id=language.id)
        async with async_session_maker() as connect:
            dictionary = await DictionaryRepository(connect).get_dictionary_by_user_id_language_id(
                context.user_data_.dictionary.user_id,
                context.user_data_.dictionary.language_id,
            )
            await update.message.reply_text("Уже существует такой словарь!")
            if not dictionary:
                dictionary = await DictionaryRepository(connect).create_dictionary(
                    context.user_data_.dictionary.validate(),
                )
                await update.message.reply_text("Словарь создан!")
        return LOOP
    # loop
    async def change_word(self, update, context: CustomContext):
        if not context.user_data_.dictionary.id:
            await update.message.reply_text("Не выбран словарь!")
            return LOOP
        await update.message.reply_text("Введите слово, которое планируете изменить:")
        return INP_SEARCH_VALUE_CH
    # inp_search_value_ch                ],
    async def input_search_value_ch(self, update, context: CustomContext):
        searched_word = re.sub('ё', 'е', update.message.text.strip().lower())
        searched_word = searched_word.capitalize()
        await update.message.reply_text(
            f"Поиск {searched_word} в базе данных...")
        async with async_session_maker() as connect:
            DTO = await DictionaryRepository(connect).get_word_and_translates(
                searched_word,
                context.user_data_.dictionary.id,
            )
        if DTO:
            await update.message.reply_text(f"Найдена информация: {DTO}")
            context.user_data_.set_old_word(content=DTO["word"])
            context.user_data_.word = context.user_data_.old_word
            context.user_data_.translates_contents = DTO["translates"]
            if DTO["note"]:
                context.user_data_.set_note(content=DTO["note"])
            await update.message.reply_text(
                "Вы в меню изменения атрибутов слова!\n"
                "Доступные команды: \n"
                "/reset_word\n"
                "/reset_translate\n"
                "/reset_notes\n"
                "/confirm"
            )
            return RESET_WORD_ATTR
        else:
            await update.message.reply_text(
                f"Не найдено слово {searched_word} в словаре.\n"
                "Введите другое:"
            )
            return INP_SEARCH_VALUE_CH
    # reset_word_attr
    async def reset_word(self, update, context: CustomContext):
        await update.message.reply_text("Введите исправленное слово: ")
        return INP_WORD_CH
    # inp_word_ch
    async def input_word_ch(self, update, context: CustomContext):
        word = re.sub('ё', 'е', update.message.text.strip().lower())
        if word:
            del context.user_data_.word
            context.user_data_.set_word(content=word.capitalize())
            await update.message.reply_text(
                f"Введено слово: {context.user_data_.word.content}."
            )
        return RESET_WORD_ATTR
    # reset_word_attr
    async def reset_translate(self, update, context: CustomContext):
        await update.message.reply_text(
            "Введите исправленный перевод или "
            "несколько переводов через запятую: "
            )
        return INP_TRANSLATE_CH
    # inp_translate_ch
    async def input_translate_ch(self, update, context: CustomContext):
        translates = re.sub('ё', 'е', update.message.text.strip().lower())
        if translates:
            del context.user_data_.translates
            context.user_data_.translates_contents = [
                    translate.strip().capitalize()
                    for translate
                    in translates.split(',')
                ]
            await update.message.reply_text(
                f"Введены переводы: {context.user_data_.translates_contents}."
            )
        return RESET_WORD_ATTR
    # reset_word_attr
    async def reset_note(self, update, context: CustomContext):
        await update.message.reply_text("Введите исправленное примечание: ")
        return INP_NOTE_CH
    # inp_note_ch
    async def input_note_ch(self, update, context: CustomContext):
        note = update.message.text
        if note:
            del context.user_data_.note
            context.user_data_.set_note(content=note)
            await update.message.reply_text(
                f"Введено примечание: {context.user_data_.note.content}.")
        return RESET_WORD_ATTR
    # reset_word_attr
    async def confirm_changed_word(self, update, context: CustomContext):
        # Удаляем старые Word_Translates
        async with async_session_maker() as connect:
            await DictionaryRepository(connect).delete_word_translates_by_word(
                context.user_data_.dictionary.id,
                context.user_data_.old_word.content,
            )
        del context.user_data_.old_word
        # Записываем новые
        context.user_data_.set_word_translate(
            dictionary_id=context.user_data_.dictionary.id,)
        async with async_session_maker() as connect:
            word = await DictionaryRepository(connect).get_word_by_content(
                # word is empty because data in old_word 
                context.user_data_.word.content)
            if not word:
                word = await DictionaryRepository(connect).create_word(
                    context.user_data_.word.validate())
            del context.user_data_.word
            for idx, valid_translate in enumerate(context.user_data_.valid_translates):
                translate = await DictionaryRepository(connect).get_word_by_content(valid_translate.content)
                if not translate:
                    translate = await DictionaryRepository(connect).create_word(valid_translate)
                context.user_data_.translates[idx].id = translate.id
            if context.user_data_.note:
                async with async_session_maker() as connect:
                    note = await DictionaryRepository().get_note_by_content(
                        context.user_data_.note.content
                    )
                    if not note:
                        note = await DictionaryRepository().create_note(
                            context.user_data_.note.validate()
                        )
                del context.user_data_.note
                context.user_data_.set_word_translate(
                    note_id=note.id)
            context.user_data_.set_word_translate(
                word_id=word.id,
                translate_ids=context.user_data_.translates_ids,
                interval_id=1,
                count = 0,
            )
            del context.user_data_.translates
        async with async_session_maker() as connect:
            await DictionaryRepository(connect).create_word_translates(
                context.user_data_.word_translate.validate()
            )
        del context.user_data_.word_translate
        await update.message.reply_text("Запись в бд произведена успешно!")
        return LOOP
    # loop
    async def delete_word(self, update, context: CustomContext):
        if not context.user_data_.dictionary.id:
            await update.message.reply_text("Не выбран словарь!")
            return LOOP
        await update.message.reply_text("Введите слово, которое планируете удалить:")
        return INP_SEARCH_VALUE_DEL
    # inp_search_value_del
    async def input_search_value_del(self, update, context: CustomContext):
        searched_word = update.message.text
        searched_word = re.sub('ё', 'е', searched_word.strip().lower())
        searched_word = searched_word.capitalize()
        await update.message.reply_text(
            f"Поиск {searched_word} в базе данных...")
        async with async_session_maker() as connect:
            DTO = await DictionaryRepository(connect).get_word_and_translates(
                searched_word,
                context.user_data_.dictionary.id,
            )
        if DTO:
            context.user_data_.set_word(content=searched_word)
            await update.message.reply_text(f"Найдена информация: {DTO}")
            return CONFIRM_DEL
        else:
            await update.message.reply_text(
                f"Не найдено слово {searched_word} в словаре.")
            return INP_SEARCH_VALUE_DEL
    # confirm_del
    async def confirm_del(self, update, context: CustomContext):
        await update.message.reply_text(
            f"Удаление {context.user_data_.word.content}...")
        async with async_session_maker() as connect:
            await DictionaryRepository(connect).delete_word_translates_by_word(
                context.user_data_.dictionary.id,
                context.user_data_.word.content,
            )
        del context.user_data_.word
        await update.message.reply_text("Удалено.")
        return LOOP
    # confirm_del
    async def revoke_del(self, update, context: CustomContext):
        del context.user_data_.word
        await update.message.reply_text("Отмена удаления...")
        return LOOP
    # loop
    async def select_dict(self, update, context: CustomContext):
        async with async_session_maker() as connect:
            dictionaries = await DictionaryRepository(connect).get_dictionaries_by_user_id(
                context.user_data_.dictionary.user_id
            )
        if dictionaries:
            context.user_data_.dictionary_ids = [
                dictionary.id
                for dictionary
                in dictionaries
            ]
            await update.message.reply_text("Выберете словарь из списка:")
            for idx, dictionary in enumerate(dictionaries):
                async with async_session_maker() as connect:
                    language = await DictionaryRepository(connect).get_language_by_id(
                        dictionary.language_id
                    )
                    interval_list = await SettingsRepository(connect).get_interval_list_by_id(
                        dictionary.interval_list_id
                    )
                    await update.message.reply_text(
                        f"{idx + 1}: {(
                            language.main_language,
                            language.translation_language,
                            interval_list.name
                            )}"
                        )
            return SEL_DICT
        else:
            await update.message.reply_text(
                "У вас нет словарей!\n"
                "Используйте /add_dict, чтобы создать новый."
                )
            return LOOP
    # sel_dict
    async def input_selected_dict(self, update, context: CustomContext):
        input = update.message.text
        if input.isnumeric():
            context.user_data_.dictionary.id = context.user_data_.dictionary_ids[
                int(input) - 1
                ]
            del context.user_data_.dictionary_ids
            await update.message.reply_text(f"Выбран словарь {input}")
            return LOOP
        else:
            await update.message.reply_text(f"Введен некорректный символ <{input}>")
            return SEL_DICT
    # loop
    async def about(self, update, context: CustomContext):
        await update.message.reply_text(
            "Berber learn v.0.2-pre_alpha\n"
            "Доступны команды:\n"
            "/add_word\n"
            "/ch_word\n"
            "/del_word\n"
            "/add_dict\n"
            "/sel_dict\n"
            "/about\n"
            "/settings\n"
            "/cancel"
            )
        return LOOP
    # loop
    async def settings(self, update, context: CustomContext):
        await update.message.reply_text("Здесь пока ничего нет, но вы ждите.")
        return LOOP

    async def test(self, update, context: CustomContext):
        await update.message.reply_text("Здесь пока ничего нет, но вы ждите.")
        return LOOP
        
    # loop
    async def cancel(self, update, context: CustomContext):
        await update.message.reply_text('Завершение работы...')
        context.user_data_.clear()
        return END
