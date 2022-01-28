"""content trust

Revision ID: 33ad0d922aaa
Revises: dadfc30be670
Create Date: 2021-09-15 11:28:40.198439

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '33ad0d922aaa'
down_revision = 'dadfc30be670'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    content_trust_roles_args = [
        'content_trust_roles',
        sa.Column('id', sa.LargeBinary(length=16), nullable=True, unique=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('channel', sa.String(), nullable=False),
        sa.Column('version', sa.BigInteger(), nullable=False),
        sa.Column('timestamp', sa.String(), nullable=False),
        sa.Column('expiration', sa.String(), nullable=False),
        sa.Column('delegator_id', sa.LargeBinary(length=16), nullable=True),
        sa.Column(
            'time_created',
            sa.Date(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('type', 'channel', 'version'),
    ]
    if op.get_context().dialect.name != 'postgresql':
        content_trust_roles_args.append(
            sa.ForeignKeyConstraint(
                ['delegator_id'],
                ['role_delegations.id'],
            )
        )
    op.create_table(*content_trust_roles_args)

    op.create_table(
        'role_delegations',
        sa.Column('id', sa.LargeBinary(length=16), nullable=False),
        sa.Column('issuer_id', sa.LargeBinary(length=16), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('channel', sa.String(), nullable=False),
        sa.Column('threshold', sa.BigInteger(), nullable=False),
        sa.Column(
            'time_created',
            sa.Date(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['issuer_id'],
            ['content_trust_roles.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )

    if op.get_context().dialect.name == 'postgresql':
        op.create_foreign_key(
            'content_trust_roles_delegator_id',
            'content_trust_roles',
            'role_delegations',
            ['delegator_id'],
            ['id'],
        )
    op.create_table(
        'signing_keys',
        sa.Column('public_key', sa.String(), nullable=False),
        sa.Column('private_key', sa.String(), nullable=True),
        sa.Column(
            'time_created',
            sa.Date(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.Column('user_id', sa.LargeBinary(length=16), nullable=True),
        sa.Column('channel_name', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ['channel_name'],
            ['channels.name'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('public_key'),
    )
    op.create_table(
        'delegations_keys',
        sa.Column('role_delegations_id', sa.LargeBinary(length=16), nullable=False),
        sa.Column('signing_keys_public_key', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['role_delegations_id'],
            ['role_delegations.id'],
        ),
        sa.ForeignKeyConstraint(
            ['signing_keys_public_key'],
            ['signing_keys.public_key'],
        ),
        sa.PrimaryKeyConstraint('role_delegations_id', 'signing_keys_public_key'),
    )
    op.drop_table('repodata_signing_keys')
    with op.batch_alter_table('channels', schema=None) as batch_op:
        batch_op.alter_column(
            'size',
            existing_type=sa.INTEGER(),
            type_=sa.BigInteger(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            'size_limit',
            existing_type=sa.INTEGER(),
            type_=sa.BigInteger(),
            existing_nullable=True,
        )

    with op.batch_alter_table('package_versions', schema=None) as batch_op:
        batch_op.alter_column(
            'size',
            existing_type=sa.INTEGER(),
            type_=sa.BigInteger(),
            existing_nullable=True,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('package_versions', schema=None) as batch_op:
        batch_op.alter_column(
            'size',
            existing_type=sa.BigInteger(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )

    with op.batch_alter_table('channels', schema=None) as batch_op:
        batch_op.alter_column(
            'size_limit',
            existing_type=sa.BigInteger(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            'size',
            existing_type=sa.BigInteger(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )

    op.create_table(
        'repodata_signing_keys',
        sa.Column('id', sa.BLOB(), nullable=False),
        sa.Column('private_key', sa.VARCHAR(), nullable=True),
        sa.Column(
            'time_created',
            sa.DATE(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.Column('user_id', sa.BLOB(), nullable=True),
        sa.Column('channel_name', sa.VARCHAR(), nullable=True),
        sa.ForeignKeyConstraint(
            ['channel_name'],
            ['channels.name'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.drop_table('delegations_keys')
    op.drop_table('signing_keys')
    op.drop_table('role_delegations')
    op.drop_table('content_trust_roles')
    # ### end Alembic commands ###
