from app.dao.base import get_db_connection
from app.queries.rel_estabelecimentos_geral_sql import TOP_5_NOTA_EST_GERAL, PIOR_5_NOTA_EST_GERAL, \
    TOP_5_PROP_EST_GERAL, PIOR_5_PROP_EST_GERAL, TOP_5_NOTA_EST_CAT, PIOR_5_NOTA_EST_CAT, PIOR_5_PROP_EST_CAT, \
    TOP_5_PROP_EST_CAT, EST_NOTA_ACIMA, MELHOR_ITEM


class RelEstabelecimentosDao():
    def top_5_nota_1_5(self, enunciado_pergunta, filtro=None):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(TOP_5_NOTA_EST_GERAL, enunciado_pergunta)
                    return cur.fetchall()
                except Exception as e:
                    print(e)

    def pior_5_nota_1_5(self, enunciado_pergunta, filtro=None):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(PIOR_5_NOTA_EST_GERAL, enunciado_pergunta)
                    return cur.fetchall()
                except Exception as e:
                    print(e)

    def top_5_prop_sim_nao(self, enunciado_pergunta):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(TOP_5_PROP_EST_GERAL, enunciado_pergunta)
                    return cur.fetchall()
                except Exception as e:
                    print(e)

    def pior_5_prop_sim_nao(self, enunciado_pergunta):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(PIOR_5_PROP_EST_GERAL, enunciado_pergunta)
                    return cur.fetchall()
                except Exception as e:
                    print(e)

    def top_5_nota_1_5_categoria(self, enunciado_pergunta, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(TOP_5_NOTA_EST_CAT, enunciado_pergunta, categoria)
                    return cur.fetchall()
                except Exception as e:
                    print(e)

    def pior_5_nota_1_5_categoria(self, enunciado_pergunta, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(PIOR_5_NOTA_EST_CAT, enunciado_pergunta, categoria)
                    return cur.fetchall()
                except Exception as e:
                    print(e)

    def top_5_prop_sim_nao_categoria(self, enunciado_pergunta, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(TOP_5_PROP_EST_CAT, enunciado_pergunta, categoria)
                    return cur.fetchall()
                except Exception as e:
                    print(e)

    def pior_5_prop_sim_nao_categoria(self, enunciado_pergunta, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(PIOR_5_PROP_EST_CAT, enunciado_pergunta, categoria)
                    return cur.fetchall()
                except Exception as e:
                    print(e)

    def count_est_acima(self, nota):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(EST_NOTA_ACIMA, nota)
                    return cur.fetchone()[0]
                except Exception as e:
                    print(e)

    def melhor_item(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(MELHOR_ITEM)
                    return cur.fetchone()
                except Exception as e:
                    print(e)