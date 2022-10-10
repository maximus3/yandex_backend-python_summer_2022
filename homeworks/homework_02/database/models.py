from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Identity,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# Items


class Item(Base):  # type: ignore
    __abstract__ = True

    id = Column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )

    name = Column(Text)
    amount = Column(Integer)
    price = Column(Numeric(8, 2))
    dosage_form = Column(Text)
    manufacturer = Column(Text)
    barcode = Column(Text)


class CommonItem(Item):
    __tablename__ = 'common_item'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='common_item_pkey'),
        UniqueConstraint('barcode', name='common_item_barcode_key'),
    )

    @classmethod
    @property
    def name_for_enum(cls) -> str:
        return 'common'


class ReceiptItem(Item):
    __tablename__ = 'receipt_item'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='receipt_item_pkey'),
        UniqueConstraint('barcode', name='receipt_item_barcode_key'),
    )

    receipt = relationship('Receipt', back_populates='item')

    @classmethod
    @property
    def name_for_enum(cls) -> str:
        return 'receipt'


class SpecialItem(Item):
    __tablename__ = 'special_item'
    __table_args__ = (
        ForeignKeyConstraint(
            ['specialty_id'],
            ['specialty.id'],
            name='special_item_specialty_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='special_item_pkey'),
        UniqueConstraint('barcode', name='special_item_barcode_key'),
    )

    specialty_id = Column(ForeignKey('specialty.id'))

    specialty = relationship('Specialty', back_populates='special_item')

    @classmethod
    @property
    def name_for_enum(cls) -> str:
        return 'special'


# Accounts


class Account(Base):  # type: ignore
    __abstract__ = True

    id = Column(Integer)
    full_name = Column(Text)
    phone = Column(Text)
    password_hash = Column(Text)


class UserAccount(Account):
    __tablename__ = 'user_account'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_account_pkey'),
        UniqueConstraint('phone', name='user_account_phone_key'),
    )

    receipt = relationship('Receipt', back_populates='user')


class DoctorAccount(Account):
    __tablename__ = 'doctor_account'
    __table_args__ = (
        ForeignKeyConstraint(
            ['specialty_id'],
            ['specialty.id'],
            name='doctor_account_specialty_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='doctor_account_pkey'),
        UniqueConstraint('phone', name='doctor_account_phone_key'),
    )

    specialty_id = Column(ForeignKey('specialty.id'))

    specialty = relationship('Specialty', back_populates='doctor_account')


# For UserAccount


class Receipt(Base):  # type: ignore
    __tablename__ = 'receipt'
    __table_args__ = (
        ForeignKeyConstraint(
            ['item_id'], ['receipt_item.id'], name='receipt_item_id_fkey'
        ),
        ForeignKeyConstraint(
            ['user_id'], ['user_account.id'], name='receipt_user_id_fkey'
        ),
        PrimaryKeyConstraint('id', name='receipt_pkey'),
        UniqueConstraint(
            'user_id', 'item_id', name='receipt_user_id_item_id_key'
        ),
    )

    id = Column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    user_id = Column(ForeignKey('user_account.id'))
    item_id = Column(ForeignKey('receipt_item.id'))

    item = relationship('ReceiptItem', back_populates='receipt')
    user = relationship('UserAccount', back_populates='receipt')


# For DoctorAccount


class Specialty(Base):  # type: ignore
    __tablename__ = 'specialty'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='specialty_pkey'),
        UniqueConstraint('name', name='specialty_name_key'),
    )

    id = Column(
        Integer,
        Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=2147483647,
            cycle=False,
            cache=1,
        ),
    )
    name = Column(Text)

    doctor_account = relationship('DoctorAccount', back_populates='specialty')
    special_item = relationship('SpecialItem', back_populates='specialty')
