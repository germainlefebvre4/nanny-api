"""First revision

Revision ID: f71ee231a6dc
Revises: 6e523d653806
Create Date: 2020-11-09 12:15:11.582850

"""
from alembic import op
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Date, Time


# revision identifiers, used by Alembic.
revision = 'f71ee231a6dc'
down_revision = '6e523d653806'
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
        Column('hashed_password', String),
        Column('is_active', Boolean, default=True),
        Column('is_user', Boolean, default=True),
        Column('is_nanny', Boolean, default=False),
        Column('is_superuser', Boolean, default=False),
    )
    op.create_index(op.f("ix_user_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_user_full_name"), "users", ["firstname"], unique=False)
    op.create_index(op.f("ix_user_id"), "users", ["id"], unique=False)


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
    op.drop_constraint("fk_working_day_day_type_id", "working_days", type_="foreignkey")
    op.drop_constraint("fk_working_day_contract_id", "working_days", type_="foreignkey")
    op.drop_table("working_days")
    op.drop_constraint("fk_contract_nanny_id", "contracts", type_="foreignkey")
    op.drop_constraint("fk_contract_user_id", "contracts", type_="foreignkey")
    op.drop_table("contracts")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_full_name"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("users")
    op.drop_table("day_types")
