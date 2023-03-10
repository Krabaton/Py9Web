"""add table contacts

Revision ID: 5235de6c07eb
Revises: 6a469539a9ec
Create Date: 2023-03-02 20:42:43.972917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5235de6c07eb'
down_revision = '6a469539a9ec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=False),
    sa.Column('last_name', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('phone', sa.String(length=150), nullable=False),
    sa.Column('address', sa.String(length=150), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contacts')
    # ### end Alembic commands ###
