from marshmallow import Schema, fields


class UserSchema(Schema):

    id = fields.Integer()
    username = fields.String()
    is_admin = fields.Boolean()
    is_delete = fields.Boolean()
    phone = fields.String()
    real_name = fields.String()
    id_card = fields.String()
    avatar_url = fields.String()

    start_time = fields.DateTime()
    update_time = fields.DateTime()

