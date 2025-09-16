from tortoise.models import Model
from tortoise import fields
from app.db.enums import WarningSeverity


class WarningEntry(Model):
    warning_id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField(model_name="models.Users", to_field="user_id", related_name="warning_entries")
    reason = fields.TextField()
    issued_by = fields.ForeignKeyField(
        model_name="models.Admins", to_field="admin_user_id"
    )
    severity = fields.CharEnumField(WarningSeverity)
    issued_at = fields.DatetimeField(auto_now_add=True)
    expire_at = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "Warning"
