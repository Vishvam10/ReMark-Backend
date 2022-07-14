"""empty message

Revision ID: 83b627cc5fbd
Revises: 02473db39a05
Create Date: 2022-07-14 20:50:06.015689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83b627cc5fbd'
down_revision = '02473db39a05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('annotation',
    sa.Column('annotation_id', sa.String(), nullable=False),
    sa.Column('website_id', sa.String(), nullable=False),
    sa.Column('website_url', sa.String(), nullable=False),
    sa.Column('website_uri', sa.String(), nullable=False),
    sa.Column('html_node_id', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('content_html', sa.String(), nullable=False),
    sa.Column('parent_node', sa.String(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.Column('upvotes', sa.Integer(), nullable=True),
    sa.Column('downvotes', sa.Integer(), nullable=True),
    sa.Column('resolved', sa.Boolean(), nullable=True),
    sa.Column('mod_required', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('annotation_id', 'website_id'),
    sa.UniqueConstraint('annotation_id'),
    sa.UniqueConstraint('html_node_id'),
    sa.UniqueConstraint('website_id')
    )
    op.create_table('token',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('api_key', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('api_key'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email_id', sa.String(), nullable=False),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('authority', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email_id'),
    sa.UniqueConstraint('password'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('website',
    sa.Column('website_id', sa.String(), nullable=False),
    sa.Column('website_url', sa.String(), nullable=False),
    sa.Column('n_annotations', sa.Integer(), nullable=True),
    sa.Column('annotation_limit', sa.Integer(), nullable=True),
    sa.Column('admin', sa.String(), nullable=False),
    sa.Column('admin_type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('website_id'),
    sa.UniqueConstraint('admin'),
    sa.UniqueConstraint('website_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('website')
    op.drop_table('user')
    op.drop_table('token')
    op.drop_table('annotation')
    # ### end Alembic commands ###