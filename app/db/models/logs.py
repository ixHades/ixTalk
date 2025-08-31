from tortoise.models import Model
from tortoise import fields
from app.db.enums import LogLevel


class LogEntry(Model):
    log_id = fields.IntField(primary_key=True)
    action_type = fields.CharField(max_length=50)
    level = fields.CharEnumField(LogLevel)
    user_id = fields.ForeignKeyField("models.Users", to_field="user_id")
    details = fields.TextField()
    timestamp = fields.DatetimeField()

    class Meta:
        table = "Logs"
