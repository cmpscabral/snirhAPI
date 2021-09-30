from marshmallow import Schema, fields


class DataQuerySchema(Schema):
    station = fields.Integer(required=True)
    parameter = fields.Integer(required=True)
    tmin = fields.Date(required=True)
    tmax = fields.String(required=True)
