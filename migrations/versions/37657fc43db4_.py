"""Switching from fqdn to hostname. Adding test name and startedDateTime

Revision ID: 37657fc43db4
Revises: 6aab1ac34c3
Create Date: 2015-07-20 20:05:42.650553

"""

# revision identifiers, used by Alembic.
revision = '37657fc43db4'
down_revision = '6aab1ac34c3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('hostname', sa.String(length=256), nullable=True))
    op.drop_column('page', 'fqdn')
    op.add_column('test', sa.Column('hostname', sa.String(length=256), nullable=False))
    op.add_column('test', sa.Column('name', sa.String(length=256), nullable=True))
    op.add_column('test', sa.Column('startedDateTime', sa.DateTime(), nullable=True))
    op.drop_column('test', 'run_date')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('run_date', sa.DATETIME(), nullable=True))
    op.drop_column('test', 'startedDateTime')
    op.drop_column('test', 'name')
    op.drop_column('test', 'hostname')
    op.add_column('page', sa.Column('fqdn', sa.VARCHAR(length=256), nullable=True))
    op.drop_column('page', 'hostname')
    ### end Alembic commands ###
