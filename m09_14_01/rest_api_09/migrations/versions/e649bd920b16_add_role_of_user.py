"""add role of user

Revision ID: e649bd920b16
Revises: 9c317d88a794
Create Date: 2023-04-13 19:51:03.175603

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e649bd920b16'
down_revision = '9c317d88a794'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE role AS ENUM('admin', 'moderator', 'user')")
    op.add_column('users',
                  sa.Column('roles', sa.Enum('admin', 'moderator', 'user', name='role'), nullable=True, default='user'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'roles')
    op.execute("DROP TYPE role")
    # ### end Alembic commands ###
