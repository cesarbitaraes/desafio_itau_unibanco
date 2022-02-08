"""
    Funções gerais para interação com o banco de dados.
"""
from enum import Enum

from alembic import command as alembic_commands
from alembic.config import Config

alembic_configuration = Config('alembic.ini')


class MigrationType(Enum):
    """
        Tipo de comandos disponíveis para execução.
    """
    upgrade = 'upgrade'
    downgrade = 'downgrade'


def run_migration(migration_type: MigrationType, revision: str):
    """
        Executa o comando informado utilizado a API do alembic.

        Exemplo: run_migration(MigrationType.upgrade, 'head')

    :param migration_type: Tipo do comando para execução. Opções disponíveis no enum MigrationType
    :param revision: Revisão alvo.
    :return: None
    """
    getattr(alembic_commands, migration_type.value)(alembic_configuration, revision)
