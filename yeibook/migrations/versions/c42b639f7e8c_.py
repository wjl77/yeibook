"""empty message

Revision ID: c42b639f7e8c
Revises: ccdb1cce7b04
Create Date: 2020-10-15 10:48:42.106835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c42b639f7e8c'
down_revision = 'ccdb1cce7b04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('nickname', sa.String(length=24), nullable=False),
    sa.Column('phone_number', sa.String(length=18), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('beans', sa.Float(), nullable=True),
    sa.Column('send_counter', sa.Integer(), nullable=True),
    sa.Column('receive_counter', sa.Integer(), nullable=True),
    sa.Column('wx_open_id', sa.String(length=50), nullable=True),
    sa.Column('wx_name', sa.String(length=32), nullable=True),
    sa.Column('wx_avatar', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nickname'),
    sa.UniqueConstraint('phone_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###