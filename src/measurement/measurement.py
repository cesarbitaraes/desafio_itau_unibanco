from src.models.fees import Taxas
from src.services.database import Session
from src.schemas.measurement import CalculateTaxForeignCurrencyInput
from src.measurement.base import MeasurementResult


class Measurement:
    """
        Classe onde estarão todos os cálculos.
    """
    def foreign_currency(self,
                         payload: CalculateTaxForeignCurrencyInput,
                         conn: Session):
        """
        Função responsável por calcular o valor em reais de uma
        quantidade determinado de moeda estrangeira, levando em conta
        as taxas envolvidas.
        :param payload: Payload que armazena os parâmetros necessários para
        o cálculo.
        :param conn: Conexão com o banco de dados.
        :return: Objeto do tipo MeasurementResult contendo o status e o valor final do cálculo.
        """
        segmento = payload.cal_en_cliente.name
        taxa_segmento = Taxas.obtem_taxa_por_cliente_e_tipo(db_session=conn,
                                                            cliente=segmento,
                                                            tipo='MOEDA_ESTRANGEIRA')
        if not taxa_segmento:
            return MeasurementResult(status=401,
                                     value=0)
        valor_reais = (payload.cal_vl_moeda_estrangeira * payload.cal_vl_taxa_conversao) * \
                      (1 + taxa_segmento.tax_vl_valor)
        return MeasurementResult(status=200,
                                 value=round(valor_reais, 2))
