"""
Desenvolva um sistema simples de gerenciamento de uma biblioteca utilizando classes e objetos.
O sistema deve permitir o gerenciamento de livros e usuários.
Cada livro terá informações como título, autor, ano de publicação e status (disponível ou emprestado).
Os usuários poderão emprestar ou devolver livros.
"""

import uuid
import json
import pandas as pd
import psycopg2



def conectar() -> psycopg2:
    try:
        connection = psycopg2.connect(
            dbname="library",
            user="marcos",
            password="marcos",
            host="localhost",
            port="5432"
        )
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao PostgreSQL:", error)
        connection.close()
        return None
    return connection

class Livros:
    def __init__(self,  titulo: str, autor: str, ano: int) -> None:
        self.id = str(uuid.uuid4())
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = True

        self.editora = 'Casa de Oração'

    def __str__(self) -> str:
        status = 'Disponivel' if self.disponivel else 'Emprestado'
        info = {
            'id': str(self.id),
            'titulo': self.titulo,
            'autor': self.autor,
            'ano': self.ano,
            'editora': self.editora,
            'status': status
        }
        return json.dumps(info, indent=4)

class Usuario:
    def __init__(self, nome: str, sobrenome: str, email: str, telefone: int) -> None:
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.telefone = telefone
        conexao = conectar()
        cur = conexao.cursor()
        cur.execute('INSERT INTO usuarios (nome, sobrenome, email, telefone) VALUES (%s, %s, %s, %s)',
                    (self.nome, self.sobrenome, self.email, self.telefone))
    
    def __str__(self):
        dados_usuario: dict = {
            'Nome': self.nome,
            'Livro(s) emprestados': self.livros_emprestados,
        }
        return str(dados_usuario)

class Biblioteca:
    def __init__(self):
        self.catalogo = dict()
        self.usuarios_registrados = list()

    #CREATE
    def adicionar_livro(self, livro: Livros) -> None:
        conexao = conectar()
        cur = conexao.cursor()
        try:
            cur.execute(f'''
                INSERT INTO livros (id, titulo, autor, ano, disponivel, editora)
                VALUES (%s, %s, %s, %s, %s, %s);
                ''', (livro.id, livro.titulo, livro.autor, livro.ano, livro.disponivel, livro.editora))
            conexao.commit()
            print(f'O livro {livro.titulo} foi adicionado ao catálogo!')
        except Exception as error:
            print(error)
        finally:
            conexao.close()

    #READ
    def listar_livros(self):
        conexao = conectar()
        cur = conexao.cursor()
        try:
            cur.execute('SELECT * FROM livros;')
        except Exception as error:
            print(error)
            conexao.close()
            return None
        rows = cur.fetchall()
        for i in rows:
            print(i)

    #UPDATE
    def alterar_dados(self, usuario: Usuario|None = None, livro: Livros|None = None, query: str|None = None):
        conexao = conectar()
        cur = conexao.cursor()
        try:
            cur.execute(query)
            print('a alteração foi executada!')
        except Exception as error:
            print(error)
        finally:
            conexao.close()
        
    #DELETE
    def remover_livro(self, livro: Livros) -> None:
        conexao = conectar()
        cur = conexao.cursor()
        try:
            cur.execute('''
                DELETE FROM Livros
                        WHERE id = (?)
            ''', livro.id)
            print(f'O livro {livro.titulo} foi excluído!')
        except Exception as error:
            print(error)
        finally:
            conexao.close()
    
    def listar_livros_disponiveis(self) -> list:
        disponiveis = [livro for livro in self.catalogo.values() if livro.disponivel]
        if disponiveis:
            print('Livros disponíveis na biblioteca:')
            for livro in disponiveis:
                print(livro)
        else:
            print('Não há livros disponíveis.')
        return disponiveis

    def emprestar_livro(self, livro_id: str, usuario: Usuario):
        #conectar na bd
        conexao = conectar()
        cur = conexao.cursor()
        
        #executar query para alterar registro do usuário
        cur.execute()



        if usuario not in self.usuarios_registrados:
            self.usuarios_registrados.append(usuario.nome)
        livro = self.catalogo.get(livro_id)
        if not livro:
            print('Este livro não está no catálogo!')
            return
        if not livro.disponivel:
            print('Este livro não está disponível para empréstimo!')
            return
        livro.disponivel = False
        usuario.livros_emprestados.append(livro)
        print(f'o livro foi emprestado para {usuario.nome} com sucesso!')
    
    def devolver_livro(self, livro_id: str, usuario):
        livro = self.catalogo.get(livro_id)
        if not livro:
            print('Este livro não está no catálogo!')
            return
        if livro.disponivel:
            print('Este livro já está disponível! Não há o que devolver')
            return
        usuario.livros_emprestados.remove(livro)
        print(f'O livro {livro.titulo} foi devolvido por {usuario.nome}!')

    def listar_usuarios(self):
        print(self.usuarios_registrados)

    def excluir_usuario(self, nome_usuario: str):
        if nome_usuario not in self.usuarios_registrados:
            print('Este usuário não é desta biblioteca!')
            return
        self.usuarios_registrados.remove(nome_usuario)


def main():
    livrao = Livros('hamburguer chorando', 'autor muito maneiro', 2005)
    lib = Biblioteca()
    lib.adicionar_livro(livrao)
    marquin = Usuario('marquin', 'Sacramento', 'sacramento.marcosf@gmail.com', 31971722247)
    lib.emprestar_livro(str(livrao.id), marquin)
    lib.listar_usuarios()
    lib.listar_livros()

if __name__ == "__main__":
    main()
