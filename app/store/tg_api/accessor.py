import typing
from dataclasses import asdict
from json import dumps
from typing import Optional

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.tg_api.dataclassess import (
    AnswerCallbackQuery,
    CallbackQuery,
    Chat,
    InlineKeyboardMarkup,
    Message,
    MessageUpdate,
    MyChatMemberUpdate,
    Update,
    User,
)
from app.store.tg_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class TgApiAccessor(BaseAccessor):
    API_PATH = "https://api.telegram.org/"

    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.poller: Optional[Poller] = None
        self.offset: Optional[int] = 0
        self.server_url: Optional[str] = None

    async def connect(self, app: "Application"):
        self.session = ClientSession(connector=TCPConnector())
        self.poller = Poller(app.store)
        self.server_url = f"{self.API_PATH}bot{self.app.config.bot.token}/"
        self.logger.info("start polling")
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()
        if self.poller:
            await self.poller.stop()

    async def poll(self) -> list[Update]:
        async with self.session.get(
            url=self.server_url + "getUpdates",
            params={
                "offset": self.offset,
                "timeout": 30,
            },
        ) as resp:
            data = (await resp.json())["result"]
            if len(data) > 0:
                self.offset = data[-1]["update_id"] + 1
            self.logger.info(data)
            return self._pack_updates(data)

    async def send_message(self, message: Message) -> None:
        async with self.session.get(
            url=self.server_url + "sendMessage",
            params={
                "chat_id": message.chat_id,
                "text": message.text,
                "reply_markup": dumps(asdict(message.reply_markup)),
                "parse_mode": "HTML",
            },
        ) as resp:
            data = await resp.json()
            self.logger.info(data)

    async def edit_message(self, message: Message) -> None:
        async with self.session.get(
            url=self.server_url + "editMessageText",
            params={
                "chat_id": message.chat_id,
                "message_id": message.message_id,
                "text": message.text,
                "reply_markup": dumps(asdict(message.reply_markup)),
            },
        ) as resp:
            data = await resp.json()
            self.logger.info(data)

    async def answer_callback_query(self, answer: AnswerCallbackQuery) -> None:
        async with self.session.get(
            url=self.server_url + "answerCallbackQuery",
            params={
                "callback_query_id": answer.id,
                "text": answer.text,
                "show_alert": dumps(answer.show_alert),
            },
        ) as resp:
            data = await resp.json()
            self.logger.info(data)

    @staticmethod
    def _pack_updates(raw_updates: dict) -> list[Update]:
        updates = []
        for raw_update in raw_updates:
            update = Update()
            if message := raw_update.get("message", None):
                update = Update(
                    message=MessageUpdate(
                        message_id=message["message_id"],
                        from_user=User(
                            id=message["from"]["id"],
                            first_name=message["from"]["first_name"],
                            username=message["from"]["username"],
                        ),
                        chat=Chat(id=message["chat"]["id"]),
                        text=message.get("text", None),
                    )
                )
            elif callback_query := raw_update.get("callback_query", None):
                update = Update(
                    callback_query=CallbackQuery(
                        id=callback_query["id"],
                        from_user=User(
                            id=callback_query["from"]["id"],
                            first_name=callback_query["from"]["first_name"],
                            username=callback_query["from"]["username"],
                        ),
                        message=Message(
                            chat_id=callback_query["message"]["chat"]["id"],
                            text=callback_query["message"]["text"],
                            message_id=callback_query["message"]["message_id"],
                            reply_markup=InlineKeyboardMarkup(
                                **callback_query["message"]["reply_markup"]
                            ),
                        ),
                        data=callback_query["data"],
                    )
                )
            elif my_chat_member := raw_update.get("my_chat_member", None):
                update = Update(
                    my_chat_member=MyChatMemberUpdate(
                        chat=Chat(id=my_chat_member["chat"]["id"]),
                        new_chat_member=User(
                            id=my_chat_member["from"]["id"],
                            first_name=my_chat_member["from"]["first_name"],
                            username=my_chat_member["from"]["username"],
                        ),
                    )
                )
            updates.append(update)
        return updates
