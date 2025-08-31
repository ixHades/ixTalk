from tortoise.models import Model
from tortoise import fields

class Users(Model):
    user_id = fields.BigIntField(primary_key=True, unique=True)
    unique_code = fields.CharField(max_length=5, unique=True)
    is_blocked = fields.BooleanField(default=False)
    warning_count = fields.IntField(default=0)
    last_activity = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)