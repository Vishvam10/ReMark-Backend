"""empty message

Revision ID: 65a531b495aa
Revises: f0bdc67fe179
Create Date: 2022-07-15 15:10:58.629524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65a531b495aa'
down_revision = 'f0bdc67fe179'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('annotation', sa.Column('annotation_name', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'annotation', ['annotation_name'])
    op.drop_column('annotation', 'downvotes')
    op.drop_column('annotation', 'content_html')
    op.drop_column('annotation', 'content')
    op.drop_column('annotation', 'mod_required')
    op.drop_column('annotation', 'upvotes')
    op.drop_column('annotation', 'parent_node')
    op.drop_column('annotation', 'tags')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('annotation', sa.Column('tags', sa.VARCHAR(), nullable=True))
    op.add_column('annotation', sa.Column('parent_node', sa.VARCHAR(), nullable=True))
    op.add_column('annotation', sa.Column('upvotes', sa.INTEGER(), nullable=True))
    op.add_column('annotation', sa.Column('mod_required', sa.BOOLEAN(), nullable=True))
    op.add_column('annotation', sa.Column('content', sa.VARCHAR(), nullable=False))
    op.add_column('annotation', sa.Column('content_html', sa.VARCHAR(), nullable=False))
    op.add_column('annotation', sa.Column('downvotes', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'annotation', type_='unique')
    op.drop_column('annotation', 'annotation_name')
    # ### end Alembic commands ###