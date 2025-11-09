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
                               INSERT INTO estabelecimentos (nome, cnpj, endereco)
                               values (%s, %s) RETURNING id_estabelecimento;""",
                               (estabelecimento.nome, estabelecimento.cnpj, estabelecimento.endereco)
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
                                (cliente.cpf, cliente.endereco, cliente.sexo, cliente.nome)
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

    def buscar_perguntas(self, alvo_avaliacao):
        """ Retorna uma lista de objetos Pergunta """
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                SELECT id_questao, enunciado_questao, tipo_resposta, alvo_avaliacao
                                FROM questoes WHERE alvo_avaliacao = (%s)
                                """, (alvo_avaliacao,)
                    )
                    perguntas = cur.fetchall()
                    lista_perguntas = []
                    for pergunta in perguntas:
                        instancia = Pergunta(pergunta[0], pergunta[1], pergunta[2], pergunta[3])
                        lista_perguntas.append(instancia)

                except Exception as e:
                    print(e)
                    return None

        return lista_perguntas

    def buscar_pedidos_para_avaliar(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                SELECT p.id_pedido, p.data_hora, p.status,
                                    e.id_estabelecimento, e.cnpj, e.nome AS nome_estabelecimento, e.endereco AS endereco_estabelecimento,
                                    en.id_entregador, en.nome AS nome_entregador, en.cpf AS cpf_entregador,
                                    c.id_cliente, c.cpf AS cliente_cpf, c.endereco AS cliente_endereco, c.sexo, c.nome AS cliente_nome
                                FROM pedidos p 
                                JOIN estabelecimentos e ON p.id_estabelecimento = e.id_estabelecimento
                                JOIN clientes c ON p.id_cliente = c.id_cliente
                                JOIN entregadores en ON p.id_entregador = en.id_entregador
                                WHERE p.status = 'Concluído'
                                """)
                    query = cur.fetchall()
                    lista_pedidos = []
                    for resultado in query:
                        estabelecimento_obj = Estabelecimento(
                            id=resultado[3], cnpj=resultado[4], nome=resultado[5], endereco=resultado[6]
                        )
                        entregador_obj = Entregador(
                            id=resultado[7], nome=resultado[8], cpf=resultado[9]
                        )
                        cliente_obj = Cliente(
                            id=resultado[10], cpf=resultado[11], endereco=resultado[12], sexo=resultado[13], nome=resultado[14]
                        )
                        pedido_obj = Pedido(
                            id=resultado[0],
                            estabelecimento_obj=estabelecimento_obj,
                            entregador_obj=entregador_obj,
                            cliente_obj=cliente_obj,
                            data_hora=resultado[1],
                            status=resultado[2]
                        )
                        lista_pedidos.append(pedido_obj)
                except Exception as e:
                    print(e)
                    return None

        return lista_pedidos

    def buscar_pedido_por_id(self, id_pedido):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                    SELECT p.id_pedido, p.data_hora, p.status,
                                        e.id_estabelecimento, e.cnpj, e.nome AS estabelecimento_nome, e.endereco AS endereco_estabelecimento,
                                        en.id_entregador, en.nome AS nome_entregador, en.cpf AS cpf_entregador,
                                        c.id_cliente, c.cpf AS cliente_cpf, c.endereco AS cliente_endereco, c.sexo, c.nome AS cliente_nome
                                    FROM pedidos p
                                    JOIN estabelecimentos e ON p.id_estabelecimento = e.id_estabelecimento
                                    JOIN entregadores en ON p.id_entregador = en.id_entregador
                                    JOIN clientes c ON p.id_cliente = c.id_cliente
                                    WHERE p.id_pedido = (%s)
                    """, (id_pedido,)
                    )

                    resultado = cur.fetchone()
                    if not resultado:
                        print(f"Nenhum pedido encontrado com {id_pedido}")
                        return None

                    estabelecimento_obj = Estabelecimento(
                        id=resultado[3], cnpj=resultado[4], nome=resultado[5], endereco=resultado[6]
                    )

                    entregador_obj = Entregador(
                        id=resultado[7], nome=resultado[8], cpf=resultado[9]
                    )

                    cliente_obj = Cliente(
                        id=resultado[10], cpf=resultado[11], endereco=resultado[12], sexo=resultado[13], nome=resultado[14]
                    )

                    pedido_obj = Pedido(
                        id=resultado[0], data_hora=resultado[1], status=resultado[2],
                        estabelecimento_obj=estabelecimento_obj,
                        entregador_obj=entregador_obj,
                        cliente_obj=cliente_obj
                    )
                except Exception as e:
                    print(e)
                    return None

        return pedido_obj

    def buscar_pergunta_por_id(self, id_pergunta):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                    SELECT id_questao, enunciado_questao, tipo_resposta, alvo_avaliacao 
                                    FROM questoes WHERE id_questao = (%s)
                                """,(id_pergunta,)
                    )

                    resultado = cur.fetchone()
                    if not resultado:
                        print(f"Nenhuma pergunta encontrada com id {id_pergunta}.")
                        return None

                    pergunta_obj = Pergunta(
                        id=resultado[0], enunciado_pergunta=resultado[1],
                        tipo_resposta=resultado[2], alvo_avaliacao=resultado[3]
                    )

                except Exception as e:
                    print(e)
                    return None

        return pergunta_obj
