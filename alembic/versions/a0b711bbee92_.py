"""

Revision ID: a0b711bbee92
Revises: 
Create Date: 2018-02-04 19:02:44.441646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0b711bbee92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('urod_id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('send_msg', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('format', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('urod_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news')
    # ### end Alembic commands ###
