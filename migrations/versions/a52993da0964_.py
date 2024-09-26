"""empty message

Revision ID: a52993da0964
Revises: 
Create Date: 2024-09-11 10:41:15.170277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a52993da0964'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('arvore',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('tipo', sa.String(length=3), nullable=False),
    sa.Column('identificador', sa.String(length=6), nullable=False),
    sa.Column('bloco', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('conversas',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('dialog_id', sa.String(length=10), nullable=False),
    sa.Column('current_block', sa.String(length=6), nullable=False),
    sa.Column('deal', sa.Integer(), nullable=True),
    sa.Column('started_on', sa.DateTime(), nullable=True),
    sa.Column('modified_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('dialog_id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('motivos',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('motivo_id', sa.Integer(), nullable=False),
    sa.Column('motivo', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('variaveis',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('dialog_id', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('variaveis')
    op.drop_table('motivos')
    op.drop_table('conversas')
    op.drop_table('arvore')
    # ### end Alembic commands ###
