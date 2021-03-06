"""haiku title

Revision ID: 3dddf98dadce
Revises: 1cc51b9a4add
Create Date: 2013-07-12 22:16:15.303441

"""

# revision identifiers, used by Alembic.
revision = '3dddf98dadce'
down_revision = '1cc51b9a4add'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('haiku', sa.Column('title', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('haiku', 'title')
    ### end Alembic commands ###
