"""create_user

Revision ID: 9d18b9bb73f4
Revises: 
Create Date: 2025-08-10 11:39:52.839349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from src.schemas.user_schemas import PortalRole

# revision identifiers, used by Alembic.
revision: str = '9d18b9bb73f4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table(
        'user_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=30), nullable=False),
        sa.Column('fullname', sa.String(length=30), nullable=True),
        sa.Column('email', sa.String(length=30), nullable=False),
        sa.Column('hashed_password', sa.String(length=64), nullable=False),
        sa.Column('disabled', sa.Boolean(), nullable=False),
        sa.Column('roles', postgresql.ARRAY(sa.String()), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username', 'email', name='uq_username_email'),
    )

    op.bulk_insert(
        sa.table(
            "user_account",
            sa.column("id", sa.Integer),
            sa.column("username", sa.String(30)),
            sa.column("fullname", sa.String(30)),
            sa.column("email", sa.String(30)),
            sa.column("hashed_password", sa.String(64)),
            sa.column("disabled", sa.Boolean),
            sa.column("roles", postgresql.ARRAY(sa.String)),
        ),
        [
            {
                "id": 1,
                "username": "johndoe",
                "fullname": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                "disabled": False,
                "roles": ["USER_ADMIN", "TUTOR", "STUDENT"],
            }
        ],
    )


def downgrade() -> None:
    op.drop_table('users_accounts')
