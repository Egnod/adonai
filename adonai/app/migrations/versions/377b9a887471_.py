"""empty message

Revision ID: 377b9a887471
Revises: 5a7c063a58b0
Create Date: 2020-01-13 19:08:27.978022

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "377b9a887471"
down_revision = "5a7c063a58b0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "user_group_permission_permission_id_fkey",
        "user_group_permission",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None, "user_group_permission", "permission", ["permission_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user_group_permission", type_="foreignkey")
    op.create_foreign_key(
        "user_group_permission_permission_id_fkey",
        "user_group_permission",
        "project",
        ["permission_id"],
        ["id"],
    )
    # ### end Alembic commands ###
