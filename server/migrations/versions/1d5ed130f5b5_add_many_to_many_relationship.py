"""add many to many relationship

Revision ID: 1d5ed130f5b5
Revises: 5af82fd411bc
Create Date: 2020-07-03 17:23:53.388906

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1d5ed130f5b5'
down_revision = '5af82fd411bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('event.id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['event.id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'event.id')
    )
    op.drop_column('event', 'image')
    op.drop_constraint('sport_current_events_fkey', 'sport', type_='foreignkey')
    op.drop_constraint('sport_active_members_fkey', 'sport', type_='foreignkey')
    op.drop_column('sport', 'current_events')
    op.drop_column('sport', 'active_members')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sport', sa.Column('active_members', postgresql.UUID(), autoincrement=False, nullable=True))
    op.add_column('sport', sa.Column('current_events', postgresql.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('sport_active_members_fkey', 'sport', 'user', ['active_members'], ['id'])
    op.create_foreign_key('sport_current_events_fkey', 'sport', 'event', ['current_events'], ['id'])
    op.add_column('event', sa.Column('image', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_table('events')
    # ### end Alembic commands ###