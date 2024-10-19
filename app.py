import psycopg2
from classes import Biblioteca, Livros, Usuario, conectar



def correcao():
    conexao = conectar()
    cur = conexao.cursor()
    for i in requisicao:
        cur.execute(i)
    conexao.commit()
    cur.close()
    conexao.close()

def main():
    usuario = Usuario('Marcos', 'SacrAmENtinho', 'sacramento.marcooooos', 31990622247)
    lib = Biblioteca()
    lib.adicionar_usuario(usuario)
    

if __name__ == "__main__":
    main()
