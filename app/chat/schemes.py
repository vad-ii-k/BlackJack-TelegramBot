from marshmallow import Schema, fields


class ChatResponseSchema(Schema):
    chat_id = fields.Int(required=True)
    games_played = fields.Int(required=True)
    game_is_active = fields.Bool(required=True)
