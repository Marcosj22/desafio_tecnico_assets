-- o script crias as tabelas na seguinte ordem: associado --> conta --> cartao --> movimento

--cria schema no banco 

CREATE SCHEMA IF NOT EXISTS db_cartoes;

--tbl de associado 
CREATE TABLE IF NOT EXISTS db_cartoes.associado (
    id          INTEGER PRIMARY KEY,
    nome        VARCHAR NOT NULL,
    sobrenome   VARCHAR NOT NULL,
    idade       INTEGER NOT NULL,
    email       VARCHAR NOT NULL
);

--tbl de conta 
CREATE TABLE IF NOT EXISTS db_cartoes.conta (
    id              INTEGER PRIMARY KEY,
    tipo            VARCHAR NOT NULL, -- No diagrama esta como tipo_conta, por falta de definição coloquei como varchar
    data_criacao    TIMESTAMP NOT NULL,
    id_associado    INTEGER NOT NULL,
    
    CONSTRAINT fk_conta_associado
        FOREIGN KEY (id_associado)
        REFERENCES db_cartoes.associado (id)
);

--tbl de cartao
CREATE TABLE IF NOT EXISTS db_cartoes.cartao (
    id              INTEGER PRIMARY KEY,
    num_cartao      INTEGER NOT NULL,
    nom_impresso    VARCHAR(100) NOT NULL,
    id_conta        INTEGER NOT NULL,
    id_associado    INTEGER NOT NULL,

    CONSTRAINT fk_cartao_conta
        FOREIGN KEY (id_conta)
        REFERENCES db_cartoes.conta (id),

    CONSTRAINT fk_cartao_associado
        FOREIGN KEY (id_associado)
        REFERENCES db_cartoes.associado (id)
);

CREATE TABLE IF NOT EXISTS db_cartoes.movimento (
    id              INTEGER PRIMARY KEY,
    vlr_transacao   DECIMAL(10, 2) NOT NULL,
    des_transacao   VARCHAR NOT NULL,
    data_movimento  TIMESTAMP NOT NULL,
    id_cartao       INTEGER NOT NULL,

    CONSTRAINT fk_movimento_cartao
        FOREIGN KEY (id_cartao)
        REFERENCES db_cartoes.cartao (id)
);