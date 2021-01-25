"""empty message

Revision ID: 707e71d64205
Revises: c42b639f7e8c
Create Date: 2020-10-15 10:54:28.698562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '707e71d64205'
down_revision = 'c42b639f7e8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('pages', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'pages')
    # ### end Alembic commands ###
