## Introdução

Esta API foi desenvolvida na linguagem Python com banco de dados PostgreSQL e tem como objetivo armazenar
taxas para vários segmentos (PRIVATE, VAREJO e PERSONNALITE) e realizar métricas envolvendo essas taxas.
Hoje a única métrica implementada é a conversão de moeda estrangeira em reais.


## Tecnologias

A implementação foi realizado utilizando Python na versão 3.7 com as seguintes bibliotecas:

 - FastAPI
 - sqlalchemy
 - uvicorn
 - alembic
 - pytest
 - coverage

### Estrutura

```shell
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions                                                    # Arquivos de migrações
│       └── 2022-02-08T21:14:14_213cfac10167_create_table_taxas.py
├── alembic.ini
├── api_entrypoint.sh                                                     # Entrypoint
├── docker-compose.yaml                                                   # docker-compose
├── Dockerfile                                                            # Arquivo de deploy
├── Pipfile                                                               # Dependências do pipenv
├── Pipfile.lock                                                          # Arquivo com o hash e versões das dependências
├── README.md
├── requirements.txt                                                      # Dependências
├── src
│   ├── app.py
│   ├── __init__.py
│   ├── measurement
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── measurement.py
│   ├── models
│   │   ├── clients.py
│   │   ├── fees.py
│   │   └── __init__.py
│   ├── resources
│   │   ├── calculated_values.py
│   │   ├── fees.py
│   │   ├── healthcheck.py
│   │   └── __init__.py
│   ├── schemas
│   │   ├── fee.py
│   │   ├── __init__.py
│   │   └── measurement.py
│   ├── services
│   │   ├── database.py
│   │   └── __init__.py
│   ├── settings.py
│   └── utils
│       ├── database.py
│       └── __init__.py
└── tests                                                             # Implementação de testes
          ├── conftest.py                                             # Fixtures do pytest
          └── resources
             ├── test_calculated_values.py
             ├── test_fees.py
             └── test_healthcheck.py
```

Onde:
* src/measurement: classe responsável por armazenar a implementação de todas as métricas executadas pela API;
* src/models: contém todos os modelos do banco de dados;
* src/resources: toda a implementação de cada rota está nesse diretório;
* src/schemas: implementação de todos os schemas do Pydantic;
* src/services: funções relacionanas à conexão com o banco de dados;
* src/utils: funções auxiliares.

## Executando a API:

Para executar a API é necessário ter instalado em seu ambiente `docker` e `docker-compose`.
```shell
# Constrói a aplicação:
$ docker-compose build

# Sobe todos os containers:
$ docker-compose up
```
A partir desse ponto todos os containers estarão disponíveis.
Para acessar o `swagger` da aplicação basta abrir em seu navegador o endereço `http://localhost:5000/docs`.
Toda a documentação da API está disponível em `http://localhost:5000/redoc`.

### Rotas implementadas:

Essas são as rotas implementadas:
* `GET/api/healthcheck`: indica se a API está ou não online;
* `GET/fees/`: retorna todas as taxas armazenadas no banco de dados;
* `POST/fees/`: registra uma taxa para um determinado segmento;
* `PATCH/fees/`: atualiza uma taxa previamente cadastrada;
* `POST/calculate_foreign_currency/`: retorna o valor em reais, incluindo todas as taxas e conversões, de um determinado valor de moeda estrangeira.

## Desenvolvimento

A estrutura contida no arquivo `docker-compose.yaml` fornece containers distintos para a API e banco de dados.

### Banco de dados

Todas as alterações relacionadas ao banco de dados devem ser feitas utilizando o `alembic`. Para criar uma nova migração basta executar o comando `docker exec desafio-itau-api alembic revision -m "<descrição>` e adicionar as modificações nos métodos `upgrade()` para a implantação e `downgrade()` para o rollback.

### Testes

Para executar os testes basta inserir os seguintes comandos no seu terminal:

```shell
# Executa os testes com coverage para gerar o relatório de cobertura:
$ docker exec desafio-itau-api coverage run -m pytest

# Exibe o relatório e lista as linhas que não estão cobertas pelos testes:
$ docker exec desafio-itau-api coverage report -m
```

Atualmente essa API contém uma cobertura de testes de 92% de seu código.

### Dependências

Caso seja necessário adicionar dependências no projeto, as mesmas devem ser incluídas nos arquivos `requirements.txt` utilizando o `pipenv`.
Exemplo:
```shell
# Vamos adicionar a lib hypothesis na lista de dependências:
$ pipenv install --dev hypothesis 

# Uma vez que a instalação foi concluída devemos atualizar os arquivos mencionados acima:
$ pipenv lock -r > requirements.txt
```

#### Pipenv

O projeto utiliza o `pipenv` para gestão de ambientes virtuais. Caso deseje utilizá-lo, basta efetuar a instalação no interpretador global com o comando `pip install pipenv`. Detalhes [aqui](https://pipenv.pypa.io/en/latest/#install-pipenv-today).
