import logging

from tortoise import fields
from tortoise.models import Model

logger = logging.getLogger(__name__)


class User(Model):
    class Meta:
        table = "users"
        ordering = ["created_at"]

    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=32, index=True, null=True)
    first_name = fields.CharField(max_length=64)
    last_name = fields.CharField(max_length=64, null=True)
    language_code = fields.CharField(max_length=8, null=True)
    language = fields.CharField(max_length=8, null=True)
    deeplink = fields.CharField(max_length=64, null=True)
    is_premium = fields.BooleanField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
