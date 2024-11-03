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
import os
import logging
import inspect
import warnings
from collections import OrderedDict

from pydantic import BaseModel, Field

from . import types, enums, errors, fields, bases
from ._types import FuncType
from ._compat import model_rebuild, field_validator
from ._builder import serialize_base64
from .generator import partial_models_ctx, PartialModelField


log: logging.Logger = logging.getLogger(__name__)
_created_partial_types: Set[str] = set()

class Asset(bases.BaseAsset):
    """Represents a Asset record"""

    id: _int
    symbol: _str
    name: _str
    assetType: _str
    sector: Optional[_str] = None
    quantity: _float
    price: _float
    transactions: Optional[List['models.Transaction']] = None
    historicalData: Optional[List['models.HistoricalData']] = None

    # take *args and **kwargs so that other metaclasses can define arguments
    def __init_subclass__(
        cls,
        *args: Any,
        warn_subclass: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__()
        if warn_subclass is not None:
            warnings.warn(
                'The `warn_subclass` argument is deprecated as it is no longer necessary and will be removed in the next release',
                DeprecationWarning,
                stacklevel=3,
            )


    @staticmethod
    def create_partial(
        name: str,
        include: Optional[Iterable['types.AssetKeys']] = None,
        exclude: Optional[Iterable['types.AssetKeys']] = None,
        required: Optional[Iterable['types.AssetKeys']] = None,
        optional: Optional[Iterable['types.AssetKeys']] = None,
        relations: Optional[Mapping['types.AssetRelationalFieldKeys', str]] = None,
        exclude_relational_fields: bool = False,
    ) -> None:
        if not os.environ.get('PRISMA_GENERATOR_INVOCATION'):
            raise RuntimeError(
                'Attempted to create a partial type outside of client generation.'
            )

        if name in _created_partial_types:
            raise ValueError(f'Partial type "{name}" has already been created.')

        if include is not None:
            if exclude is not None:
                raise TypeError('Exclude and include are mutually exclusive.')
            if exclude_relational_fields is True:
                raise TypeError('Include and exclude_relational_fields=True are mutually exclusive.')

        if required and optional:
            shared = set(required) & set(optional)
            if shared:
                raise ValueError(f'Cannot make the same field(s) required and optional {shared}')

        if exclude_relational_fields and relations:
            raise ValueError(
                'exclude_relational_fields and relations are mutually exclusive'
            )

        fields: Dict['types.AssetKeys', PartialModelField] = OrderedDict()

        try:
            if include:
                for field in include:
                    fields[field] = _Asset_fields[field].copy()
            elif exclude:
                for field in exclude:
                    if field not in _Asset_fields:
                        raise KeyError(field)

                fields = {
                    key: data.copy()
                    for key, data in _Asset_fields.items()
                    if key not in exclude
                }
            else:
                fields = {
                    key: data.copy()
                    for key, data in _Asset_fields.items()
                }

            if required:
                for field in required:
                    fields[field]['optional'] = False

            if optional:
                for field in optional:
                    fields[field]['optional'] = True

            if exclude_relational_fields:
                fields = {
                    key: data
                    for key, data in fields.items()
                    if key not in _Asset_relational_fields
                }

            if relations:
                for field, type_ in relations.items():
                    if field not in _Asset_relational_fields:
                        raise errors.UnknownRelationalFieldError('Asset', field)

                    # TODO: this method of validating types is not ideal
                    # as it means we cannot two create partial types that
                    # reference each other
                    if type_ not in _created_partial_types:
                        raise ValueError(
                            f'Unknown partial type: "{type_}". '
                            f'Did you remember to generate the {type_} type before this one?'
                        )

                    # TODO: support non prisma.partials models
                    info = fields[field]
                    if info['is_list']:
                        info['type'] = f'List[\'partials.{type_}\']'
                    else:
                        info['type'] = f'\'partials.{type_}\''
        except KeyError as exc:
            raise ValueError(
                f'{exc.args[0]} is not a valid Asset / {name} field.'
            ) from None

        models = partial_models_ctx.get()
        models.append(
            {
                'name': name,
                'fields': cast(Mapping[str, PartialModelField], fields),
                'from_model': 'Asset',
            }
        )
        _created_partial_types.add(name)


class Transaction(bases.BaseTransaction):
    """Represents a Transaction record"""

    id: _int
    type: _str
    quantity: _float
    price: _float
    createdAt: datetime.datetime
    asset: Optional['models.Asset'] = None
    assetId: _int

    # take *args and **kwargs so that other metaclasses can define arguments
    def __init_subclass__(
        cls,
        *args: Any,
        warn_subclass: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__()
        if warn_subclass is not None:
            warnings.warn(
                'The `warn_subclass` argument is deprecated as it is no longer necessary and will be removed in the next release',
                DeprecationWarning,
                stacklevel=3,
            )


    @staticmethod
    def create_partial(
        name: str,
        include: Optional[Iterable['types.TransactionKeys']] = None,
        exclude: Optional[Iterable['types.TransactionKeys']] = None,
        required: Optional[Iterable['types.TransactionKeys']] = None,
        optional: Optional[Iterable['types.TransactionKeys']] = None,
        relations: Optional[Mapping['types.TransactionRelationalFieldKeys', str]] = None,
        exclude_relational_fields: bool = False,
    ) -> None:
        if not os.environ.get('PRISMA_GENERATOR_INVOCATION'):
            raise RuntimeError(
                'Attempted to create a partial type outside of client generation.'
            )

        if name in _created_partial_types:
            raise ValueError(f'Partial type "{name}" has already been created.')

        if include is not None:
            if exclude is not None:
                raise TypeError('Exclude and include are mutually exclusive.')
            if exclude_relational_fields is True:
                raise TypeError('Include and exclude_relational_fields=True are mutually exclusive.')

        if required and optional:
            shared = set(required) & set(optional)
            if shared:
                raise ValueError(f'Cannot make the same field(s) required and optional {shared}')

        if exclude_relational_fields and relations:
            raise ValueError(
                'exclude_relational_fields and relations are mutually exclusive'
            )

        fields: Dict['types.TransactionKeys', PartialModelField] = OrderedDict()

        try:
            if include:
                for field in include:
                    fields[field] = _Transaction_fields[field].copy()
            elif exclude:
                for field in exclude:
                    if field not in _Transaction_fields:
                        raise KeyError(field)

                fields = {
                    key: data.copy()
                    for key, data in _Transaction_fields.items()
                    if key not in exclude
                }
            else:
                fields = {
                    key: data.copy()
                    for key, data in _Transaction_fields.items()
                }

            if required:
                for field in required:
                    fields[field]['optional'] = False

            if optional:
                for field in optional:
                    fields[field]['optional'] = True

            if exclude_relational_fields:
                fields = {
                    key: data
                    for key, data in fields.items()
                    if key not in _Transaction_relational_fields
                }

            if relations:
                for field, type_ in relations.items():
                    if field not in _Transaction_relational_fields:
                        raise errors.UnknownRelationalFieldError('Transaction', field)

                    # TODO: this method of validating types is not ideal
                    # as it means we cannot two create partial types that
                    # reference each other
                    if type_ not in _created_partial_types:
                        raise ValueError(
                            f'Unknown partial type: "{type_}". '
                            f'Did you remember to generate the {type_} type before this one?'
                        )

                    # TODO: support non prisma.partials models
                    info = fields[field]
                    if info['is_list']:
                        info['type'] = f'List[\'partials.{type_}\']'
                    else:
                        info['type'] = f'\'partials.{type_}\''
        except KeyError as exc:
            raise ValueError(
                f'{exc.args[0]} is not a valid Transaction / {name} field.'
            ) from None

        models = partial_models_ctx.get()
        models.append(
            {
                'name': name,
                'fields': cast(Mapping[str, PartialModelField], fields),
                'from_model': 'Transaction',
            }
        )
        _created_partial_types.add(name)


class HistoricalData(bases.BaseHistoricalData):
    """Represents a HistoricalData record"""

    id: _int
    date: datetime.datetime
    closePrice: _float
    asset: Optional['models.Asset'] = None
    assetId: _int

    # take *args and **kwargs so that other metaclasses can define arguments
    def __init_subclass__(
        cls,
        *args: Any,
        warn_subclass: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__()
        if warn_subclass is not None:
            warnings.warn(
                'The `warn_subclass` argument is deprecated as it is no longer necessary and will be removed in the next release',
                DeprecationWarning,
                stacklevel=3,
            )


    @staticmethod
    def create_partial(
        name: str,
        include: Optional[Iterable['types.HistoricalDataKeys']] = None,
        exclude: Optional[Iterable['types.HistoricalDataKeys']] = None,
        required: Optional[Iterable['types.HistoricalDataKeys']] = None,
        optional: Optional[Iterable['types.HistoricalDataKeys']] = None,
        relations: Optional[Mapping['types.HistoricalDataRelationalFieldKeys', str]] = None,
        exclude_relational_fields: bool = False,
    ) -> None:
        if not os.environ.get('PRISMA_GENERATOR_INVOCATION'):
            raise RuntimeError(
                'Attempted to create a partial type outside of client generation.'
            )

        if name in _created_partial_types:
            raise ValueError(f'Partial type "{name}" has already been created.')

        if include is not None:
            if exclude is not None:
                raise TypeError('Exclude and include are mutually exclusive.')
            if exclude_relational_fields is True:
                raise TypeError('Include and exclude_relational_fields=True are mutually exclusive.')

        if required and optional:
            shared = set(required) & set(optional)
            if shared:
                raise ValueError(f'Cannot make the same field(s) required and optional {shared}')

        if exclude_relational_fields and relations:
            raise ValueError(
                'exclude_relational_fields and relations are mutually exclusive'
            )

        fields: Dict['types.HistoricalDataKeys', PartialModelField] = OrderedDict()

        try:
            if include:
                for field in include:
                    fields[field] = _HistoricalData_fields[field].copy()
            elif exclude:
                for field in exclude:
                    if field not in _HistoricalData_fields:
                        raise KeyError(field)

                fields = {
                    key: data.copy()
                    for key, data in _HistoricalData_fields.items()
                    if key not in exclude
                }
            else:
                fields = {
                    key: data.copy()
                    for key, data in _HistoricalData_fields.items()
                }

            if required:
                for field in required:
                    fields[field]['optional'] = False

            if optional:
                for field in optional:
                    fields[field]['optional'] = True

            if exclude_relational_fields:
                fields = {
                    key: data
                    for key, data in fields.items()
                    if key not in _HistoricalData_relational_fields
                }

            if relations:
                for field, type_ in relations.items():
                    if field not in _HistoricalData_relational_fields:
                        raise errors.UnknownRelationalFieldError('HistoricalData', field)

                    # TODO: this method of validating types is not ideal
                    # as it means we cannot two create partial types that
                    # reference each other
                    if type_ not in _created_partial_types:
                        raise ValueError(
                            f'Unknown partial type: "{type_}". '
                            f'Did you remember to generate the {type_} type before this one?'
                        )

                    # TODO: support non prisma.partials models
                    info = fields[field]
                    if info['is_list']:
                        info['type'] = f'List[\'partials.{type_}\']'
                    else:
                        info['type'] = f'\'partials.{type_}\''
        except KeyError as exc:
            raise ValueError(
                f'{exc.args[0]} is not a valid HistoricalData / {name} field.'
            ) from None

        models = partial_models_ctx.get()
        models.append(
            {
                'name': name,
                'fields': cast(Mapping[str, PartialModelField], fields),
                'from_model': 'HistoricalData',
            }
        )
        _created_partial_types.add(name)



_Asset_relational_fields: Set[str] = {
        'transactions',
        'historicalData',
    }
_Asset_fields: Dict['types.AssetKeys', PartialModelField] = OrderedDict(
    [
        ('id', {
            'name': 'id',
            'is_list': False,
            'optional': False,
            'type': '_int',
            'is_relational': False,
            'documentation': None,
        }),
        ('symbol', {
            'name': 'symbol',
            'is_list': False,
            'optional': False,
            'type': '_str',
            'is_relational': False,
            'documentation': None,
        }),
        ('name', {
            'name': 'name',
            'is_list': False,
            'optional': False,
            'type': '_str',
            'is_relational': False,
            'documentation': None,
        }),
        ('assetType', {
            'name': 'assetType',
            'is_list': False,
            'optional': False,
            'type': '_str',
            'is_relational': False,
            'documentation': None,
        }),
        ('sector', {
            'name': 'sector',
            'is_list': False,
            'optional': True,
            'type': '_str',
            'is_relational': False,
            'documentation': None,
        }),
        ('quantity', {
            'name': 'quantity',
            'is_list': False,
            'optional': False,
            'type': '_float',
            'is_relational': False,
            'documentation': None,
        }),
        ('price', {
            'name': 'price',
            'is_list': False,
            'optional': False,
            'type': '_float',
            'is_relational': False,
            'documentation': None,
        }),
        ('transactions', {
            'name': 'transactions',
            'is_list': True,
            'optional': True,
            'type': 'List[\'models.Transaction\']',
            'is_relational': True,
            'documentation': None,
        }),
        ('historicalData', {
            'name': 'historicalData',
            'is_list': True,
            'optional': True,
            'type': 'List[\'models.HistoricalData\']',
            'is_relational': True,
            'documentation': None,
        }),
    ],
)

_Transaction_relational_fields: Set[str] = {
        'asset',
    }
_Transaction_fields: Dict['types.TransactionKeys', PartialModelField] = OrderedDict(
    [
        ('id', {
            'name': 'id',
            'is_list': False,
            'optional': False,
            'type': '_int',
            'is_relational': False,
            'documentation': None,
        }),
        ('type', {
            'name': 'type',
            'is_list': False,
            'optional': False,
            'type': '_str',
            'is_relational': False,
            'documentation': None,
        }),
        ('quantity', {
            'name': 'quantity',
            'is_list': False,
            'optional': False,
            'type': '_float',
            'is_relational': False,
            'documentation': None,
        }),
        ('price', {
            'name': 'price',
            'is_list': False,
            'optional': False,
            'type': '_float',
            'is_relational': False,
            'documentation': None,
        }),
        ('createdAt', {
            'name': 'createdAt',
            'is_list': False,
            'optional': False,
            'type': 'datetime.datetime',
            'is_relational': False,
            'documentation': None,
        }),
        ('asset', {
            'name': 'asset',
            'is_list': False,
            'optional': True,
            'type': 'models.Asset',
            'is_relational': True,
            'documentation': None,
        }),
        ('assetId', {
            'name': 'assetId',
            'is_list': False,
            'optional': False,
            'type': '_int',
            'is_relational': False,
            'documentation': None,
        }),
    ],
)

_HistoricalData_relational_fields: Set[str] = {
        'asset',
    }
_HistoricalData_fields: Dict['types.HistoricalDataKeys', PartialModelField] = OrderedDict(
    [
        ('id', {
            'name': 'id',
            'is_list': False,
            'optional': False,
            'type': '_int',
            'is_relational': False,
            'documentation': None,
        }),
        ('date', {
            'name': 'date',
            'is_list': False,
            'optional': False,
            'type': 'datetime.datetime',
            'is_relational': False,
            'documentation': None,
        }),
        ('closePrice', {
            'name': 'closePrice',
            'is_list': False,
            'optional': False,
            'type': '_float',
            'is_relational': False,
            'documentation': None,
        }),
        ('asset', {
            'name': 'asset',
            'is_list': False,
            'optional': True,
            'type': 'models.Asset',
            'is_relational': True,
            'documentation': None,
        }),
        ('assetId', {
            'name': 'assetId',
            'is_list': False,
            'optional': False,
            'type': '_int',
            'is_relational': False,
            'documentation': None,
        }),
    ],
)



# we have to import ourselves as relation types are namespaced to models
# e.g. models.Post
from . import models, actions

# required to support relationships between models
model_rebuild(Asset)
model_rebuild(Transaction)
model_rebuild(HistoricalData)