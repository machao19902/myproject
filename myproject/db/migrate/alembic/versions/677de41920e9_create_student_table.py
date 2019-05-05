"""Create student table

Revision ID: 677de41920e9
Revises: 


"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '677de41920e9'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'student',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('userId', sa.String(256), nullable=False),
        sa.Column('name', sa.String(128), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_student_userId', 'student', ['userId'], unique=True)


def downgrade():
    op.drop_table('student')
