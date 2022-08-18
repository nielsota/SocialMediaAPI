"""add users table

Revision ID: 7f6d1ddc1bd2
Revises: 942581d1bcf2
Create Date: 2022-08-16 10:21:21.659677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f6d1ddc1bd2'
down_revision = '942581d1bcf2'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )

def downgrade() -> None:
    op.drop_table('users')
