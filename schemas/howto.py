from marshmallow import Schema, fields

class HowToCookSchema(Schema):
    id = fields.Int(dump_only=True)
    recipe_id = fields.Int(required=True)
    steps = fields.Int(required=True)
    description = fields.Str(required=True)
    img_urls = fields.Str()