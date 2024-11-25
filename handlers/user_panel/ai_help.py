from aiogram import F, Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filter.chat_types import ChatTypeFilter, IsAdmin
from handlers.ai_function import sent_prompt_and_get_response
from handlers.user_panel.start_functions import user_preferences
from keyboard.inline import start_functions_keyboard, language_selection_keyboard, get_cancel_keyboard, \
    get_cancel_ai_help_keyboard
from message_text.text import chat_messages as messages, cancel

ai_help_private_router = Router()
ai_help_private_router.message.filter(ChatTypeFilter(['private']))


class AiAssistanceState(StatesGroup):
    WaitingForReview = State()


@ai_help_private_router.callback_query(F.data.startswith("ai_help"))
async def send_review_request_callback_query(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')

    await query.message.edit_caption(
        caption=messages[language]['ai_help_message'],
        reply_markup=get_cancel_keyboard(language)
    )
    await state.set_state(AiAssistanceState.WaitingForReview)


@ai_help_private_router.callback_query(F.data == "cancel_ai_help")
async def cancel_feedback(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')
    await query.message.edit_caption(
        caption=messages[language]['request_canceled'],
        reply_markup=get_cancel_ai_help_keyboard(language)
    )
    await state.clear()


@ai_help_private_router.message(AiAssistanceState.WaitingForReview)
async def process_help_request(message: types.Message, state: FSMContext, bot: Bot):
    language = user_preferences.get(message.from_user.id, {}).get('language', 'ru')

    if message.text:
        generated_help = sent_prompt_and_get_response(message.text)
        await state.clear()
        await message.answer(generated_help, reply_markup=start_functions_keyboard(language))
    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=cancel[language], callback_data="cancel_create_feedback"))
        await message.answer(messages[language]['city_not_found'], reply_markup=keyboard)