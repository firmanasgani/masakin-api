from marshmallow import Schema, fields

class CategorySchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
