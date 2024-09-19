"""empty message

Revision ID: 4a481e70f3a1
Revises: 8c9dfda7057f
Create Date: 2024-09-19 15:29:24.088245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a481e70f3a1'
down_revision = '8c9dfda7057f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('height', sa.Integer(), nullable=True))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=80),
               nullable=True)
        batch_op.alter_column('gender',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=80),
               nullable=True)
        batch_op.drop_constraint('people_Homeworld_key', type_='unique')
        batch_op.drop_constraint('people_gender_key', type_='unique')
        batch_op.drop_constraint('people_hair_color_key', type_='unique')
        batch_op.drop_constraint('people_name_key', type_='unique')
        batch_op.drop_column('hair_color')
        batch_op.drop_column('Homeworld')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Homeworld', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('hair_color', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('people_name_key', ['name'])
        batch_op.create_unique_constraint('people_hair_color_key', ['hair_color'])
        batch_op.create_unique_constraint('people_gender_key', ['gender'])
        batch_op.create_unique_constraint('people_Homeworld_key', ['Homeworld'])
        batch_op.alter_column('gender',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.drop_column('height')
        batch_op.drop_column('description')

    # ### end Alembic commands ###
