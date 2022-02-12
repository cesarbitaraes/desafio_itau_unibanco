from enum import Enum as TypeEnum


class ClientOptions(TypeEnum):
    """
        Classe que define um objeto Enum para a coluna tax_en_cliente da tabela taxa.
    """
    VAREJO = "VAREJO"
    PERSONNALITE = "PERSONNALITE"
    PRIVATE = "PRIVATE"


class TaxType(TypeEnum):
    """
        Classe que define um objeto Enum para a coluna tax_tx_tipo da tabela taxa.
    """
    MOEDA_ESTRANGEIRA = "MOEDA_ESTRANGEIRA"
