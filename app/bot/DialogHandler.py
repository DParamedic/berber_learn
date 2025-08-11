import re

from app.bot import *
from app.models import *
from app.bot import standard_view
from app.repository.Repository import Repository
from app.DTO import Valid_User
from app.bot.CustomContext import CustomContext

class DialogHandler:
    async def start(self, update, context: CustomContext):
        await context.bot.send_message(
            chat_id=context.chat_id,
            text="Привет!",
        )
        user = await Repository.get_or_create_user(
            Valid_User(telegram_id=context.chat_id)
        )
        context.user_data_.set_dictionary(id=None, user_id=user.id)
        await Repository.get_classic_interval(
            "classic",
            [1 << grad for grad in range(10)],
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
        word = update.message.text.strip()
        if word:
            context.user_data_.set_word(content=word)
            await update.message.reply_text(
                f"Введено слово: {context.user_data_.word.content}.")
            return SET_WORD_ATTR
        else:
            await update.message.reply_text(
                "Неверный формат слова. Введите другое:")
        return INP_WORD
    # set_word_attr
    async def set_new_translate(self, update, context: CustomContext):
        await update.message.reply_text(
            "Введите перевод или несколько переводов через запятую: "
            )
        return INP_TRANSLATE
    # inp_translate
    async def input_translate(self, update, context: CustomContext):
        translations = update.message.text.strip()
        if translations:
            context.user_data_.translations_contents = [
                    translate.strip()
                    for translate
                    in translations.split(',')
                ]
            await update.message.reply_text(
                f"Введены переводы: {context.user_data_.translations_contents}."
            )
            return SET_WORD_ATTR
        else:
            await update.message.reply_text(
                "Неверный формат перевода. Введите иначе:")
            return INP_TRANSLATE
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
        word = await Repository.get_or_create_word(
            context.user_data_.word.validate()
        )
        del context.user_data_.word
        if context.user_data_.note:
            note = await Repository.get_or_create_note(
                context.user_data_.note.validate()
            )
            del context.user_data_.note
            context.user_data_.set_word_translate(note_id=note.id)
        translations = await Repository.get_or_create_translations(
            context.user_data_.valid_translations)
        context.user_data_.set_word_translate(
            word_id=word.id,
            translate_ids=[translate.id for translate in translations]
        )
        del context.user_data_.translations
        write_status = await Repository.create_word_translations(
            context.user_data_.word_translate.validate())
        del context.user_data_.word_translate
        if write_status:
            await update.message.reply_text("Записано успешно.")
        else:
            await update.message.reply_text("Запись найдена в базе данных.")
        return LOOP
    # loop
    async def add_dict(self, update, context: CustomContext):
        await update.message.reply_text(
            "Вы в меню добавления атрибутов словаря.\n"
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
        interval_lists = await Repository.get_interval_lists_by_user(
            context.user_data_.dictionary.user_id)
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
        language = await Repository.get_or_create_language(
            context.user_data_.language.validate()
        )
        del context.user_data_.language
        context.user_data_.set_dictionary(language_id=language.id)
        dictionary = await Repository.get_dictionary(
                user_id=context.user_data_.dictionary.user_id,
                language_id=context.user_data_.dictionary.language_id,
        )
        if dictionary:
            await update.message.reply_text("Уже существует такой словарь!")
        else:
            dictionary = await Repository.create_dictionary(
                context.user_data_.dictionary.validate())
            await update.message.reply_text("Словарь создан!")
        return LOOP
    # loop
    async def change_word(self, update, context: CustomContext):
        if not context.user_data_.dictionary.id:
            await update.message.reply_text("Не выбран словарь!")
            return LOOP
        await update.message.reply_text("Введите слово, которое планируете изменить:")
        return INP_SEARCH_VALUE_CH
    # inp_search_value_ch
    async def input_search_value_ch(self, update, context: CustomContext):
        searched_word = update.message.text.strip()
        if searched_word:
            await update.message.reply_text(
                f"Поиск {searched_word} в базе данных...")
            DTO = await Repository.get_word_translations_inf(
                    searched_word,
                    context.user_data_.dictionary.id,
            )
            if DTO:
                await update.message.reply_text(
                    "Найдена информация:\n"
                    f"  Слово: {searched_word}\n  Переводы: {DTO["translations"]}\n"
                    f"  Примечание: {DTO["note"] if DTO["note"] else ''}\n"
                    f"  Длительность: {DTO["interval"]}\n  Счетчик: {DTO["count"]}"
                )
                context.user_data_.set_old_word(content=searched_word)
                context.user_data_.word = context.user_data_.old_word
                context.user_data_.translations_contents = DTO["translations"]
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
        else:
            await update.message.reply_text(
                "Неверный формат слова. Введите иначе:")
        return INP_SEARCH_VALUE_CH
    # reset_word_attr
    async def reset_word(self, update, context: CustomContext):
        await update.message.reply_text("Введите исправленное слово: ")
        return INP_WORD_CH
    # inp_word_ch
    async def input_word_ch(self, update, context: CustomContext):
        word = update.message.text.strip()
        if word:
            del context.user_data_.word
            context.user_data_.set_word(content=word)
            await update.message.reply_text(
                f"Введено слово: {context.user_data_.word.content}."
            )
            return RESET_WORD_ATTR
        else:
            await update.message.reply_text(
                "Неверный формат слова. Введите иначе:")
            return INP_WORD_CH
    # reset_word_attr
    async def reset_translate(self, update, context: CustomContext):
        await update.message.reply_text(
            "Введите исправленный перевод или "
            "несколько переводов через запятую: "
            )
        return INP_TRANSLATE_CH
    # inp_translate_ch
    async def input_translate_ch(self, update, context: CustomContext):
        translations = update.message.text.strip()
        if translations:
            del context.user_data_.translations
            context.user_data_.translations_contents = [
                    translate.strip()
                    for translate
                    in translations.split(',')
                ]
            await update.message.reply_text(
                f"Введены переводы: {context.user_data_.translations_contents}."
            )
            return RESET_WORD_ATTR
        else:
            await update.message.reply_text(
                "Неверный формат введенный переводов. Введите иначе:")
            return INP_TRANSLATE_CH
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
        # Удаляем старые Word_Translations
        await Repository.delete_word_translations(
                context.user_data_.dictionary.id,
                context.user_data_.old_word.content,
        )
        del context.user_data_.old_word
        # Записываем новые
        context.user_data_.set_word_translate(
            dictionary_id=context.user_data_.dictionary.id,)
        word = await Repository.get_or_create_word(
            context.user_data_.word.validate())
        del context.user_data_.word
        if context.user_data_.note:
            note = await Repository.get_or_create_note(
                context.user_data_.note.validate())
            del context.user_data_.note
            context.user_data_.set_word_translate(note_id=note.id)
        translations = await Repository.get_or_create_translations(
            context.user_data_.valid_translations)
        context.user_data_.set_word_translate(
            word_id=word.id,
            translate_ids=[translate.id for translate in translations],
                interval_id=1,
                count = 0,
        )
        del context.user_data_.translations
        await Repository.create_word_translations(
            context.user_data_.word_translate.validate())
        del context.user_data_.word_translate
        await update.message.reply_text("Записано успешно.")
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
        searched_word = update.message.text.strip()
        if searched_word:
            await update.message.reply_text(
                f"Поиск {searched_word} в базе данных...")
            DTO = await Repository.get_word_translations_inf(
                    searched_word,
                    context.user_data_.dictionary.id,
            )
            if DTO:
                context.user_data_.set_word(content=searched_word)
                await update.message.reply_text(
                    "Найдена информация:\n"
                    f"  Слово: {searched_word}\n  Переводы: {DTO["translations"]}\n"
                    f"  Примечание: {DTO["note"] if DTO["note"] else ''}\n"
                    f"  Длительность: {DTO["interval"]}\n"
                    f"  Счетчик: {DTO["count"]}\n"
                    "Подтвердить: /y\nНе удалять: /n"
                )
                return CONFIRM_DEL
            else:
                await update.message.reply_text(
                    f"Не найдено слово {searched_word} в словаре.")
        else:
            await update.message.reply_text(
                "Неверный формат слова. Введите иначе:")
        return INP_SEARCH_VALUE_DEL
    # confirm_del
    async def confirm_del(self, update, context: CustomContext):
        await update.message.reply_text(
            f"Удаление {context.user_data_.word.content}...")
        await Repository.delete_word_translations(
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
        dictionaries = await Repository.get_dictionaries(
            context.user_data_.dictionary.user_id)
        if dictionaries:
            context.user_data_.dictionary_ids = [
                dictionary.id
                for dictionary
                in dictionaries
            ]
            await update.message.reply_text("Выберете словарь из списка:")
            for (
                idx,
                main_language,
                translate_language,
                interval_list,
            ) in await Repository.get_dict_info(dictionaries):
                await update.message.reply_text(
                    f"{idx + 1}: {main_language}, {translate_language}.\n"
                    f"Список интервалов: {interval_list}"
                )
            return SEL_DICT
        else:
            await update.message.reply_text(
                "У вас нет словарей!\n"
                "Используйте /add_dict,\nчтобы создать новый."
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
