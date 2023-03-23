from aiohttp_apispec import docs, response_schema

from app.auth.decorators import auth_required
from app.player.dataclasses import Player
from app.player.schemes import PlayerResponseSchema
from app.web.app import View
from app.web.utils import json_response


class PlayerView(View):
    @auth_required
    @docs(tags=["player"], summary="Get info about player")
    @response_schema(PlayerResponseSchema, 200)
    async def get(self):
        tg_id = int(self.request.match_info.get("tg_id"))

        player_db = await self.store.game.get_player(tg_id)
        player_stats_db = await self.store.game.get_player_statistics(tg_id)

        player = Player.from_db(player_db, player_stats_db)
        return json_response(data=PlayerResponseSchema().dump(player))
