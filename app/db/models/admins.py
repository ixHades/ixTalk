from tortoise.models import Model
from tortoise import fields
from app.db.enums import AdminRole


class Admins(Model):
    admin_user_id = fields.BigIntField(unique=True)
    role = fields.CharEnumField(AdminRole)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
