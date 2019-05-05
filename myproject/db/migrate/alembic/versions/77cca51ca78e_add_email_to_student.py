"""add email to student

Revision ID: 77cca51ca78e
Revises: 677de41920e9

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77cca51ca78e'
down_revision = '677de41920e9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('student', sa.Column('email', sa.String(256), nullable=True))


def downgrade():
    op.drop_column('student', 'email')
