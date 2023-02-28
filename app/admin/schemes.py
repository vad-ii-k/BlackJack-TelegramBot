from marshmallow import Schema, fields


class AdminResponseSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)


class AdminAuthRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
