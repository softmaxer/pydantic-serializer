from collections.abc import Callable
from functools import wraps
from loguru import logger
from typing import Any, ParamSpec
from pydantic import BaseModel, ValidationError
import json

P = ParamSpec("P")  # the callable parameters


def serialize(
    return_type: type[BaseModel],
) -> Callable[[Callable[P, str]], Callable[..., BaseModel | None]]:
    def wrapper(func: Callable[P, str]) -> Callable[..., BaseModel | None]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> BaseModel | None:
            json_string = func(*args, **kwargs)
            try:
                json_object = json.loads(json_string)
                model = return_type.model_validate(json_object)
                return model
            except ValidationError as e:
                logger.exception(f"Failed to parse json string: {e}")
                return
            except json.JSONDecodeError as e:
                logger.exception(f"Failed to load json object into dictionary: {e}")
                return

        return inner

    return wrapper
