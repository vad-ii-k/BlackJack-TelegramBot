"""added game tables

Revision ID: a66b1e6a53cc
Revises: 79ae3b07a903
Create Date: 2023-03-03 00:04:53.104586

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a66b1e6a53cc"
down_revision = "79ae3b07a903"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chats",
        sa.Column(
            "chat_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("chat_id"),
    )
    op.create_table(
        "users",
        sa.Column(
            "tg_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("tg_id"),
    )
    op.create_table(
        "games",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "state",
            sa.Enum("created", "in_progress", "finished", name="gamestate"),
            server_default="created",
            nullable=True,
        ),
        sa.Column("message_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chats.chat_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "players",
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=True),
        sa.Column("hand", sa.Text(), nullable=False, default=""),
        sa.Column("score", sa.Text(), nullable=False, default="0/0"),
        sa.Column("balance", sa.Integer(), nullable=False, default=10000),
        sa.Column("bet", sa.Integer(), nullable=True),
        sa.Column(
            "state",
            sa.Enum(
                "waiting_for_hand",
                "makes_turn",
                "waiting_for_results",
                "won",
                "draw",
                "lost",
                name="playerstate",
            ),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.id"],
        ),
        sa.ForeignKeyConstraint(["tg_id"], ["users.tg_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("tg_id"),
    )
    op.create_table(
        "players_statistics",
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.Column("games_played", sa.Integer(), nullable=True),
        sa.Column("games_won", sa.Integer(), nullable=True),
        sa.Column("games_lost", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tg_id"], ["players.tg_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("tg_id"),
    )


def downgrade() -> None:
    op.drop_table("players_statistics")
    op.drop_table("players")
    op.drop_table("games")
    op.drop_table("users")
    op.drop_table("chats")
    op.execute("DROP TYPE gamestate")
    op.execute("DROP TYPE playerstate")
