"""
    Classe base que fornece operações de atualização, gravação e remoção
    para as classes que a herdarem.
"""

from typing import Tuple, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class BasicModel:
    """
        Classe base com os métodos para atualização, gravação e remoção de
        registros no banco de dados.
    """

    def update(self, db_session: Session, **kwargs) -> Tuple[bool, Optional[str]]:
        """
        Atualiza os valores de um objeto dinamicamente e efetua o commit.

        :param db_session: Conexão com o banco de dados.
        :param kwargs: Atributos para alteração
        :returns: Tuple(bool, Optional[str])
            - (True, None): Registro salvo no sistema.
            - (False, str): Erro ao salvar o registro e a mensagem descritiva
        """
        try:
            for (attribute, _) in self.__dict__.items():
                if kwargs.get(attribute):
                    setattr(self, attribute, kwargs.get(attribute))
            db_session.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, " ".join(error.args)

    def save(self, db_session: Session) -> Tuple[bool, Optional[str]]:
        """
        Salva a instância da classe no banco de dados.

        :param db_session: Conexão com o banco de dados
        :returns: Tuple(bool, Optional[str])
            - (True, None): Registro salvo no sistema.
            - (False, str): Erro ao salvar o registro e a mensagem descritiva
        """
        try:
            db_session.add(self)
            db_session.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, " ".join(error.args)

    def remove(self, db_session: Session) -> Tuple[bool, Optional[str]]:
        """
        Remove o objeto do banco de dados

        :param db_session: Conexão com o banco de dados.
        :returns: Tuple(bool, Optional[str])
            - (True, None): Registro salvo no sistema.
            - (False, str): Erro ao salvar o registro e a mensagem descritiva
        """
        try:
            db_session.delete(self)
            db_session.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, " ".join(error.args)
