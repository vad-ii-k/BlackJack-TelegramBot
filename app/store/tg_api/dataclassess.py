from pydantic import BaseModel, Field


class InlineKeyboardButton(BaseModel):
    text: str
    callback_data: str


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: list[list[InlineKeyboardButton]]


class Chat(BaseModel):
    id: int


class Message(BaseModel):
    chat: Chat
    text: str
    message_id: int | None = None
    reply_markup: InlineKeyboardMarkup | None = None


class User(BaseModel):
    id: int
    first_name: str
    username: str


class MessageUpdate(BaseModel):
    message_id: int
    from_user: User = Field(alias="from")
    chat: Chat
    text: str | None = None


class ChatMember(BaseModel):
    user = User


class MyChatMemberUpdate(BaseModel):
    chat: Chat
    new_chat_member: ChatMember


class CallbackQuery(BaseModel):
    id: int
    from_user: User = Field(alias="from")
    message: Message
    data: str


class AnswerCallbackQuery(BaseModel):
    id: int
    text: str
    show_alert: bool = False


class Update(BaseModel):
    message: MessageUpdate | None = None
    my_chat_member: MyChatMemberUpdate | None = None
    callback_query: CallbackQuery | None = None
