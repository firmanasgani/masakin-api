from marshmallow import Schema, fields

class RecipeSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    img_banner = fields.Str()
    country = fields.Str()
    description = fields.Str()
    video_url = fields.Str()
    difficulty = fields.Int(required=True)
    estimated_time = fields.Str(required=True)
    created_at = fields.DateTime()