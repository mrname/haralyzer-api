"""Initial Structure (Creating test and page tables)

Revision ID: 6aab1ac34c3
Revises: None
Create Date: 2015-07-19 12:58:04.968533

"""

# revision identifiers, used by Alembic.
revision = '6aab1ac34c3'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Text(), nullable=False),
    sa.Column('run_date', sa.DateTime(), nullable=True),
    sa.Column('browser_name', sa.String(length=20), nullable=True),
    sa.Column('browser_version', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('page',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('test_id', sa.Integer(), nullable=False),
    sa.Column('page_id', sa.String(length=64), nullable=False),
    sa.Column('fqdn', sa.String(length=256), nullable=True),
    sa.Column('time_to_first_byte', sa.Float(), nullable=True),
    sa.Column('html_load_time', sa.Float(), nullable=True),
    sa.Column('video_load_time', sa.Float(), nullable=True),
    sa.Column('audio_load_time', sa.Float(), nullable=True),
    sa.Column('js_load_time', sa.Float(), nullable=True),
    sa.Column('css_load_time', sa.Float(), nullable=True),
    sa.Column('image_load_time', sa.Float(), nullable=True),
    sa.Column('page_load_time', sa.Float(), nullable=True),
    sa.Column('page_size', sa.Float(), nullable=True),
    sa.Column('image_size', sa.Float(), nullable=True),
    sa.Column('css_size', sa.Float(), nullable=True),
    sa.Column('text_size', sa.Float(), nullable=True),
    sa.Column('js_size', sa.Float(), nullable=True),
    sa.Column('audio_size', sa.Float(), nullable=True),
    sa.Column('video_size', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['test_id'], ['test.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('page')
    op.drop_table('test')
    ### end Alembic commands ###