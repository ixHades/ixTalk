from tortoise.models import Model
from tortoise import fields
from app.db.enums import AdminRole
from .warnings import WarningEntry


class Admins(Model):
    admin_user_id = fields.BigIntField(unique=True)
    role = fields.CharEnumField(AdminRole)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    issued_warnings: fields.ReverseRelation["WarningEntry"]

    class Meta:
        table = "admins"

    def __str__(self) -> str:
        return f"Admin {self.admin_user_id} - {self.role}"
