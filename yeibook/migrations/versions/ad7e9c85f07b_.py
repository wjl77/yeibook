"""empty message

Revision ID: ad7e9c85f07b
Revises: 
Create Date: 2020-10-15 10:29:53.569741

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ad7e9c85f07b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('create_time', sa.DateTime(), nullable=True))
    op.add_column('book', sa.Column('status', sa.SmallInteger(), nullable=True))
    op.drop_column('book', 'my_message')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('my_message', mysql.VARCHAR(length=2048), nullable=True))
    op.drop_column('book', 'status')
    op.drop_column('book', 'create_time')
    # ### end Alembic commands ###
