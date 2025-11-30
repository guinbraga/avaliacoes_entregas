from app.dao.base import get_db_connection
from app.queries.rel_estabelecimentos_geral_sql import TOP_5_NOTA_EST_GERAL, PIOR_5_NOTA_EST_GERAL, \
    TOP_5_PROP_EST_GERAL, PIOR_5_PROP_EST_GERAL, TOP_5_NOTA_EST_CAT, PIOR_5_NOTA_EST_CAT, PIOR_5_PROP_EST_CAT, \
    TOP_5_PROP_EST_CAT, EST_NOTA_ACIMA, MELHOR_ITEM, EST_NOTA_ACIMA_CAT, MELHOR_ITEM_CAT, TOTAL_EST_CAT, TOTAL_EST


class RelEstabelecimentosDao():
    def top_5_nota_1_5(self, enunciado_pergunta, categoria=None):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if categoria:
                        cur.execute(TOP_5_NOTA_EST_CAT, (enunciado_pergunta, categoria))
                        return cur.fetchall()
                    else:
                        cur.execute(TOP_5_NOTA_EST_GERAL, (enunciado_pergunta,))
                        return cur.fetchall()
                except Exception as e:
                    print(e)

    def pior_5_nota_1_5(self, enunciado_pergunta, categoria=None):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if categoria:
                        cur.execute(PIOR_5_NOTA_EST_CAT, (enunciado_pergunta, categoria))
                        return cur.fetchall()
                    else:
                        cur.execute(PIOR_5_NOTA_EST_GERAL, (enunciado_pergunta,))
                        return cur.fetchall()
                except Exception as e:
                    print(e)

    def top_5_prop_sim_nao(self, enunciado_pergunta, categoria=None):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if categoria:
                        cur.execute(TOP_5_PROP_EST_CAT, (enunciado_pergunta, categoria))
                        return cur.fetchall()
                    else:
                        cur.execute(TOP_5_PROP_EST_GERAL, (enunciado_pergunta,))
                        return cur.fetchall()
                except Exception as e:
                    print(e)

    def pior_5_prop_sim_nao(self, enunciado_pergunta, categoria=None):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if categoria:
                        cur.execute(PIOR_5_PROP_EST_CAT, (enunciado_pergunta, categoria))
                        return cur.fetchall()
                    else:
                        cur.execute(PIOR_5_PROP_EST_GERAL, (enunciado_pergunta,))
                        return cur.fetchall()
                except Exception as e:
                    print(e)


    def count_est_acima(self, nota, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if categoria:
                        cur.execute(EST_NOTA_ACIMA_CAT, (categoria, nota))
                        return cur.fetchone()[0]
                    else:
                        cur.execute(EST_NOTA_ACIMA, (nota,))
                        return cur.fetchone()[0]
                except Exception as e:
                    print(e)

    def melhor_item(self, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if categoria:
                        cur.execute(MELHOR_ITEM_CAT, (categoria,))
                        return cur.fetchone()
                    else:
                        cur.execute(MELHOR_ITEM)
                        return cur.fetchone()
                except Exception as e:
                    print(e)

    def total_estabelecimentos(self, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if categoria:
                        cur.execute(TOTAL_EST_CAT, (categoria,))
                        return cur.fetchone()[0]
                    else:
                        cur.execute(TOTAL_EST)
                        return cur.fetchone()[0]
                except Exception as e:
                    print(e)