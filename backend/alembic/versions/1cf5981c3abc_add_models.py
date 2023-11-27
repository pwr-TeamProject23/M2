"""Add models

Revision ID: 1cf5981c3abc
Revises: 
Create Date: 2023-11-27 10:03:14.196296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cf5981c3abc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('task_id', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'RECEIVED', 'STARTED', 'SUCCESS', 'FAILURE', 'REVOKED', 'REJECTED', 'RETRY', 'IGNORED', name='celerytaskstatus'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.String(), nullable=False),
    sa.Column('expiration_datetime', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('upload_id', sa.Integer(), nullable=False),
    sa.Column('author_external_id', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('affiliation', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('source', sa.Enum('DBLP', 'GoogleScholar', 'Scopus', name='source'), nullable=False),
    sa.ForeignKeyConstraint(['upload_id'], ['upload.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('author')
    op.drop_table('user_session')
    op.drop_table('upload')
    op.drop_table('user')
    # ### end Alembic commands ###
