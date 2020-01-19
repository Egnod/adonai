"""empty message.

Revision ID: first_start
Revises: a6387d2c9a49
Create Date: 2020-01-19 02:51:53.698992
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from adonai.app.permission import get_internal_permissions_names


# revision identifiers, used by Alembic.
revision = 'first_start'
down_revision = 'a6387d2c9a49'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO domain (uuid, name, is_active) VALUES ('00000000-0000-0000-0000-000000000000', 'Base', true)")
    op.execute("INSERT INTO \"user\" (domain_id, login, password_hash, uuid, first_name, last_name, internal_auth) VALUES ((SELECT id FROM domain WHERE uuid='00000000-0000-0000-0000-000000000000'), 'admin', '$argon2id$v=19$m=102400,t=2,p=8$q7XWWktp7X3Pee+d05oz5g$bHjHhhF30g3GNp27repW3w', '00000000-0000-0000-0000-000000000000', 'test', 'test', true)")

    permissions = get_internal_permissions_names()

    for permission in permissions:
        op.execute(f"INSERT INTO permission (name, type) VALUES ('{permission}', 'internal')")
        op.execute(f"INSERT INTO user_permission (user_id, permission_id) VALUES ((SELECT \"user\".id FROM \"user\" WHERE uuid='00000000-0000-0000-0000-000000000000'), (SELECT permission.\"id\" FROM public.permission WHERE name='{permission}'))")


def downgrade():
    pass