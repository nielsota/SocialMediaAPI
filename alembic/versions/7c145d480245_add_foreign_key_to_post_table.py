"""add foreign key to post table

Revision ID: 7c145d480245
Revises: 7f6d1ddc1bd2
Create Date: 2022-08-17 09:05:49.131364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c145d480245'
down_revision = '7f6d1ddc1bd2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.add_column('posts', sa.Column('content', sa.Integer(), nullable=False))
    
    op.create_foreign_key(
        'posts_users_fk', 
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'owner_id')
