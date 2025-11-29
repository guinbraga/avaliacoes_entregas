# para cada estabelecimento:
    # devemos puxar todos os pedidos com status 'Concluído'
    # definir viés:
        # estabelecimentos melhor avaliados: ids no range(300, 310), 310 excluso;
                                            # ids no range(374,383)
                                            # ids no range (424,429)
        # estabelecimentos pior avaliados: ids no range (237,247)
                                            # ids no range(310,318)
                                            # ids no range(383,389)
        # itens_pedido melhor avaliados: X-Salada, Margherita, Mocca
        # itens_pedido pior avaliados: X-Tudo, 4 Queijos, Latte


    # para cada pedido, devemos:
        # selecionar uma pergunta aleatoria sobre o entregador,
        # selecionar uma pergunta aleatoria sobre o estabelecimento,
        # para cada item do pedido, selecionar uma pergunta aleatoria sobre ele,
        # selecionar uma pergunta aleatoria sobre o aplicativo
        # para cada pergunta aleatoria devemos:
            # se ela for de sim/nao, escolher aleatoriamente entre sim ou nao
            # se ela for de 1 a 5, escolher aleatoriamente entre 1, 2, 3, 4, 5
            # salvar as respostas
        # salvar a avaliacao
        # mudar o status do pedido para 'Avaliado'