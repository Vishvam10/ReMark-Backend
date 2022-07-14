"""empty message

Revision ID: 02473db39a05
Revises: dc2c19ec11c9
Create Date: 2022-07-14 20:48:05.321719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02473db39a05'
down_revision = 'dc2c19ec11c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'api_key')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('api_key', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###
