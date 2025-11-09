import psycopg
import sys
from models import (
    Cliente, Entregador, Estabelecimento, Classe_produto, Item,
    Pedido, Item_pedido, Categoria, Categoria_estabelecimento,
    Pergunta, Avaliacao, Resposta
)

DB_URL = "postgresql://postgres:Guilhormo%40123@localhost/imeals"

def get_db_connection():
    """ Cria e retorna uma nova conexão com o banco de dados """
    try:
        connection = psycopg.connect(DB_URL)
        return connection
    except Exception as e:
        print(f"Erro: não foi possível conectar ao banco de dados: {e}")

class DBManager:
    def __init__(self):
        pass

    def inserir_estabelecimento(self, estabelecimento):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
               try:
                   cur.execute("""
                               INSERT INTO estabelecimentos (nome, cnpj)
                               values (%s, %s) RETURNING id_estabelecimento;""",
                               (estabelecimento.nome, estabelecimento.cnpj)
                               )
                   id_estabelecimento = cur.fetchone()[0]
                   estabelecimento.id = id_estabelecimento
                   conn.commit()
               except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_categoria_estabelecimento(self, categoria_estabelecimento):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
               try:
                   cur.execute("""INSERT INTO categorias_estabelecimento (id_estabelecimento, id_categoria)
                                  VALUES (%s, %s);""",
                                  (categoria_estabelecimento.estabelecimento.id, categoria_estabelecimento.categoria.id)
                               )
                   conn.commit()
               except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_cliente(self, cliente):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO clientes (cpf, endereco, sexo, nome)
                                VALUES (%s, %s, %s, %s) RETURNING id_cliente;
                                """,
                                (cliente.cpf, cliente.endereco, cliente.genero, cliente.nome)
                    )
                    id_cliente = cur.fetchone()[0]
                    cliente.id = id_cliente
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_entregador(self, entregador):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO entregadores (nome, cpf)
                                VALUES (%s, %s) RETURNING id_entregador;
                                """,
                                (entregador.nome, entregador.cpf)
                    )
                    id_entregador = cur.fetchone()[0]
                    entregador.id = id_entregador
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_categoria(self, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""INSERT INTO categorias (categoria) VALUES (%s)
                                   RETURNING id_categoria;
                                """, (categoria.categoria,)
                    )
                    id_categoria = cur.fetchone()[0]
                    categoria.id = id_categoria
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_classificacao(self, classe_produto):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if classe_produto.classificacao_pai:
                        cur.execute("SELECT 1 FROM classificacoes WHERE tipo_produto = %s", (classe_produto.classificacao_pai,))
                        busca = cur.fetchone()
                        if not busca:
                            raise ValueError(f"Erro: A classificação pai '{classe_produto.classificacao_pai}' não existe.")
                    cur.execute("""
                                INSERT INTO classificacoes (tipo_produto, classificacao_pai)
                                VALUES (%s, %s)
                                ;""", (classe_produto.tipo_produto, classe_produto.classificacao_pai)
                    )
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_item(self, item):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""INSERT INTO itens (nome, valor_base, classificacao, id_estabelecimento)
                                    VALUES (%s, %s, %s, %s) RETURNING id_item;""",
                                    (item.nome, item.valor_base, item.classe_produto.tipo_produto, item.estabelecimento.id)
                    )
                    id_item = cur.fetchone()[0]
                    item.id = id_item
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_pedido(self, pedido):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO pedidos (id_estabelecimento, id_cliente, data_hora, status, id_entregador)
                                VALUES (%s, %s, %s, %s, %s) RETURNING id_pedido;
                                """,
                                (pedido.estabelecimento.id, pedido.cliente.id, pedido.data_hora, pedido.status, pedido.entregador.id)
                    )
                    id_pedido = cur.fetchone()[0]
                    pedido.id = id_pedido
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_item_pedido(self, item_pedido):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO itens_pedido (id_pedido, id_item, quantidade, preco_unidade)
                                VALUES (%s, %s, %s, %s) RETURNING id_item_pedido;
                                """,
                                (item_pedido.pedido.id, item_pedido.item.id, item_pedido.quantidade, item_pedido.preco_unidade)
                    )
                    id_item_pedido = cur.fetchone()[0]
                    item_pedido.id = id_item_pedido
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_pergunta(self, pergunta):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO perguntas (enunciado_pergunta, tipo_resposta, alvo_avaliacao)
                                VALUES (%s, %s, %s) RETURNING id_pergunta;
                                """,
                                (pergunta.enunciado_pergunta, pergunta.tipo_resposta, pergunta.alvo_avaliacao)
                    )
                    id_pergunta = cur.fetchone()[0]
                    pergunta.id = id_pergunta
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_avaliacao(self, avaliacao):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO avaliacoes (data_hora, id_pedido)
                                VALUES (%s, %s) RETURNING id_avaliacao;
                                """,
                                (avaliacao.data_hora, avaliacao.pedido.id)
                    )
                    id_avaliacao = cur.fetchone()[0]
                    avaliacao.id = id_avaliacao
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_resposta(self, resposta):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO respostas (id_avaliacao, id_questao, id_item_pedido, valor_resposta)
                                VALUES (%s, %s, %s, %s) RETURNING id_resposta;
                                """,
                                (resposta.avaliacao.id, resposta.questao.id, resposta.item_pedido.id, resposta.valor_resposta)
                    )
                    id_resposta = cur.fetchone()[0]
                    resposta.id = id_resposta
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()