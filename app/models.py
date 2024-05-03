import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from database import Base


class FieldDataTypeEnum(enum.Enum):
    string = 1
    number = 2
    dict_entry = 0


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)


class Dictionary(Base):
    __tablename__ = 'dictionary'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    # dependent_fields = relationship(
    # 'DictionaryEntryFieldSpec', back_populates='dictionary')
    entries = relationship('DictionaryEntry')


class DictionaryEntry(Base):
    __tablename__ = 'dictionary_entry'
    id = Column(Integer, primary_key=True)
    dict_id = Column(Integer, ForeignKey('dictionary.id', ondelete='CASCADE'))
    values_as_json = Column(String)
    fields = relationship('EntryField')


class EntryField(Base):
    __tablename__ = 'entry_field'
    id = Column(Integer, primary_key=True)
    entry_id = Column(Integer, ForeignKey(
        'dictionary_entry.id', ondelete='CASCADE'))
    dict_id = Column(Integer, ForeignKey('dictionary.id', ondelete='CASCADE'))
    name = Column(String)
    value_as_string = Column(String)
    # entry = relationship('DictionaryEntry')


class DictionaryEntryFieldSpec(Base):
    __tablename__ = 'field_specification'

    id = Column(Integer, primary_key=True)
    field_name = Column(String, nullable=False)
    datatype = Column(Enum(FieldDataTypeEnum))
    dict = Column(Integer, ForeignKey('dictionary.id',
                  ondelete='CASCADE'), nullable=False)
    is_reference = Column(Boolean, server_default='False')
    referenced_dict = Column(Integer,  ForeignKey(
        'dictionary.id', ondelete='CASCADE'))
