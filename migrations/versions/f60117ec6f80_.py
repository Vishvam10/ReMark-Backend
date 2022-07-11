"""empty message

Revision ID: f60117ec6f80
Revises: 1a9d9f6baa80
Create Date: 2022-07-11 21:32:05.580882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f60117ec6f80'
down_revision = '1a9d9f6baa80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('website',
    sa.Column('website_id', sa.String(), nullable=False),
    sa.Column('website_url', sa.String(), nullable=False),
    sa.Column('website_uri', sa.String(), nullable=False),
    sa.Column('html_node', sa.String(), nullable=False),
    sa.Column('html_node_class', sa.String(), nullable=True),
    sa.Column('html_node_id', sa.String(), nullable=True),
    sa.Column('html_parent_node', sa.String(), nullable=True),
    sa.Column('depth_from_body', sa.Integer(), nullable=True),
    sa.Column('annotation_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['annotation_id'], ['annotation.annotation_id'], ),
    sa.PrimaryKeyConstraint('website_id'),
    sa.UniqueConstraint('website_id')
    )
    op.drop_table('html_node_data')
    op.add_column('annotation', sa.Column('website_id', sa.String(), nullable=False))
    op.add_column('annotation', sa.Column('resolved', sa.Boolean(), nullable=True))
    op.add_column('annotation', sa.Column('created_by', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'annotation', ['website_id'])
    op.add_column('user', sa.Column('bio', sa.String(), nullable=True))
    op.add_column('user', sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'webhook_url')
    op.drop_column('user', 'app_preferences')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('app_preferences', sa.VARCHAR(), nullable=False))
    op.add_column('user', sa.Column('webhook_url', sa.VARCHAR(), nullable=True))
    op.add_column('user', sa.Column('updated_at', sa.DATETIME(), nullable=True))
    op.drop_column('user', 'modified_at')
    op.drop_column('user', 'bio')
    op.drop_constraint(None, 'annotation', type_='unique')
    op.drop_column('annotation', 'created_by')
    op.drop_column('annotation', 'resolved')
    op.drop_column('annotation', 'website_id')
    op.create_table('html_node_data',
    sa.Column('website_id', sa.VARCHAR(), nullable=False),
    sa.Column('website_url', sa.VARCHAR(), nullable=False),
    sa.Column('html_node', sa.VARCHAR(), nullable=False),
    sa.Column('html_parent_node', sa.VARCHAR(), nullable=True),
    sa.Column('html_node_class', sa.VARCHAR(), nullable=True),
    sa.Column('html_node_id', sa.VARCHAR(), nullable=True),
    sa.Column('annotation_id', sa.VARCHAR(), nullable=False),
    sa.ForeignKeyConstraint(['annotation_id'], ['annotation.annotation_id'], ),
    sa.PrimaryKeyConstraint('website_id'),
    sa.UniqueConstraint('website_id')
    )
    op.drop_table('website')
    # ### end Alembic commands ###