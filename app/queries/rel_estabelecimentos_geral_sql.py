TOP_5_NOTA_EST_CAT = """SELECT AVG(r.valor_resposta :: integer) AS media_nota, e.nome
FROM estabelecimentos e 
JOIN pedidos p ON e.id_estabelecimento = p.id_estabelecimento
JOIN avaliacoes a ON p.id_pedido = a.id_pedido
JOIN respostas r ON r.id_avaliacao = a.id_avaliacao
JOIN perguntas prg ON prg.id_pergunta = r.id_pergunta
JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
JOIN categorias c ON c.id_categoria = ce.id_categoria
WHERE prg.enunciado_pergunta = (%s)
AND c.categoria = (%s)
GROUP BY e.id_estabelecimento
ORDER BY media_nota DESC
LIMIT 5;"""

PIOR_5_NOTA_EST_CAT = """SELECT AVG(r.valor_resposta :: integer) AS media_nota, e.nome
FROM estabelecimentos e 
JOIN pedidos p ON e.id_estabelecimento = p.id_estabelecimento
JOIN avaliacoes a ON p.id_pedido = a.id_pedido
JOIN respostas r ON r.id_avaliacao = a.id_avaliacao
JOIN perguntas prg ON prg.id_pergunta = r.id_pergunta
JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
JOIN categorias c ON c.id_categoria = ce.id_categoria
WHERE prg.enunciado_pergunta = (%s)
AND c.categoria = (%s)
GROUP BY e.id_estabelecimento
ORDER BY media_nota
LIMIT 5;"""

TOP_5_PROP_EST_CAT = """SELECT AVG(CASE WHEN r.valor_resposta = 'sim' THEN 1.0 ELSE 0.0 END) AS prop_sim, e.nome
FROM estabelecimentos e 
JOIN pedidos p ON e.id_estabelecimento = p.id_estabelecimento
JOIN avaliacoes a ON p.id_pedido = a.id_pedido
JOIN respostas r ON r.id_avaliacao = a.id_avaliacao
JOIN perguntas prg ON prg.id_pergunta = r.id_pergunta
JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
JOIN categorias c ON c.id_categoria = ce.id_categoria
WHERE prg.enunciado_pergunta = (%s)
AND c.categoria = (%s)
GROUP BY e.id_estabelecimento
ORDER BY prop_sim DESC
LIMIT 5;"""

PIOR_5_PROP_EST_CAT = """SELECT AVG(CASE WHEN r.valor_resposta = 'sim' THEN 1.0 ELSE 0.0 END) AS prop_sim, e.nome
FROM estabelecimentos e 
JOIN pedidos p ON e.id_estabelecimento = p.id_estabelecimento
JOIN avaliacoes a ON p.id_pedido = a.id_pedido
JOIN respostas r ON r.id_avaliacao = a.id_avaliacao
JOIN perguntas prg ON prg.id_pergunta = r.id_pergunta
JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
JOIN categorias c ON c.id_categoria = ce.id_categoria
WHERE prg.enunciado_pergunta = (%s)
AND c.categoria = (%s)
GROUP BY e.id_estabelecimento
ORDER BY prop_sim
LIMIT 5;"""


# SEM DETERMINAR CATEGORIA:

TOP_5_NOTA_EST_GERAL = """SELECT AVG(r.valor_resposta :: integer) AS media_nota, 
                                 e.nome,
                                 STRING_AGG(DISTINCT c.categoria, ', '),
                                 e.id_estabelecimento 
FROM estabelecimentos e 
JOIN pedidos p ON e.id_estabelecimento = p.id_estabelecimento
JOIN avaliacoes a ON p.id_pedido = a.id_pedido
JOIN respostas r ON r.id_avaliacao = a.id_avaliacao
JOIN perguntas prg ON prg.id_pergunta = r.id_pergunta
JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
JOIN categorias c ON c.id_categoria = ce.id_categoria
WHERE prg.enunciado_pergunta = (%s)
GROUP BY e.id_estabelecimento
ORDER BY media_nota DESC
LIMIT 5;"""

PIOR_5_NOTA_EST_GERAL = """SELECT AVG(r.valor_resposta :: integer) AS media_nota, 
                                  e.nome,
                                  STRING_AGG(DISTINCT c.categoria, ', '),
                                  e.id_estabelecimento 
FROM estabelecimentos e 
JOIN pedidos p ON e.id_estabelecimento = p.id_estabelecimento
JOIN avaliacoes a ON p.id_pedido = a.id_pedido
JOIN respostas r ON r.id_avaliacao = a.id_avaliacao
JOIN perguntas prg ON prg.id_pergunta = r.id_pergunta
JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
JOIN categorias c ON c.id_categoria = ce.id_categoria
WHERE prg.enunciado_pergunta = (%s)
GROUP BY e.id_estabelecimento
ORDER BY media_nota
LIMIT 5;"""

TOP_5_PROP_EST_GERAL = """SELECT AVG(CASE WHEN r.valor_resposta = 'sim' THEN 1.0 ELSE 0.0 END) AS prop_sim, 
                                 e.nome,
                                 STRING_AGG(DISTINCT c.categoria, ', '),
                                 e.id_estabelecimento 
FROM estabelecimentos e 
JOIN pedidos p ON e.id_estabelecimento = p.id_estabelecimento
JOIN avaliacoes a ON p.id_pedido = a.id_pedido
JOIN respostas r ON r.id_avaliacao = a.id_avaliacao
JOIN perguntas prg ON prg.id_pergunta = r.id_pergunta
JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
JOIN categorias c ON c.id_categoria = ce.id_categoria
WHERE prg.enunciado_pergunta = (%s)
GROUP BY e.id_estabelecimento
ORDER BY prop_sim DESC
LIMIT 5;"""

PIOR_5_PROP_EST_GERAL = """SELECT AVG(CASE WHEN r.valor_resposta = 'sim' THEN 1.0 ELSE 0.0 END) AS prop_sim, 
                                  e.nome, 
                                  STRING_AGG(DISTINCT c.categoria, ', '),
                                  e.id_estabelecimento 
FROM estabelecimentos e 
JOIN pedidos p ON e.id_estabelecimento = p.id_estabelecimento
JOIN avaliacoes a ON p.id_pedido = a.id_pedido
JOIN respostas r ON r.id_avaliacao = a.id_avaliacao
JOIN perguntas prg ON prg.id_pergunta = r.id_pergunta
JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
JOIN categorias c ON c.id_categoria = ce.id_categoria
WHERE prg.enunciado_pergunta = (%s)
GROUP BY e.id_estabelecimento
ORDER BY prop_sim
LIMIT 5;"""

EST_NOTA_ACIMA = """
SELECT COUNT(*) FROM
	(SELECT e.nome, AVG(r.valor_resposta :: integer) as nota_media
	FROM estabelecimentos e
	JOIN pedidos p ON e.id_estabelecimento = p.id_estabelecimento
	JOIN avaliacoes a ON a.id_pedido = p.id_pedido
	JOIN respostas r ON r.id_avaliacao = a.id_avaliacao
	JOIN perguntas prg ON r.id_pergunta = prg.id_pergunta
	WHERE prg.enunciado_pergunta = 'Qual nota você dá para o estabelecimento?'
	GROUP BY e.id_estabelecimento)
WHERE nota_media > (%s)
"""

MELHOR_ITEM = """
SELECT i.nome, e.nome, AVG(r.valor_resposta :: integer) AS nota_media
FROM itens i
JOIN estabelecimentos e ON i.id_estabelecimento = e.id_estabelecimento
JOIN itens_pedido ip ON i.id_item = ip.id_item
JOIN respostas r ON r.id_item_pedido = ip.id_item_pedido
JOIN perguntas p ON p.id_pergunta = r.id_pergunta
WHERE p.enunciado_pergunta = 'O quão gostoso estava esse item?'
GROUP BY i.nome, e.nome
ORDER BY nota_media DESC
LIMIT 1
"""