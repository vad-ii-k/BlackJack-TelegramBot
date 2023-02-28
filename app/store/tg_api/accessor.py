import typing
from typing import Optional

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.tg_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class TgApiAccessor(BaseAccessor):
    API_PATH = "https://api.telegram.org/"

    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.poller: Optional[Poller] = None
        self.offset: Optional[int] = None

    async def connect(self, app: "Application"):
        self.session = ClientSession(connector=TCPConnector())
        self.poller = Poller(app.store)
        self.logger.info("start polling")
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()
        if self.poller:
            await self.poller.stop()

    def _build_query(self, method: str, params: dict = None) -> str:
        if params is None:
            params = dict()
        url = f"{self.API_PATH}bot{self.app.config.bot.token}/" + method + "?"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def poll(self):
        async with self.session.get(
            self._build_query(
                method="getUpdates",
                params={
                    "offset": self.offset,
                    "timeout": 30,
                },
            )
        ) as resp:
            data = (await resp.json())["result"]
            if len(data) > 0:
                self.offset = data[-1]["update_id"] + 1
            self.logger.info(data)
