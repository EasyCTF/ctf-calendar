"""empty message

Revision ID: 4716a9303c39
Revises: 06cfdde7ecc1
Create Date: 2016-06-12 14:23:07.089563

"""

# revision identifiers, used by Alembic.
revision = '4716a9303c39'
down_revision = '06cfdde7ecc1'

from alembic import op


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_events_start_time', table_name='events')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_events_start_time', 'events', ['start_time'], unique=False)
    ### end Alembic commands ###
