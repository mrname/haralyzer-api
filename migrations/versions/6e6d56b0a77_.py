"""Adding startedDateTime to page table

Revision ID: 6e6d56b0a77
Revises: 37657fc43db4
Create Date: 2015-07-26 13:10:38.594409

"""

# revision identifiers, used by Alembic.
revision = '6e6d56b0a77'
down_revision = '37657fc43db4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('startedDateTime', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test', 'startedDateTime')
    ### end Alembic commands ###
