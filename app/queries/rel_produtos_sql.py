TOP_5_NOTA_1_5_PROD = """SELECT e.nome, i.nome, cl.tipo_produto, AVG(r.valor_resposta :: integer) AS media_nota
FROM estabelecimentos e
JOIN pedidos p on p.id_estabelecimento = e.id_estabelecimento
JOIN itens_pedido ip ON ip.id_pedido = p.id_pedido
JOIN avaliacoes a ON a.id_pedido = p.id_pedido
JOIN respostas r ON r.id_avaliacao = a.id_avaliacao AND r.id_item_pedido = ip.id_item_pedido
JOIN perguntas prg ON prg.id_pergunta = r.id_pergunta
JOIN itens i ON i.id_item = ip.id_item
JOIN classificacoes cl on i.classificacao = cl.tipo_produto
WHERE prg.enunciado_pergunta = (%s) AND cl.tipo_produto = (%s)
GROUP BY cl.tipo_produto, e.nome, i.nome
ORDER BY media_nota DESC
LIMIT 5
"""