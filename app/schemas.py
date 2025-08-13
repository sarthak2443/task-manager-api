from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class TaskCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(load_default="")
    completed = fields.Boolean(load_default=False)

class TaskUpdateSchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String()
    completed = fields.Boolean()

class TaskOutSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    completed = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime(allow_none=True)
    owner_id = fields.Int()
