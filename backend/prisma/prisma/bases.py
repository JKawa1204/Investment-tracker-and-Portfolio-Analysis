# -*- coding: utf-8 -*-
# code generated by Prisma. DO NOT EDIT.
# pyright: reportUnusedImport=false
# fmt: off

# global imports for type checking
from builtins import bool as _bool
from builtins import int as _int
from builtins import float as _float
from builtins import str as _str
import sys
import decimal
import datetime
from typing import (
    TYPE_CHECKING,
    Optional,
    Iterable,
    Iterator,
    Sequence,
    Callable,
    ClassVar,
    NoReturn,
    TypeVar,
    Generic,
    Mapping,
    Tuple,
    Union,
    List,
    Dict,
    Type,
    Any,
    Set,
    overload,
    cast,
)
from typing_extensions import TypedDict, Literal


LiteralString = str
# -- template models.py.jinja --
from pydantic import BaseModel

from . import fields, actions
from ._types import FuncType
from ._builder import serialize_base64
from ._compat import PYDANTIC_V2, ConfigDict

if TYPE_CHECKING:
    from .client import Prisma


_PrismaModelT = TypeVar('_PrismaModelT', bound='_PrismaModel')


class _PrismaModel(BaseModel):
    if PYDANTIC_V2:
        model_config: ClassVar[ConfigDict] = ConfigDict(
            use_enum_values=True,
            arbitrary_types_allowed=True,
            populate_by_name=True,
        )
    elif not TYPE_CHECKING:
        from ._compat import BaseConfig

        class Config(BaseConfig):
            use_enum_values: bool = True
            arbitrary_types_allowed: bool = True
            allow_population_by_field_name: bool = True
            json_encoders: Dict[Any, FuncType] = {
                fields.Base64: serialize_base64,
            }

    # TODO: ensure this is required by subclasses
    __prisma_model__: ClassVar[str]


class BaseAsset(_PrismaModel):
    __prisma_model__: ClassVar[Literal['Asset']] = 'Asset'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.AssetActions[_PrismaModelT]':
        from .client import get_client

        return actions.AssetActions[_PrismaModelT](client or get_client(), cls)


class BaseTransaction(_PrismaModel):
    __prisma_model__: ClassVar[Literal['Transaction']] = 'Transaction'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.TransactionActions[_PrismaModelT]':
        from .client import get_client

        return actions.TransactionActions[_PrismaModelT](client or get_client(), cls)


class BaseHistoricalData(_PrismaModel):
    __prisma_model__: ClassVar[Literal['HistoricalData']] = 'HistoricalData'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.HistoricalDataActions[_PrismaModelT]':
        from .client import get_client

        return actions.HistoricalDataActions[_PrismaModelT](client or get_client(), cls)


