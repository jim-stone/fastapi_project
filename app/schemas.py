from pydantic import BaseModel
from datetime import datetime
from models import FieldDataTypeEnum
from typing import List, Union


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True


class EntryFieldSpec(BaseModel):
    field_name: str
    datatype: FieldDataTypeEnum
    is_reference: bool = False
    referenced_dict: str = None


class DictCreate(BaseModel):
    name: str
    entry_field_specs: List[EntryFieldSpec]


class EntryField(BaseModel):
    name: str
    value_as_string: str

    class Config:
        orm_mode = True


class Entry(BaseModel):
    id: int
    fields: Union[List[EntryField], None]

    class Config:
        orm_mode = True


class DictWithEntries(BaseModel):
    id: int
    name: str
    entries: Union[List[Entry], None]

    class Config:
        orm_mode = True
