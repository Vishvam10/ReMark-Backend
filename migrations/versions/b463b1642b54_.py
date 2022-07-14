"""empty message

Revision ID: b463b1642b54
Revises: d02ed65280b1
Create Date: 2022-07-14 18:36:17.471706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b463b1642b54'
down_revision = 'd02ed65280b1'
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
    op.create_table('user',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email_id', sa.String(), nullable=False),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('authority', sa.String(), nullable=False),
    sa.Column('api_key', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('api_key'),
    sa.UniqueConstraint('email_id'),
    sa.UniqueConstraint('password'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('annotation')
    # ### end Alembic commands ###
