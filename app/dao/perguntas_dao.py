from app.models import Pergunta
from .base import get_db_connection

class PerguntasDAO:
    def inserir_pergunta(self, pergunta):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO perguntas (enunciado_pergunta, tipo_resposta, alvo_avaliacao)
                                VALUES (%s, %s, %s)
                                RETURNING id_pergunta;
                                """,
                                (pergunta.enunciado_pergunta, pergunta.tipo_resposta, pergunta.alvo_avaliacao)
                                )
                    id_pergunta = cur.fetchone()[0]
                    pergunta.id = id_pergunta
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def buscar_perguntas_por_alvo(self, alvo_avaliacao):
        """ Retorna uma lista de objetos Pergunta """
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                SELECT id_pergunta, enunciado_pergunta, tipo_resposta, alvo_avaliacao
                                FROM perguntas WHERE alvo_avaliacao = (%s)
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

    def buscar_pergunta_por_id(self, id_pergunta):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                    SELECT id_pergunta, enunciado_pergunta, tipo_resposta, alvo_avaliacao 
                                    FROM perguntas WHERE id_pergunta = (%s)
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

    def buscar_pergunta_aleatoria_por_alvo(self, alvo_avaliacao):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                    SELECT id_pergunta, enunciado_pergunta, tipo_resposta, alvo_avaliacao
                                    FROM perguntas 
                                    WHERE alvo_avaliacao = (%s)
                                    ORDER BY RANDOM()
                                    LIMIT 1;""", (alvo_avaliacao,))

                    resultado = cur.fetchone()
                    if resultado:
                        pergunta = Pergunta(resultado[0], resultado[1], resultado[2], resultado[3])
                        return pergunta

                    else:
                        print(f"Pergunta não encontrada com alvo: {alvo_avaliacao}")
                        return None

                except Exception as e:
                    print(e)
                    return None