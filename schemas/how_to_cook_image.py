from marshmallow import Schema, fields

class HowToCookImageSchema(Schema):
    id = fields.Int(dump_only=True)
    howtocook_id = fields.Int(required=True)
    img_url = fields.Str(required=True)
    uploaded_at = fields.DateTime(dump_only=True)

    # howtocook = fields.Nested('HowToCookSchema', only=('id', 'steps', 'description'))
