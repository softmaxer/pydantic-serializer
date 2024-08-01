# Pydantic serializer

this is a simple decorator that can be used on functions that have a return type of `str`, To serialize it into a given Pydantic Model.

## Usage:

For a function returning a string:

```py
def func_returning_str() -> str:
    return '{"sample": "json"}'
```

Let's say there's a Pydantic model like so:

```py
class SampleJson(BaseModel):
    sample: str
```

We can try and parse it with the decorator:

```py
from pydantic_serializer import serialize

@serialize(return_type=SampleJson)
def func_returning_str() -> str:
    return '{"sample": "json"}'
```

The function will return a `None` and log the error using `loguru` if there is an error.
If no error occurs, then you should get a return type of `SampleJson` in this case.
