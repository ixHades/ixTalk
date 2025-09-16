from typing import List, Optional

from tortoise.exceptions import DoesNotExist
from tortoise.models import Model
from tortoise import fields
from app.db.enums import MessageStatus
from app.utils.code_generator import CodeGenerator
from app.db.models import Admins


class Messages(Model):
    message_id = fields.IntField(primary_key=True)
    message_code = fields.CharField(
        max_length=10,
        unique=True,
        default=CodeGenerator.generate_code_pattern("MSG_{6}"),
    )
    message_text = fields.TextField(null=False)
    referenced_message_id = fields.ForeignKeyField(
        "models.Messages",
        to_field="message_code",
        related_name="referenced_messages",
        null=True,
    )
    channel_message_id = fields.IntField(null=False)
    user = fields.ForeignKeyField(
        "models.Users", to_field="unique_code", related_name="messages"
    )
    status = fields.CharEnumField(MessageStatus)
    reviewed_by = fields.ForeignKeyField(
        "models.Admins", to_field="admin_user_id", related_name="reviewed_messages"
    )
    reviewed_note = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    async def get_message_by_status(self, status_enum: MessageStatus) -> list:
        return await self.filter(status=status_enum)

    async def set_status(
        self, status: MessageStatus, reviewed_by: int, note=""
    ) -> None:
        self.status = status
        self.reviewed_by = reviewed_by
        if status == status.REJECT:
            self.reviewed_note = note
        await self.save(
            update_fields=["status", "reviewed_by_id", "reviewed_note", "updated_at"]
        )

    @classmethod
    async def get_by_code(cls, message_code: str) -> Optional["Messages"]:
        try:
            return await cls.get(message_code=message_code)
        except DoesNotExist:
            return None
    @classmethod
    async def get_user_messages(cls, user_code:str) -> List["Messages"]:
        return await cls.filter(user_id=user_code, status=MessageStatus.APPROVED)

    @property
    async def is_approved(self) -> bool:
        return self.status == MessageStatus.APPROVED

    @property
    async def is_pending(self) -> bool:
        return self.status == MessageStatus.PENDING
