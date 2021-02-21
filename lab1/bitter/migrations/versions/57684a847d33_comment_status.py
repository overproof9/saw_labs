"""Comment status

Revision ID: 57684a847d33
Revises: 77db36db96ac
Create Date: 2021-02-21 12:16:53.745253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57684a847d33'
down_revision = '77db36db96ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comment', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comment', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
