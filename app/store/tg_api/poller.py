import asyncio
from asyncio import Task

from app.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Task | None = None

    async def start(self):
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        self.is_running = False
        await self.poll_task

    async def poll(self):
        while self.is_running:
            updates = await self.store.tg_api.poll()
            await self.store.bots_manager.handle_updates(updates)
            if updates:
                await asyncio.sleep(0.5)
