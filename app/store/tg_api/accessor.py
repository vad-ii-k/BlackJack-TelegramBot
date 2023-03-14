import json
import typing

from aiohttp import TCPConnector
from aiohttp.client import ClientSession
from pydantic import ValidationError, parse_obj_as

from app.base.base_accessor import BaseAccessor
from app.store.tg_api.dataclassess import (
    AnswerCallbackQuery,
    Message,
    MessageUpdate,
    Update,
)
from app.store.tg_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class TgApiAccessor(BaseAccessor):
    API_PATH = "https://api.telegram.org/"

    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.poller: Poller | None = None
        self.offset: int = 0
        self.server_url: str | None = None

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
                "allowed_updates": [
                    "message",
                    "callback_query",
                    "my_chat_member",
                ],
            },
        ) as resp:
            data = await resp.json()
            self.logger.info(data)
            result = data.get("result", [])
            if result:
                self.offset = result[-1]["update_id"] + 1
            try:
                return parse_obj_as(list[Update], result)
            except ValidationError as err:
                self.logger.error(err)
                return []

    async def send_message(self, message: Message) -> MessageUpdate:
        async with self.session.get(
            url=self.server_url + "sendMessage",
            params={
                "chat_id": message.chat.id,
                "text": message.text,
                "reply_markup": message.reply_markup.json(),
                "reply_to_message_id": json.dumps(message.reply_to_message_id),
                "parse_mode": "HTML",
                "disable_web_page_preview": "true",
            },
        ) as resp:
            data = await resp.json()
            self.logger.info(data)
            try:
                return parse_obj_as(MessageUpdate, data.get("result", {}))
            except ValidationError as err:
                self.logger.error(err)

    async def edit_message(self, message: Message) -> None:
        async with self.session.get(
            url=self.server_url + "editMessageText",
            params={
                "chat_id": message.chat.id,
                "message_id": message.message_id,
                "text": message.text,
                "reply_markup": message.reply_markup.json(),
                "parse_mode": "HTML",
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
                "show_alert": str(answer.show_alert),
                "cache_time": 1,
            },
        ) as resp:
            data = await resp.json()
            self.logger.info(data)
