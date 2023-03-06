from typing import Any, Callable, Dict, Iterable

import bson


class ObjectId(bson.ObjectId):
    """Type to abstract ObjectId interactions."""

    @classmethod
    def __get_validators__(cls) -> Iterable[Callable]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> bson.ObjectId:
        """Validate if value is a valid ObjectId"""
        if isinstance(value, bson.ObjectId):
            return value
        if ObjectId.is_valid(value):
            return ObjectId(value)
        raise ValueError("Invalid objectid.")

    @classmethod
    def __modify_schema__(cls, field_schema: Dict) -> None:
        field_schema.update(type="string")
