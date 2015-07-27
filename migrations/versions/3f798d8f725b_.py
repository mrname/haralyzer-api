"""Removing test.data column from db storage, moving to redis

Revision ID: 3f798d8f725b
Revises: 6e6d56b0a77
Create Date: 2015-07-27 11:32:53.808307

"""

# revision identifiers, used by Alembic.
revision = '3f798d8f725b'
down_revision = '6e6d56b0a77'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test', 'data')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('data', sa.Text(), nullable=False))
    ### end Alembic commands ###
