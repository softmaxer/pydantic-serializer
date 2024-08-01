from typing import Optional
from pydantic_serializer import serialize
from pydantic import BaseModel


class SimpleModel(BaseModel):
    id: str
    name: str


class ModelWithOptionalParams(BaseModel):
    id: str
    name: str
    age: Optional[int] = 0


class InheritedObject(ModelWithOptionalParams):
    height: float
    weight: float


class NestedObject(BaseModel):
    simple_model: SimpleModel


@serialize(return_type=SimpleModel)
def return_correct_string():
    return '{"id": "1", "name": "John smith"}'


@serialize(return_type=ModelWithOptionalParams)
def correct_string_with_optional_model():
    return '{"id": "1", "name": "John smith"}'


@serialize(return_type=ModelWithOptionalParams)
def wrong_string():
    return '{"id: "1", "name": "John smith"}'


@serialize(return_type=InheritedObject)
def inherited_string():
    return '{"id": "1", "name": "John Smith", "height": 1.5, "weight": 26}'


@serialize(return_type=NestedObject)
def nested_string():
    return '{"simple_model": {"id": "1", "name": "John smith"}}'


def test_correct_string():
    result = return_correct_string()
    assert result is not None
    assert isinstance(result, SimpleModel)


def test_wrong_string():
    result = wrong_string()
    assert result is None


def test_optional():
    result = correct_string_with_optional_model()
    assert result is not None
    assert isinstance(result, ModelWithOptionalParams)


def test_inherited():
    result = inherited_string()
    assert result is not None
    assert isinstance(result, InheritedObject)


def test_nested():
    result = nested_string()
    assert result is not None
    assert isinstance(result, NestedObject)
