"""Add files table

Revision ID: 43e4eb2f8ee
Revises: 48ff3ef1bd6
Create Date: 2015-08-12 22:36:32.769607

"""

# revision identifiers, used by Alembic.
revision = '43e4eb2f8ee'
down_revision = '48ff3ef1bd6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=32), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    with op.batch_alter_table('photogalleryitems') as batch_op:
        batch_op.add_column(sa.Column('file_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('photogalleryitems_files', 'files', ['file_id'], ['id'])
        batch_op.drop_column('url')

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photogalleryitems') as batch_op:
        batch_op.add_column(sa.Column('url', sa.VARCHAR(length=2000), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('file_id')

    op.drop_table('files')
    ### end Alembic commands ###
