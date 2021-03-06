"""empty message

Revision ID: 58083ee8ea81
Revises: 06dd5b9ad56b
Create Date: 2020-12-22 23:37:03.331454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58083ee8ea81'
down_revision = '06dd5b9ad56b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('pub_date', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'pub_date')
    # ### end Alembic commands ###
