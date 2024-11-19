from marshmallow import Schema, fields

class IngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    recipe_id = fields.Str(required=True)
    nama_bahan = fields.Str(required=True)
    image = fields.Str(required=True)
    description = fields.Str(required=True)
    takaran = fields.Str(required=True)
