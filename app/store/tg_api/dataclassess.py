from dataclasses import dataclass
from typing import Optional


@dataclass
class InlineKeyboardButton:
    text: str
    callback_data: str


@dataclass
class InlineKeyboardMarkup:
    inline_keyboard: list[list[InlineKeyboardButton]]


@dataclass
class Message:
    chat_id: int
    text: str
    message_id: int = None
    reply_markup: Optional[InlineKeyboardMarkup] = None


@dataclass
class User:
    id: int
    first_name: str
    username: str


@dataclass
class Chat:
    id: int


@dataclass
class MessageUpdate:
    message_id: int
    from_user: User
    chat: Chat
    text: str


@dataclass
class MyChatMemberUpdate:
    chat: Chat
    new_chat_member: User


@dataclass
class CallbackQuery:
    id: int
    from_user: User
    message: Message
    data: str


@dataclass
class AnswerCallbackQuery:
    id: int
    text: str
    show_alert: bool = False


@dataclass
class Update:
    message: Optional[MessageUpdate] = None
    my_chat_member: Optional[MyChatMemberUpdate] = None
    callback_query: Optional[CallbackQuery] = None
