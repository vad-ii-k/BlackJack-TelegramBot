from aiohttp_apispec import docs, response_schema

from app.auth.decorators import auth_required
from app.chat.dataclasses import Chat
from app.chat.schemes import ChatResponseSchema
from app.web.app import View
from app.web.utils import json_response


class ChatView(View):
    @auth_required
    @docs(tags=["chat"], summary="Get info about chat")
    @response_schema(ChatResponseSchema, 200)
    async def get(self):
        chat_id = int(self.request.match_info.get("chat_id"))

        active_game = await self.store.game.get_active_game(chat_id)
        games_played = await self.store.game.get_num_of_games_played_in_chat(
            chat_id=chat_id
        )

        chat = Chat(chat_id, games_played, active_game is not None)
        return json_response(data=ChatResponseSchema().dump(chat))
