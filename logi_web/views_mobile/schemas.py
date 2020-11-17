from marshmallow import Schema, fields

from logi_web.schemas import VehicleSchema, DriverSchema


class ChangePassWordSchema(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class SendPasswordSchema(Schema):
    email = fields.Email(required=True)


class LogEditReqestSchema(Schema):
    driver_id = fields.Int(required=True)


class VehicleRequestSchema(Schema):
    driver_id = fields.Int(required=True)
    status = fields.Int(required=True)


class VehicleConfirmationSchema(Schema):
    vehicles = fields.Nested(VehicleSchema(many=True))
    driver = fields.Nested(DriverSchema(many=False))


log_edit_request_schema = LogEditReqestSchema()
change_password_schema = ChangePassWordSchema()
login_schema = LoginSchema()
send_password_schema = SendPasswordSchema()
vehicle_request_schema = VehicleRequestSchema()
