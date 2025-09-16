import random
import string
from typing import Type, Optional
from tortoise.models import Model
from tortoise.exceptions import DoesNotExist
import re


class CodeGenerator:
    @staticmethod
    def generate_unique_code(
        length: int = 5,
    ) -> str:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return code

    @staticmethod
    def generate_code_pattern(
        pattern: str,
    ) -> str:
        match = re.match(r"(.*)\{(\d+)}(.*)", pattern)
        if not match:
            raise ValueError("الگوی وارد شده معتبر نیست")
        prefix = match.group(1)
        length = int(match.group(2))
        suffix = match.group(3)

        random_part = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=length)
        )
        code = f"{prefix}{random_part}{suffix}"

        return code
