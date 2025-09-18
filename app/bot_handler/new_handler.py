import datetime
import asyncio
from typing import Iterable

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from app.bot_handler import conditions as cnds
from app.models import models
from app.repository import ConnectedRepository as Repository
from app.DTO import Valid_User, convert_to_tree, convert_tree_to_generator
from app.bot_handler.CustomContext import CustomContext

def one_button_kwd(text_for_button: str, callback_data: str) -> InlineKeyboardMarkup:
    """callback клавиатура с одной кнопкой."""
    return InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text_for_button, callback_data=callback_data))

async def start(update: Update, context: CustomContext):
    user = await Repository.get_or_create_user(
        Valid_User(telegram_id=context.user_id))
    context.custom_user_data.set_dictionary(user_id=user.id)
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
    return await start_headline(update, context, True)

async def start_headline(update: Update, context: CustomContext, start_over: bool = False):
    buttons = [
        [
            InlineKeyboardButton("Добавить слово", callback_data=cnds.R_ADD_WORD),
            InlineKeyboardButton("Искать слово", callback_data=cnds.R_SEARCH_WORD),
        ],
        [
            InlineKeyboardButton("Начать повторение", callback_data=cnds.R_START_REPETITION),
        ],
        [
            InlineKeyboardButton("Создать словарь", callback_data=cnds.R_ADD_DICT),
            InlineKeyboardButton("Выбрать словарь", callback_data=cnds.R_SEL_DICT),
        ],
        [
            InlineKeyboardButton("О приложении", callback_data=cnds.R_ABOUT),
            InlineKeyboardButton("Настройки", callback_data=cnds.R_SETTINGS),
        ],
    ]
    if start_over:
        await update.message.reply_text(
            "Привет. Действуй.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await update.callback_query.answer()
        if context.custom_user_data.dictionary.id:
            text = f"Активный словарь: {context.custom_user_data.dictionary.language_represent}"
        else:
            text = "Словарь не выбран."
        await update.callback_query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(buttons))
    return cnds.C_ACTION
    

async def set_dictionary_attr(update: Update, context: CustomContext, start_over: bool = False):
    ud = context.custom_user_data
    ud.dialog_active = True
    buttons = [
        [
            InlineKeyboardButton("Установить основной язык", callback_data=cnds.R_MAIN_LANGUAGE),
            InlineKeyboardButton("Установить язык перевода", callback_data=cnds.R_TRANSLATE_LANGUAGE),
        ],
        [
            InlineKeyboardButton("Установить интервалы повторения (опционально)", callback_data=cnds.R_INTERVAL_LIST),
        ],
        [
            InlineKeyboardButton("Записать", callback_data=cnds.R_CONFIRM_DICT),
            InlineKeyboardButton("Отмена", callback_data=cnds.R_CANCEL),
        ],
    ]
    if start_over:
        text = (
            "Вы в меню добавления атрибутов словаря.\n"
            f"{f'Добавленная информация:\n'
                if ud.dictionary.interval_list_id
                or ud.language.main_language
                or ud.language.translation_language
                else 'Ничего не добавлено.'}"
            f"{f"Основной язык: {ud.language.main_language}\n"
                if ud.language.main_language
                else ''}"
            f"{f"Язык перевода: {ud.language.translation_language}\n"
                if ud.language.translation_language
                else ''}"
            f"{f'Список интервалов: {"classic"}'
                if ud.dictionary.interval_list_id
                else ''}"
        )
        await update.message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Вы в меню добавления атрибутов словаря.\n",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    return cnds.C_SET_DICT_ATTR

async def set_main_language(update: Update, context: CustomContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Введите название основного языка.\n"
        "(Например, для англо-русского словаря это \"Английский\").\n"
        "Используйте любые удобные названия кроме пустого.)",
        reply_markup=one_button_kwd("Отмена", cnds.R_CANCEL),
        )
    return cnds.C_INP_MAIN_LANGUAGE
# inp_main_language
async def input_main_language(update: Update, context: CustomContext):
    main_language = update.message.text
    if main_language:
        context.custom_user_data.set_language(main_language=main_language.strip())
        return await set_dictionary_attr(update, context, True)
    else:
        await update.message.reply_text(
            "Название пустое. Введите иное:",
            reply_markup=one_button_kwd("Отмена", cnds.R_CANCEL),
        )
        return cnds.C_INP_MAIN_LANGUAGE
# dict_attr
async def set_translation_language(update: Update, context: CustomContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Введите название языка перевода.\n"
        "(Например, для англо-русского словаря это \"Русский\").\n"
        "Используйте любые удобные названия кроме пустого.",
        reply_markup=one_button_kwd("Отмена", cnds.R_CANCEL),
        )
    return cnds.C_INP_TRANSLATE_LANGUAGE
# inp_translate_language
async def input_translation_language(update: Update, context: CustomContext):
    translation_language = update.message.text
    if translation_language:
        context.custom_user_data.set_language(
            translation_language=translation_language.strip())
        return await set_dictionary_attr(update, context, True)
    else:
        await update.message.reply_text(
            "Название пустое. Не подходит.",
            reply_markup=one_button_kwd("Отмена", cnds.R_CANCEL),
        )
        return cnds.C_INP_TRANSLATE_LANGUAGE
# dict_attr
async def sel_interval_list(update: Update, context: CustomContext):
    await update.callback_query.answer()
    text = "Введите номер списка интервалов из представленных ниже.\n"
    interval_lists = await Repository.get_interval_lists_by_user(
        context.custom_user_data.dictionary.user_id)
    context.custom_user_data.interval_ids = [
        interval_list.id
        for interval_list
        in interval_lists
    ]
    for idx, interval_list in enumerate(interval_lists):
        text += f"{idx + 1}: {interval_list.name}\n"
    await update.callback_query.edit_message_text(
        text,
        reply_markup=one_button_kwd("Отмена", cnds.R_CANCEL),
    )
    return cnds.C_SEL_INTERVAL_LIST
# sel_interval_list
async def select_list_interval(update: Update, context: CustomContext):
    input = update.message.text
    if input.isnumeric():
        context.custom_user_data.set_dictionary(
            interval_list_id=context.custom_user_data.interval_ids[int(input) - 1]
        )
        del context.custom_user_data.interval_ids
        return await set_dictionary_attr(update, context, True)
    else:
        await update.message.reply_text(
            f"Введен некорректный символ <{input}>",
            reply_markup=one_button_kwd("Отмена", cnds.R_CANCEL),
        )
        return cnds.C_SEL_INTERVAL_LIST
# dict_attr
async def confirm_dict(update: Update, context: CustomContext):
    await update.callback_query.answer()
    language = await Repository.get_or_create_language(
        context.custom_user_data.language.validate())
    context.custom_user_data.set_dictionary(
        language_represent=f"{context.custom_user_data.language.main_language}"
        f", {context.custom_user_data.language.translation_language}"
    )
    del context.custom_user_data.language
    context.custom_user_data.set_dictionary(language_id=language.id)
    dictionary = await Repository.get_dictionary(
        user_id=context.custom_user_data.dictionary.user_id,
        language_id=context.custom_user_data.dictionary.language_id,
    )
    if dictionary:
        await update.callback_query.edit_message_text(
            "Такой словарь уже существует.",
            reply_markup=one_button_kwd("Ясно", cnds.R_CONFIRM),
        )
    else:
        if not hasattr(context.custom_user_data.dictionary, "interval_list_id"):
            interval_list = await Repository.get_interval_list(name="classic")
            context.custom_user_data.set_dictionary(
                interval_list_id = interval_list.id)
        dictionary = await Repository.create_dictionary(
            context.custom_user_data.dictionary.validate())
        await update.callback_query.edit_message_text(
            "Словарь создан.",
            reply_markup=one_button_kwd("Ясно", cnds.R_CONFIRM),
        )
        if not context.custom_user_data.dictionary.id:
            context.custom_user_data.set_dictionary(id=dictionary.id)
    context.custom_user_data.dialog_active = False
    return cnds.C_EMPTY

async def select_dictionary(update: Update, context: CustomContext):
    ...

async def set_word_attr(update: Update, context: CustomContext):
    ...

async def search_word(update: Update, context: CustomContext):
    ...

async def start_repetition(update: Update, context: CustomContext):
    ...

async def cancel(update: Update, context: CustomContext):
    return await start_headline(update, context)

async def confirm(update: Update, context: CustomContext):
    return await start_headline(update, context)

# loop
async def about(update: Update, context: CustomContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Berber learn v.0.2-beta\n"
        "Это приложение создано для расширения словарного запаса "
        "при изучении иностранных языков.\n",
        reply_markup=one_button_kwd("Ясно", cnds.R_CONFIRM)
    )
    return cnds.C_EMPTY
# loop
async def settings(update: Update, context: CustomContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Здесь пока ничего нет.",
        reply_markup=one_button_kwd("Ясно", cnds.R_CONFIRM)
    )
    return cnds.C_EMPTY

async def stop(update: Update, context: CustomContext) -> None:
    await update.message.reply_text('Завершение работы...')
    context.custom_user_data.clear()
    return cnds.R_END

# events
async def repetition_reminder(context: CustomContext) -> None:
    ...