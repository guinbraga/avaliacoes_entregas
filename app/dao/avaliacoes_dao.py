from .base import get_db_connection


class AvaliacoesDAO:
    def inserir_avaliacao(self, avaliacao):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO avaliacoes (data_hora, id_pedido)
                                VALUES (%s, %s)
                                RETURNING id_avaliacao;
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
                                INSERT INTO respostas (id_avaliacao, id_pergunta, id_item_pedido, valor_resposta)
                                VALUES (%s, %s, %s, %s) RETURNING id_resposta;
                                """,
                                (resposta.avaliacao.id, resposta.pergunta.id, resposta.item_pedido.id, resposta.valor_resposta)
                    )
                    id_resposta = cur.fetchone()[0]
                    resposta.id = id_resposta
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def salvar_avaliacao_atomica(self, avaliacao, respostas):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:

                    if not respostas:
                        raise ValueError("Avaliação não pode ser salva sem respostas!")

                    cur.execute("""
                                INSERT INTO avaliacoes (data_hora, id_pedido)
                                VALUES (%s, %s) RETURNING id_avaliacao;
                                """,
                                (avaliacao.data_hora, avaliacao.pedido.id)
                    )
                    id_avaliacao = cur.fetchone()[0]
                    avaliacao.id = id_avaliacao

                    for resposta in respostas:
                        id_item_pedido = resposta.item_pedido.id if resposta.item_pedido else None

                        try:
                            cur.execute("""
                                        INSERT INTO respostas (id_avaliacao, id_pergunta, id_item_pedido, valor_resposta)
                                        VALUES (%s, %s, %s, %s) RETURNING id_resposta;
                                        """,
                                        (avaliacao.id, resposta.pergunta.id, id_item_pedido,
                                         resposta.valor_resposta)
                                        )
                            id_resposta = cur.fetchone()[0]
                            resposta.id = id_resposta

                        except Exception as e:
                            print(e)
                            conn.rollback()
                            raise e

                    try:
                        cur.execute(
                        """
                        UPDATE pedidos
                        SET status = 'Avaliado'
                        WHERE id_pedido = %s
                                    """, (avaliacao.pedido.id,))

                        conn.commit()

                    except Exception as e:
                        print(e)
                        conn.rollback()
                        raise e

                except Exception as e:
                    print(e)
                    conn.rollback()
                    raise e