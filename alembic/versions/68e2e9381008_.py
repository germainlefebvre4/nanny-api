"""Database Initialization

Revision ID: 68e2e9381008
Revises: 
Create Date: 2020-10-28 23:20:06.817732

"""
from alembic import op
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Date, Time


# revision identifiers, used by Alembic.
revision = '68e2e9381008'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'day_types',
        Column('id', Integer, primary_key=True, index=True),
        Column('name', String, unique=True)
    )

    op.create_table(
        'users',
        Column('id', Integer, primary_key=True, index=True),
        Column('email', String, unique=True, index=True),
        Column('firstname', String),
        Column('password', String),
        Column('is_active', Boolean, default=True),
        Column('is_user', Boolean, default=True),
        Column('is_nanny', Boolean, default=False),
        Column('is_admin', Boolean, default=False),
    )

    op.create_table(
        'contracts',
        Column('id', Integer, primary_key=True, index=True),
        Column('weekdays', Integer),
        Column('weeks', Integer),
        Column('hours', Integer),
        Column('price_hour_standard', Float),
        Column('price_hour_extra', Float),
        Column('price_fees', Float),
        Column('price_meals', Float),
        Column('start', Date),
        Column('end', Date),
        Column('created_on', DateTime),
        Column('updated_on', DateTime),
        Column('user_id', Integer,
            ForeignKey('users.id', name='fk_contract_user_id')),
        Column('nanny_id', Integer,
            ForeignKey('users.id', name='fk_contract_nanny_id')),    )

    op.create_table(
        'working_days',
        Column('id', Integer, primary_key=True, index=True),
        Column('day', Date),
        Column('start', Time),
        Column('end', Time),
        Column('created_on', DateTime),
        Column('updated_on', DateTime),
        Column('contract_id', Integer,
            ForeignKey('contracts.id', name='fk_working_day_contract_id')),
        Column('day_type_id', Integer,
            ForeignKey('day_types.id', name='fk_working_day_day_type_id'))
    )


def downgrade():
    op.drop_table('working_days')
    op.drop_table('contracts')
    op.drop_table('users')
    op.drop_table('day_types')
    op.drop_table('user_types')
