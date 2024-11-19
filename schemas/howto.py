from marshmallow import Schema, fields

from schemas.how_to_cook_image import HowToCookImageSchema

class HowToCookSchema(Schema):
    id = fields.Int(dump_only=True)
    recipe_id = fields.Int(required=True)
    steps = fields.Int(required=True)
    description = fields.Str(required=True)
    
    images = fields.List(fields.Nested(HowToCookImageSchema))