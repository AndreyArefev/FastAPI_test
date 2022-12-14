"""version 3.0

Revision ID: 95a6a22afca9
Revises: 358d0ca78345
Create Date: 2022-09-17 17:46:57.769173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95a6a22afca9'
down_revision = '358d0ca78345'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'account_id',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('products', 'product_id',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('transactions', 'transaction_id',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('users', 'user_id',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'user_id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=86, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('transactions', 'transaction_id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=18, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('products', 'product_id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=2, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('accounts', 'account_id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=8, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###
