"""empty message

Revision ID: 9197038171a3
Revises: 5fbc2274d12c
Create Date: 2021-08-16 22:18:28.924982

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9197038171a3'
down_revision = '5fbc2274d12c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=False))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', mysql.VARCHAR(length=100), nullable=False))
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
