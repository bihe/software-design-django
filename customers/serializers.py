# Serializer for the Django customer model
from marshmallow import Schema, fields


class CustomerSerializer(Schema):
    username: fields.Str = fields.Str()
