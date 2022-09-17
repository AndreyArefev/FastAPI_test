"""revision 1.0

Revision ID: 654f5a6c32e1
Revises: 
Create Date: 2022-09-16 20:13:51.634998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '654f5a6c32e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('accounts', 'account_id',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('accounts', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('accounts', 'account_balance',
               existing_type=sa.REAL(),
               nullable=True)
    op.create_index(op.f('ix_accounts_user_id'), 'accounts', ['user_id'], unique=False)
    op.alter_column('products', 'product_id',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('products', 'product_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('products', 'product_price',
               existing_type=sa.REAL(),
               nullable=True)
    op.drop_constraint('products_product_name_key', 'products', type_='unique')
    op.add_column('transactions', sa.Column('amount', sa.Float(), nullable=True))
    op.alter_column('transactions', 'transaction_id',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('transactions', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('transactions', 'account_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('transactions', 'type_operation',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.create_index(op.f('ix_transactions_account_id'), 'transactions', ['account_id'], unique=False)
    op.create_index(op.f('ix_transactions_user_id'), 'transactions', ['user_id'], unique=False)
    op.drop_column('transactions', 'deposit')
    op.alter_column('users', 'user_id',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)



def downgrade() -> None:
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('users', 'user_id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.add_column('transactions', sa.Column('deposit', sa.REAL(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_transactions_user_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_account_id'), table_name='transactions')
    op.alter_column('transactions', 'type_operation',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('transactions', 'account_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('transactions', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('transactions', 'transaction_id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.drop_column('transactions', 'amount')
    op.create_unique_constraint('products_product_name_key', 'products', ['product_name'])
    op.alter_column('products', 'product_price',
               existing_type=sa.REAL(),
               nullable=False)
    op.alter_column('products', 'product_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('products', 'product_id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.drop_index(op.f('ix_accounts_user_id'), table_name='accounts')
    op.alter_column('accounts', 'account_balance',
               existing_type=sa.REAL(),
               nullable=False)
    op.alter_column('accounts', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('accounts', 'account_id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)

