"""add last few columns to post table

Revision ID: 17b0bd65a549
Revises: 7c145d480245
Create Date: 2022-08-17 09:13:07.517898

"""
from email.policy import default
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17b0bd65a549'
down_revision = '7c145d480245'
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    # add a published column
    op.add_column(
        'posts',
        sa.Column(
            'published',
            sa.Boolean(),
            nullable=False,
            server_default='TRUE'
        )
    )

    # add a created at column
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('NOW()')
        )
    )


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
