"""Add initial tables and supertokens_user_id

Revision ID: c9e81b7e6c99
Revises: 8f350bbc5e33
Create Date: 2025-04-18 11:04:42.321170

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c9e81b7e6c99"
down_revision: Union[str, None] = "8f350bbc5e33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "educational_frameworks", ["name"])
    op.drop_index("ix_project_settings_project_id", table_name="project_settings")
    op.create_index(
        op.f("ix_project_settings_project_id"),
        "project_settings",
        ["project_id"],
        unique=True,
    )
    op.add_column("users", sa.Column("supertokens_user_id", sa.String(), nullable=True))
    op.create_index(
        op.f("ix_users_supertokens_user_id"),
        "users",
        ["supertokens_user_id"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_supertokens_user_id"), table_name="users")
    op.drop_column("users", "supertokens_user_id")
    op.drop_index(op.f("ix_project_settings_project_id"), table_name="project_settings")
    op.create_index(
        "ix_project_settings_project_id",
        "project_settings",
        ["project_id"],
        unique=False,
    )
    op.drop_constraint(None, "educational_frameworks", type_="unique")
    # ### end Alembic commands ###
