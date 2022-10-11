from marshmallow import Schema, fields


class UserSchema(Schema):

    id = fields.Integer()
    username = fields.String()
    is_admin = fields.Boolean()
    phone = fields.String()
    avatar_url = fields.String()
    start_time = fields.DateTime("%Y-%m-%d %H:%M:%S")


class UserFullSchema(UserSchema):
    update_time = fields.DateTime("%Y-%m-%d %H:%M:%S")
    real_name = fields.String()
    id_card = fields.String()
    is_delete = fields.Boolean()
