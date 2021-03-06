"""empty message

Revision ID: abe64340c56c
Revises: 145e8a4bde8a
Create Date: 2021-08-14 02:01:52.940698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abe64340c56c'
down_revision = '145e8a4bde8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_meals', sa.Column('count', sa.Integer(), nullable=True))
    op.add_column('order_meals', sa.Column('sum', sa.Float(precision=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_meals', 'sum')
    op.drop_column('order_meals', 'count')
    # ### end Alembic commands ###
