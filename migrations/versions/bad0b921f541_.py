"""empty message

Revision ID: bad0b921f541
Revises: 3ef5f6c3c296
Create Date: 2022-07-27 20:28:01.920541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bad0b921f541'
down_revision = '3ef5f6c3c296'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('annotation', sa.Column('node_xpath', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'annotation', ['node_xpath'])
    op.drop_column('annotation', 'node_xpath')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('annotation', sa.Column('node_xpath', sa.VARCHAR(), nullable=False))
    op.drop_constraint(None, 'annotation', type_='unique')
    op.drop_column('annotation', 'node_xpath')
    # ### end Alembic commands ###