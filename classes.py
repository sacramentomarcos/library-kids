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
    def __init__(self, isbn: str, titulo: str, editora: str, autor: str, ano: int) -> None:
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.disponivel = True
        self.editora = editora

    def __str__(self) -> str:
        status = 'Disponivel' if self.disponivel else 'Emprestado'
        info = {
            'isbn': self.isbn,
            'titulo': self.titulo,
            'autor': self.autor,
            'ano': self.ano,
            'status': status,
        }
        return json.dumps(info, indent=4)
    
class LivrosRepositorio:
    def __init__(self, livro: Livros):
        try:
            conexao = conectar()
            cur = conexao.cursor()
            cur.execute('INSERT INTO livros (titulo, autor, ano, editora, disponivel, isbn) VALUES (%s, %s, %s, %s, %s, %s)',
                        (livro.titulo, livro.autor, livro.ano, livro.editora, livro.isbn))
        except Exception as error:
            print('Não foi possível cadastrar o livro', error)
        finally:
            cur.close()
            conexao.close()

class Usuario:
    def __init__(self, nome: str, sobrenome: str, email: str, telefone: str) -> None:
        self.nome = nome.lower()
        self.sobrenome = sobrenome.lower()
        self.email = email.lower()
        self.telefone = telefone

    def __str__(self):
        dados_usuario: dict = {
            'Nome': self.nome,
            'Livro(s) emprestados': self.livros_emprestados,
        }
        return str(dados_usuario)

class UsuarioRepositorio:
    def __init__(self):
        self.conexao = conectar()

    def inserir_usuario(self, usuario: Usuario):
        try:
            cur = self.conexao.cursor()
            cur.execute('INSERT INTO usuarios (nome, sobrenome, email, telefone) VALUES (%s, %s, %s, %s)',
                        (usuario.nome, usuario.sobrenome, usuario.email, usuario.telefone))
        except Exception as error:
            print('não foi possível cadastrar usuário', error)
        finally:
            cur.close()
            self.conexao.close()

class Biblioteca:
    def __init__(self):
        self.catalogo = dict()
        self.usuarios_registrados = list()
    #LIVROS
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

    def adicionar_usuario(self, usuario: Usuario) -> None:
        nome = (usuario.nome).lower()
        sobrenome = (usuario.sobrenome).lower()
        email = (usuario.email).lower()
        telefone = usuario.telefone

        conexao = conectar()
        cur = conexao.cursor()
        try:
            cur.execute("""INSERT INTO usuarios (nome, sobrenome, email, telefone)
                        VALUES (%s, %s, %s, %s)
            """, (nome, sobrenome, email, telefone))
            conexao.commit()
            cur.close()
        except:
            print('ocorreu um erro na inserção dos dados dos usuários')
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

    #UPDATE DEPOIS EU FAÇO
    # def alterar_dados(self, usuario: Usuario|None = None, livro: Livros|None = None, query: str|None = None):
    #     conexao = conectar()
    #     cur = conexao.cursor()
    #     try:
    #         cur.execute(query)
    #         print('a alteração foi executada!')
    #     except Exception as error:
    #         print(error)
    #     finally:
    #         conexao.close()

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
    
    # def listar_livros_disponiveis(self) -> list:
    #     disponiveis = [livro for livro in self.catalogo.values() if livro.disponivel]
    #     if disponiveis:
    #         print('Livros disponíveis na biblioteca:')
    #         for livro in disponiveis:
    #             print(livro)
    #     else:
    #         print('Não há livros disponíveis.')
    #     return disponiveis

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
    
    # def devolver_livro(self, livro_id: str, usuario):
    #     livro = self.catalogo.get(livro_id)
    #     if not livro:
    #         print('Este livro não está no catálogo!')
    #         return
    #     if livro.disponivel:
    #         print('Este livro já está disponível! Não há o que devolver')
    #         return
    #     usuario.livros_emprestados.remove(livro)
    #     print(f'O livro {livro.titulo} foi devolvido por {usuario.nome}!')

    def listar_usuarios(self):
        print(self.usuarios_registrados)

    # def excluir_usuario(self, nome_usuario: str):
    #     if nome_usuario not in self.usuarios_registrados:
    #         print('Este usuário não é desta biblioteca!')
    #         return
    #     self.usuarios_registrados.remove(nome_usuario)


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
