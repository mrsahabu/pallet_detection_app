"""First Shot1

Revision ID: 91df7cc2e1a4
Revises: 
Create Date: 2024-05-31 13:24:02.142946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91df7cc2e1a4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=512), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('user_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('pallets_count', sa.Integer(), nullable=True),
    sa.Column('insert_time', sa.DateTime(), nullable=True),
    sa.Column('price_piece', sa.Float(), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=True),
    sa.Column('transport_fc_count', sa.Float(), nullable=True),
    sa.Column('co2_saving_count', sa.Float(), nullable=True),
    sa.Column('total_transport', sa.Float(), nullable=True),
    sa.Column('co2_fc', sa.Float(), nullable=True),
    sa.Column('transport_cost', sa.Float(), nullable=True),
    sa.Column('buy_or_sell', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_data_id'), 'user_data', ['id'], unique=False)
    op.create_table('image_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_id', sa.Integer(), nullable=True),
    sa.Column('img_path', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['data_id'], ['user_data.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_data_id'), 'image_data', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_image_data_id'), table_name='image_data')
    op.drop_table('image_data')
    op.drop_index(op.f('ix_user_data_id'), table_name='user_data')
    op.drop_table('user_data')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###