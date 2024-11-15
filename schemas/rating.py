from marshmallow import Schema, fields

class RatingSchema(Schema):
    id = fields.Int(dump_only=True)
    users_id = fields.Int(required=True)
    recipe_id = fields.Int(required=True)
    rating_value = fields.Int(required=True)

class AddRatingSchema(Schema):
    users_id = fields.Int(required=True)
    rating_value = fields.Int(required=True)
