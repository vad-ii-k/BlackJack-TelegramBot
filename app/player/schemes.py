from marshmallow import Schema, fields


class PlayerResponseSchema(Schema):
    tg_id = fields.Int(required=True)
    balance = fields.Int(required=True)
    games_played = fields.Int(required=True)
    games_won = fields.Int(required=True)
    games_lost = fields.Int(required=True)
