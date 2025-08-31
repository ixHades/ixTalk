from tortoise.models import Model
from tortoise import fields

class Reports(Model):
    report_id = fields.IntField(primary_key=True)
    message_code = fields.ForeignKeyField(model_name="models.Messages", to_field="message_code")
    reporter_user_id = fields.ForeignKeyField(model_name="models.Users", to_field="user_id")
    created_at = fields.DatetimeField(auto_now_add=True)