from typing import Optional, List, Dict, NewType, Any, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from uuid import UUID

from dataclasses_jsonschema import JsonSchemaMixin, FieldEncoder

Postcode = NewType('Postcode', str)


class PostcodeField(FieldEncoder):

    @property
    def json_schema(self):
        return {'type': 'string', 'minLength': 5, 'maxLength': 8}


JsonSchemaMixin.register_field_encoders({Postcode: PostcodeField()})


class SubSchemas(JsonSchemaMixin):
    pass


class Weekday(Enum):
    MON = 'Monday'
    TUE = 'Tuesday'
    WED = 'Wednesday'
    THU = 'Thursday'
    FRI = 'Friday'


@dataclass(eq=True)
class Point(SubSchemas):
    x: float
    y: float

    @classmethod
    def field_mapping(cls) -> Dict[str, str]:
        return {'x': 'z'}


NewPoint = NewType('NewPoint', Point)


@dataclass
class Foo(SubSchemas):
    """A foo that foos"""
    a: datetime
    b: Optional[List[Point]]
    c: Dict[str, int]
    d: Weekday
    f: Tuple[str, int]
    g: Tuple[str, ...]
    e: Optional[Postcode] = None
    h: Optional[NewPoint] = None


@dataclass(eq=True)
class Bar(JsonSchemaMixin):
    """Type with union field"""
    a: Union[Weekday, Point]


@dataclass
class Recursive(JsonSchemaMixin):
    """A recursive data-structure"""
    a: str
    b: Optional['Recursive'] = None


@dataclass
class OpaqueData(JsonSchemaMixin):
    """Structure with unknown types"""
    a: List[Any]
    b: Dict[str, Any]


@dataclass
class Product(JsonSchemaMixin):
    name: str
    cost: float


@dataclass
class ShoppingCart(JsonSchemaMixin):
    items: List[Product]

    @property
    def cost(self):
        return sum([item.cost for item in self.items])


@dataclass
class ProductList(JsonSchemaMixin):
    products: Dict[UUID, Product]
