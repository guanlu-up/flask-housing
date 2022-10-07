from marshmallow import Schema, fields


class CityAreaSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class FacilitySchema(Schema):
    id = fields.Integer()
    name = fields.String()


class HouseImageSchema(Schema):
    id = fields.Integer()
    url = fields.String()


class HouseSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    price = fields.Integer()
    address = fields.String()
    room_count = fields.Integer()
    acreage = fields.Integer()
    unit = fields.String()
    capacity = fields.Integer()
    beds = fields.String()
    deposit = fields.Integer()
    min_days = fields.Integer()
    max_days = fields.Integer()
    order_count = fields.Integer()
    image_url = fields.String()

    facilities = fields.List(fields.Nested(FacilitySchema()))
