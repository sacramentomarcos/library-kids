from classes import Biblioteca, Livros, Usuario
import re
import pytest

class TestLivros:
    def test_atributos_livros(self):
        test_livro = Livros('titulozasso', 'autorzasso', 2002)
        regex = r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$'
        uuid_regex = re.compile(regex, re.I)
        assert uuid_regex.match(test_livro.id), 'O uuid não corresponde com o padrão!'

class TestBiblioteca:
    def test_adicionar_livro(self):
        lib = Biblioteca()
        livro = Livros('titulozasso', 'autorzasso', 2002)
        livro_id = livro.id
        lib.adicionar_livro(livro)
        assert lib.catalogo[livro_id] == livro, 'O livro não está adicionado ao dicionário!'
        assert type(livro) == Livros
    
    def test_remover_livro(self):
        lib = Biblioteca()
        livro = Livros('titulozasso', 'autorzasso', 2002)
        lib.adicionar_livro(livro)
        lib.remover_livro(livro)
        assert lib.catalogo.get(livro.id, -1) == -1, 'O livro ainda está no catálogo!'

    def test_listar_livros_disponiveis(self):
        lib = Biblioteca()
        livro = Livros('titulozasso', 'autorzasso', 2002)
        lib.adicionar_livro(livro)
        lista = lib.listar_livros_disponiveis()
        assert lista == [livro]

    def test_emprestar_livro(self):
        pass