"""create posts table

Revision ID: 942581d1bcf2
Revises: 
Create Date: 2022-08-16 10:18:26.008490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '942581d1bcf2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('posts')
