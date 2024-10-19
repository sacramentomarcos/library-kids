requisicao = ['''
    CREATE TABLE IF NOT EXISTS emprestimos(
    "id" BIGINT PRIMARY KEY NOT NULL,
    "id_livro" VARCHAR(255) NOT NULL,
    "id_usuario" INTEGER NOT NULL,
    "data_emprestimo" DATE NOT NULL,
    "data_renovacao" DATE,
    "data_devolucao" DATE
);''',
'''CREATE TABLE IF NOT EXISTS livros(
    "id" VARCHAR(255) PRIMARY KEY NOT NULL,
    "titulo" VARCHAR(255) NOT NULL,
    "autor" VARCHAR(255) NOT NULL,
    "ano" INTEGER NOT NULL,
    "editora" VARCHAR(255) NOT NULL,
    "disponivel" VARCHAR(255) NOT NULL
);''',
'''CREATE TABLE IF NOT EXISTS usuarios(
    "id" INTEGER PRIMARY KEY NOT NULL,
    "nome" VARCHAR(255) NOT NULL,
    "sobrenome" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "telefone" BIGINT NOT NULL
);''',
'''
ALTER TABLE
    emprestimos ADD CONSTRAINT emprestimos_id_livro_foreign FOREIGN KEY(id_livro) REFERENCES livros(id);''',
'''
ALTER TABLE
    emprestimos ADD CONSTRAINT emprestimos_id_usuario_foreign FOREIGN KEY(id_usuario) REFERENCES usuarios(id);''']

exclude = ['''
        DROP TABLE emprestimos CASCADE
    ''',
    '''DROP TABLE usuarios CASCADE
    ''',
    '''DROP TABLE livros CASCADE
    ''']
