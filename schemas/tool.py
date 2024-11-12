from marshmallow import Schema, fields

class ToolSchema(Schema):
    id = fields.Int(dump_only=True)
    recipe_id = fields.Str(required=True)
    nama_alat = fields.Str(required=True)