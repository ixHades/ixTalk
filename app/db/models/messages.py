from tortoise.models import Model
from tortoise import fields
from app.db.enums import MessageStatus
from app.utils.code_generator import CodeGenerator


class Messages(Model):
    message_id = fields.IntField(primary_key=True)
    message_code = fields.CharField(max_length=10, unique=True, default=CodeGenerator.generate_code_pattern("MSG-{6}"))
    message_text = fields.TextField(null=False)
    referenced_message_id = fields.ForeignKeyField(
        "models.Messages", to_field="message_code", null=True
    )
    channel_message_id = fields.IntField(null=False)
    unique_code = fields.ForeignKeyField("models.Users", to_field="unique_code")
    status = fields.CharEnumField(MessageStatus)
    reviewed_by = fields.ForeignKeyField("models.Admins", to_field="admin_user_id")
    reviewed_note = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
