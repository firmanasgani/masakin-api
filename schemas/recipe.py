from marshmallow import Schema, fields

from schemas.category import CategorySchema
from schemas.ingredient import IngredientSchema
from schemas.ingredient_group import IngredientGroupSchema
from schemas.tool import ToolSchema

class RecipeSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    img_banner = fields.Str()
    description = fields.Str()
    video_url = fields.Str()
    difficulty = fields.Int(required=True)
    estimated_time = fields.Str(required=True)
    created_at = fields.DateTime()
    ingredient_groups = fields.List(fields.Nested(IngredientGroupSchema))
    tools = fields.List(fields.Nested(ToolSchema))
    category = fields.Nested(CategorySchema)