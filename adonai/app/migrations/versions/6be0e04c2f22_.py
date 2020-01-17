"""empty message

Revision ID: 6be0e04c2f22
Revises: 1a36ada339d1
Create Date: 2020-01-16 18:57:17.620032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6be0e04c2f22"
down_revision = "1a36ada339d1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column(
            "internal_auth", sa.Boolean(), server_default="false", nullable=False
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "internal_auth")
    # ### end Alembic commands ###