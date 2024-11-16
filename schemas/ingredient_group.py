from marshmallow import Schema, fields

from schemas.ingredient import IngredientSchema

class IngredientGroupSchema(Schema):
    id = fields.Int(required=True)
    group_name = fields.Str(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    ingredients = fields.List(fields.Nested(IngredientSchema))