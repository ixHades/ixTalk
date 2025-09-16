from typing import Any, Coroutine, List

from tortoise.models import Model
from tortoise import fields, signals, transactions

from app.db.models import WarningEntry
from .warnings import WarningEntry
from .admins import Admins
from app.db.enums import WarningSeverity
from app.utils.code_generator import CodeGenerator


class Users(Model):
    user_id = fields.BigIntField(primary_key=True, unique=True)
    unique_code = fields.CharField(
        max_length=5, unique=True, default=CodeGenerator.generate_unique_code
    )
    is_blocked = fields.BooleanField(default=False)
    warning_count = fields.IntField(default=0)
    last_activity = fields.DatetimeField(auto_now=True)
    warning_entries: fields.ReverseRelation["WarningEntry"]
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    async def add_warning(
        self, reason: str, severity: WarningSeverity, issued_by: Admins
    ) -> WarningEntry:
        warning = await WarningEntry.create(
                user=self,
                reason=reason,
                severity=severity,
                issued_by=issued_by,
            )
        self.warning_count += 1
        if severity == WarningSeverity.HIGH:
            self.is_blocked = True
        await self.save(
                update_fields=["warning_count", "is_blocked", "updated_at"],
            )
        return warning

    async def is_blocked_or_high_warning(self) -> bool:
        if self.is_blocked:
            return True
        return await WarningEntry.filter(
            user_id=self.user_id, serverity=WarningSeverity.HIGH, is_active=True
        ).exists()

    async def get_active_warnings(self) -> List[WarningEntry]:
        return await WarningEntry.filter(user_id=self.user_id, is_active=True).order_by(
            "-created_at"
        )

    async def regenerate_unique_code(self) -> str:
        new_code = await CodeGenerator.generate_unique_code(5)
        self.unique_code = new_code
        await self.save(update_fields=["unique_code", "updated_at"])
        return new_code

    def __str__(self):
        return f"{self.user_id} - {self.unique_code}"
