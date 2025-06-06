"""text body

Revision ID: b92c238ef099
Revises: 43c70d802db1
Create Date: 2025-05-27 13:08:58.057458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b92c238ef099'
down_revision = '43c70d802db1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.VARCHAR(length=140),
               type_=sa.Text(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=140),
               existing_nullable=False)

    # ### end Alembic commands ###
