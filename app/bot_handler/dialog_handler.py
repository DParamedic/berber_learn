import datetime
import asyncio
from typing import Iterable

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from app.bot_handler import *
from app.models import *
from app.repository import ConnectedRepository as Repository
from app.DTO import Valid_User, convert_to_tree, convert_tree_to_generator
from app.bot_handler.CustomContext import CustomContext

async def start(update: Update, context: CustomContext):
    await context.bot.send_message(
        chat_id=context.chat_id,
        text="Привет!",
    )
    user = await Repository.get_or_create_user(
        Valid_User(telegram_id=context.user_id))
    context.custom_user_data.set_dictionary(id=None, user_id=user.id)
    # start daily check
    context.job_queue.run_daily(
        repetition_reminder,
        time=datetime.time(hour=12),
        chat_id=context.chat_id,
        user_id=context.user_id,
    )
    await Repository.create_classic_interval(
        context.custom_user_data.dictionary.user_id,
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
        "/start_event\n"
        "/about\n"
        "/settings\n"
        "/cancel"
        )
    return LOOP
# loop
async def add_word(update: Update, context: CustomContext):
    context.custom_user_data.dialog_active = True
    if not context.custom_user_data.dictionary.id:
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
async def set_new_word(update: Update, context: CustomContext):
    await update.message.reply_text("Введите слово: ")
    return INP_WORD
# inp_word
async def input_word(update: Update, context: CustomContext):
    word = update.message.text.strip()
    if word:
        context.custom_user_data.set_word(content=word)
        await update.message.reply_text(
            f"Введено слово: {context.custom_user_data.word.content}.")
        return SET_WORD_ATTR
    else:
        await update.message.reply_text(
            "Неверный формат слова. Введите другое:")
    return INP_WORD
# set_word_attr
async def set_new_translate(update: Update, context: CustomContext):
    await update.message.reply_text(
        "Введите перевод или несколько переводов через запятую: "
        )
    return INP_TRANSLATE
# inp_translate
async def input_translate(update: Update, context: CustomContext):
    translations = update.message.text.strip()
    if translations:
        context.custom_user_data.translations_contents = [
                translate.strip()
                for translate
                in translations.split(',')
            ]
        await update.message.reply_text(
            f"Введены переводы: {context.custom_user_data.translations_contents}."
        )
        return SET_WORD_ATTR
    else:
        await update.message.reply_text(
            "Неверный формат перевода. Введите иначе:")
        return INP_TRANSLATE
# set_word_attr
async def set_new_note(update: Update, context: CustomContext):
    await update.message.reply_text("Введите примечание: ")
    return INP_NOTE
# inp_note
async def input_note(update: Update, context: CustomContext):
    note = update.message.text
    if note:
        del context.custom_user_data.note
        context.custom_user_data.set_note(content=note)
        await update.message.reply_text(
            f"Введено примечание: {context.custom_user_data.note.content}.")
        return SET_WORD_ATTR
    else:
        await update.message.reply_text(
            "Неверный формат примечания. Введите иначе:")
        return INP_NOTE
# set_word_attr
async def confirm_new_word(update: Update, context: CustomContext):
    context.custom_user_data.set_word_translate(
        dictionary_id=context.custom_user_data.dictionary.id,
        interval_id=1,
        count = 0,
    )
    # добавить функцию добавления минимального интервала
    word = await Repository.get_or_create_word(
        context.custom_user_data.word.validate()
    )
    del context.custom_user_data.word
    if context.custom_user_data.note:
        note = await Repository.get_or_create_note(
            context.custom_user_data.note.validate()
        )
        del context.custom_user_data.note
        context.custom_user_data.set_word_translate(note_id=note.id)
    translations = await Repository.get_or_create_translations(
        context.custom_user_data.valid_translations)
    context.custom_user_data.set_word_translate(
        word_id=word.id,
        translate_ids=[translate.id for translate in translations]
    )
    del context.custom_user_data.translations
    write_status = await Repository.create_word_translations(
        context.custom_user_data.word_translate.validate())
    del context.custom_user_data.word_translate
    if write_status:
        await update.message.reply_text("Записано успешно.")
    else:
        await update.message.reply_text("Запись найдена в базе данных.")
    context.custom_user_data.dialog_active = False
    return LOOP

async def add_dict(update: Update, context: CustomContext):
    context.custom_user_data.dialog_active = True
    await update.message.reply_text(
        "Вы в меню добавления атрибутов словаря.\n"
        "Доступные команды: \n"
        "/set_main_lang\n"
        "/set_tr_lang\n"
        "/set_interval_list\n"
        "/confirm"
        )
    return SET_DICT_ATTR
# dict_attr
async def set_main_language(update: Update, context: CustomContext):
    await update.message.reply_text(
        "Введите название основного языка.\n"
        "(Например, для англо-русского словаря это \"Английский\").\n"
        "Используйте любые удобные названия кроме пустого.)"
        )
    return INP_MAIN_LANGUAGE
# inp_main_language
async def input_main_language(update: Update, context: CustomContext):
    main_language = update.message.text
    if main_language:
        context.custom_user_data.set_language(main_language=main_language)
        await update.message.reply_text(
            f"Записано: {context.custom_user_data.language.main_language}")
        return SET_DICT_ATTR
    else:
        await update.message.reply_text("Название пустое. Не подходит.")
        return INP_MAIN_LANGUAGE
# dict_attr
async def set_translation_language(update: Update, context: CustomContext):
    await update.message.reply_text(
        "Введите название языка перевода.\n"
        "(Например, для англо-русского словаря это \"Русский\").\n"
        "Используйте любые удобные названия кроме пустого."
        )
    return INP_TRANSLATE_LANGUAGE
# inp_translate_language
async def input_translation_language(update: Update, context: CustomContext):
    translation_language = update.message.text
    if translation_language:
        context.custom_user_data.set_language(
            translation_language=translation_language)
        await update.message.reply_text(
            f"Записано: {context.custom_user_data.language.translation_language}"
            )
        return SET_DICT_ATTR
    else:
        await update.message.reply_text("Название пустое. Не подходит.")
        return INP_TRANSLATE_LANGUAGE
# dict_attr
async def sel_interval_list(update: Update, context: CustomContext):
    await update.message.reply_text(
        "Введите номер списка интервалов из представленных ниже.")
    interval_lists = await Repository.get_interval_lists_by_user(
        context.custom_user_data.dictionary.user_id)
    context.custom_user_data.interval_ids = [
        interval_list.id
        for interval_list
        in interval_lists
    ]
    for idx, interval_list in enumerate(interval_lists):
        await update.message.reply_text(f"{idx + 1}: {interval_list.name}")
    return SEL_INTERVAL_LIST
# sel_interval_list
async def select_list_interval(update: Update, context: CustomContext):
    input = update.message.text
    if input.isnumeric():
        context.custom_user_data.set_dictionary(
            interval_list_id=context.custom_user_data.interval_ids[int(input) - 1]
        )
        del context.custom_user_data.interval_ids
        await update.message.reply_text(
            f"Выбран список интервалов {input}")
        return SET_DICT_ATTR
    else:
        await update.message.reply_text(f"Введен некорректный символ <{input}>")
        return SEL_INTERVAL_LIST
# dict_attr
async def confirm_dict(update: Update, context: CustomContext):
    language = await Repository.get_or_create_language(
        context.custom_user_data.language.validate()
    )
    del context.custom_user_data.language
    context.custom_user_data.set_dictionary(language_id=language.id)
    dictionary = await Repository.get_dictionary(
            user_id=context.custom_user_data.dictionary.user_id,
            language_id=context.custom_user_data.dictionary.language_id,
    )
    if dictionary:
        await update.message.reply_text("Уже существует такой словарь!")
    else:
        dictionary = await Repository.create_dictionary(
            context.custom_user_data.dictionary.validate())
        await update.message.reply_text("Словарь создан!")
    context.custom_user_data.dialog_active = False
    return LOOP

async def change_word(update: Update, context: CustomContext):
    if not context.custom_user_data.dictionary.id:
        await update.message.reply_text("Не выбран словарь!")
        return LOOP
    context.custom_user_data.dialog_active = True
    await update.message.reply_text("Введите слово, которое планируете изменить:")
    return INP_SEARCH_VALUE_CH
# inp_search_value_ch
async def input_search_value_ch(update: Update, context: CustomContext):
    searched_word = update.message.text.strip()
    if searched_word:
        await update.message.reply_text(
            f"Поиск {searched_word} в базе данных...")
        DTO = await Repository.get_word_translations_inf(
                searched_word,
                context.custom_user_data.dictionary.id,
        )
        if DTO:
            await update.message.reply_text(
                "Найдена информация:\n"
                f"  Слово: {searched_word}\n  Переводы: {DTO["translations"]}\n"
                f"  Примечание: {DTO["note"] if DTO["note"] else ''}\n"
                f"  Длительность: {DTO["interval"]}\n  Счетчик: {DTO["count"]}"
            )
            context.custom_user_data.set_old_word(content=searched_word)
            context.custom_user_data.word = context.custom_user_data.old_word
            context.custom_user_data.translations_contents = DTO["translations"]
            if DTO["note"]:
                context.custom_user_data.set_note(content=DTO["note"])
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
async def reset_word(update: Update, context: CustomContext):
    await update.message.reply_text("Введите исправленное слово: ")
    return INP_WORD_CH
# inp_word_ch
async def input_word_ch(update: Update, context: CustomContext):
    word = update.message.text.strip()
    if word:
        del context.custom_user_data.word
        context.custom_user_data.set_word(content=word)
        await update.message.reply_text(
            f"Введено слово: {context.custom_user_data.word.content}."
        )
        return RESET_WORD_ATTR
    else:
        await update.message.reply_text(
            "Неверный формат слова. Введите иначе:")
        return INP_WORD_CH
# reset_word_attr
async def reset_translate(update: Update, context: CustomContext):
    await update.message.reply_text(
        "Введите исправленный перевод или "
        "несколько переводов через запятую: "
        )
    return INP_TRANSLATE_CH
# inp_translate_ch
async def input_translate_ch(update: Update, context: CustomContext):
    translations = update.message.text.strip()
    if translations:
        del context.custom_user_data.translations
        context.custom_user_data.translations_contents = [
                translate.strip()
                for translate
                in translations.split(',')
            ]
        await update.message.reply_text(
            f"Введены переводы: {context.custom_user_data.translations_contents}."
        )
        return RESET_WORD_ATTR
    else:
        await update.message.reply_text(
            "Неверный формат введенный переводов. Введите иначе:")
        return INP_TRANSLATE_CH
# reset_word_attr
async def reset_note(update: Update, context: CustomContext):
    await update.message.reply_text("Введите исправленное примечание: ")
    return INP_NOTE_CH
# inp_note_ch
async def input_note_ch(update: Update, context: CustomContext):
    note = update.message.text
    if note:
        del context.custom_user_data.note
        context.custom_user_data.set_note(content=note)
        await update.message.reply_text(
            f"Введено примечание: {context.custom_user_data.note.content}.")
        return RESET_WORD_ATTR
    else:
        await update.message.reply_text(
            "Неверный формат примечания. Введите иначе:")
        return INP_NOTE_CH
# reset_word_attr
async def confirm_changed_word(update: Update, context: CustomContext):
    # Удаляем старые Word_Translations
    await Repository.delete_word_translations(
            context.custom_user_data.dictionary.id,
            context.custom_user_data.old_word.content,
    )
    del context.custom_user_data.old_word
    # Записываем новые
    context.custom_user_data.set_word_translate(
        dictionary_id=context.custom_user_data.dictionary.id,)
    word = await Repository.get_or_create_word(
        context.custom_user_data.word.validate())
    del context.custom_user_data.word
    if context.custom_user_data.note:
        note = await Repository.get_or_create_note(
            context.custom_user_data.note.validate())
        del context.custom_user_data.note
        context.custom_user_data.set_word_translate(note_id=note.id)
    translations = await Repository.get_or_create_translations(
        context.custom_user_data.valid_translations)
    context.custom_user_data.set_word_translate(
        word_id=word.id,
        translate_ids=[translate.id for translate in translations],
            interval_id=1,
            count = 0,
    )
    del context.custom_user_data.translations
    await Repository.create_word_translations(
        context.custom_user_data.word_translate.validate())
    del context.custom_user_data.word_translate
    await update.message.reply_text("Записано успешно.")
    context.custom_user_data.dialog_active = False
    return LOOP

async def delete_word(update: Update, context: CustomContext):
    if not context.custom_user_data.dictionary.id:
        await update.message.reply_text("Не выбран словарь!")
        return LOOP
    context.custom_user_data.dialog_active = True
    await update.message.reply_text("Введите слово, которое планируете удалить:")
    return INP_SEARCH_VALUE_DEL
# inp_search_value_del
async def input_search_value_del(update: Update, context: CustomContext):
    searched_word = update.message.text.strip()
    if searched_word:
        await update.message.reply_text(
            f"Поиск {searched_word} в базе данных...")
        DTO = await Repository.get_word_translations_inf(
                searched_word,
                context.custom_user_data.dictionary.id,
        )
        if DTO:
            context.custom_user_data.set_word(content=searched_word)
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
async def confirm_del(update: Update, context: CustomContext):
    await update.message.reply_text(
        f"Удаление {context.custom_user_data.word.content}...")
    await Repository.delete_word_translations(
            context.custom_user_data.dictionary.id,
            context.custom_user_data.word.content,
    )
    del context.custom_user_data.word
    await update.message.reply_text("Удалено.")
    context.custom_user_data.dialog_active = False
    return LOOP
# confirm_del
async def revoke_del(update: Update, context: CustomContext):
    del context.custom_user_data.word
    await update.message.reply_text("Отмена удаления...")
    context.custom_user_data.dialog_active = False
    return LOOP
# loop
async def select_dict(update: Update, context: CustomContext):
    context.custom_user_data.dialog_active = True
    dictionaries = await Repository.get_dictionaries(
        context.custom_user_data.dictionary.user_id)
    if dictionaries:
        context.custom_user_data.dictionary_ids = [
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
async def input_selected_dict(update: Update, context: CustomContext):
    input = update.message.text
    if input.isnumeric():
        context.custom_user_data.dictionary.id = context.custom_user_data.dictionary_ids[int(input) - 1]
        del context.custom_user_data.dictionary_ids
        await update.message.reply_text(f"Выбран словарь {input}")
        context.custom_user_data.dialog_active = False
        return LOOP
    else:
        await update.message.reply_text(f"Введен некорректный символ <{input}>")
        return SEL_DICT
# loop
async def about(update: Update, context: CustomContext):
    await update.message.reply_text(
        "Berber learn v.0.2-pre_alpha\n"
        "Доступны команды:\n"
        "/add_word\n"
        "/ch_word\n"
        "/del_word\n"
        "/add_dict\n"
        "/sel_dict\n"
        "/start_event\n"
        "/about\n"
        "/settings\n"
        "/cancel"
        )
    return LOOP
# loop
async def settings(update: Update, context: CustomContext):
    await update.message.reply_text("Здесь пока ничего нет, но вы ждите.")
    return LOOP
# loop
async def test(update: Update, context: CustomContext):
    await update.message.reply_text("Здесь пока ничего нет, но вы ждите.")
    return LOOP
# loop
async def send_word(update: Update, context: CustomContext):
    ud = context.custom_user_data
    ud.dialog_active = True
    # Активация диалога, чтоб напоминание не пришло,
    # если пользователь активировал диалог до напоминания
    ud.done_event = not ud.done_event
    if not isinstance(
        ud.word_translations_order, Iterable):
        ud.word_translations_order = convert_tree_to_generator(
            convert_to_tree(
                await Repository.update_word_translations_count(
                    ud.dictionary.user_id
                )
            )
        )
    return await _send_word(update, context)

async def _send_word(update: Update, context: CustomContext):
    ud = context.custom_user_data
    if ud.current_element:
        if ud.current_element.dictionary_name != ud.current_dictionary:
            ud.current_dictionary = ud.current_element.dictionary_name
            await update.message.reply_text(
                f"Словарь {ud.current_dictionary}.")
        if ud.current_element.word_name != ud.current_word:
            ud.current_word = ud.current_element.word_name
            await update.message.reply_text(
                f"Введите перевод для {ud.current_word}:")
        else:
            await update.message.reply_text("Введите другой перевод:")
        return MESSAGE_TRANSLATE
    else:
        await update.message.reply_text("На сегодня всё.")
        del context.custom_user_data.word_translations_order
        context.custom_user_data.dialog_active = False
        return LOOP

# message_translate
async def send_translate(update: Update, context: CustomContext):
    ud = context.custom_user_data
    ud.choice_count -= 1
    # Обработка ввода
    if update.message.text in ud.current_element.translations:
        await update.message.reply_text("Верно.")
        word_translate = ud.current_element.translations.pop(update.message.text)
        await Repository.update_word_translate_interval_up(*word_translate)
    else:
        await update.message.reply_text("Ошибка.")
    # Обработка неверных ответов и обнуление current_element
    # Это необходимо для того, чтобы следующий элемент был получен через next
    if not ud.choice_count:
        if ud.current_element.translations:
            text = "Правильные переводы:\n"
            message = await update.message.reply_text(text)
            for translate, word_translate in ud.current_element.translations.items():
                text += f"{translate}\n"
                message = await message.edit_text(text)
                await Repository.update_word_translate_interval_down(
                    *word_translate[:-1])
        del ud.current_element
    return await _send_word(update, context)

# events
async def repetition_reminder(context: CustomContext) -> None:
    count = 23
    while count:
        if context.custom_user_data.done_event:
            context.custom_user_data.done_event = False
            break
        else:
            if context.custom_user_data.dialog_active:
                await asyncio.sleep(60**2)
            else:
                await context.bot.send_message(
                    context.chat_id,
                    "Ежедневное напоминание о повторении слов.\n"
                    "Введите /start_event, чтоб начать."
                )
                break
        count -= 1
    return None

# loop
async def stop(update: Update, context: CustomContext):
    await update.message.reply_text('Завершение работы...')
    context.custom_user_data.clear()
    return END
