"""
    Classes de mapeamento das tabelas relacionadas
    ao endereço.
"""
from typing import List
from sqlalchemy import Column, Integer, Float, DateTime, Enum

from src.models import BasicModel
from src.models.clients import ClientOptions, TaxType
from src.services.database import BaseModel, Session


class Taxas(BasicModel, BaseModel):
    """
    Classe de mapeamento da tabela taxa.
    Tabela com responsabilidade de manter os valores das taxas para cada segmento.
    """
    __tablename__ = 'taxa'
    tax_pk_taxa = Column(Integer, primary_key=True, autoincrement=True)
    tax_en_cliente = Column(Enum(ClientOptions), nullable=False)
    tax_en_tipo = Column(Enum(TaxType), nullable=False)
    tax_vl_valor = Column(Float, nullable=False)
    tax_dt_criacao = Column(DateTime, server_default="current_timestamp", nullable=False)
    tax_dt_atualizacao = Column(DateTime, nullable=True)

    @classmethod
    def obtem_taxa_por_cliente_e_tipo(cls,
                                      db_session: Session,
                                      cliente: ClientOptions,
                                      tipo: str) -> float:
        """
        Retorna a taxa dado o tipo e o segmento.
        :param db_session: Conexão com o banco de dados.
        :param cliente: Segmento do cliente.
        :param tipo: Tipo da taxa.
        :return: Objeto Taxas que representa um registro do banco de dados.
        """
        return db_session.query(cls).filter_by(tax_en_cliente=cliente,
                                               tax_en_tipo=tipo).first()

    @classmethod
    def obtem_taxa_por_id(cls,
                          db_session: Session,
                          id: int) -> "Taxas":
        """
        Retorna uma taxa armazenada dado o seu id.
        :param db_session: Conexão com o banco de dados.
        :param id: Identificação da taxa.
        :return: Objeto Taxas que representa um registro do banco de dados.
        """
        return db_session.query(cls).filter_by(tax_pk_taxa=id).first()


    @classmethod
    def obtem_todas_taxas(cls,
                          db_session: Session) -> List["Taxas"]:
        """
        Retorna todas as taxas armazenadas.
        :param db_session: Conexão com o banco de dados.
        :return: Uma lista de Taxas.
        """
        return db_session.query(cls).all()
