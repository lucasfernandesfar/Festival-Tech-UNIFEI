from collections import deque
import ingressos
# O estado do sistema é encapsulado em um único dicionário, que é
# passado e retornado por todas as funções.
ESTADO_INICIAL = {
    'fila_padrao': deque(),
    'fila_vip': deque(),
    'fila_inteira': deque(),
    'fila_meia': deque(),
    'modo_atendimento': 'PADRAO',  # PADRAO ou PRIORIDADE
    'proximo_id': 1,
    'contador_atendido': 0,
    'atendidos': [],
    'relogio_logico': 0,  # Simula o tempo em "minutos"
    'tempo_total_espera': 0,
}

def comprar(estado, nome, categoria):
    """
    COMPRAR <nome> <categoria>
    Cria ingresso com id sequencial e enfileira.
    Categorias válidas: INTEIRA, MEIA, VIP.
    """
    categoria = categoria.upper()

    # ✅ Verificação antes de criar o ingresso
    if categoria not in ['INTEIRA', 'MEIA', 'VIP']:
        print(f"ERRO: Categoria '{categoria}' inválida. Use INTEIRA, MEIA ou VIP.")
        return estado

    novo_ingresso = {
        'id': estado['proximo_id'],
        'nome': nome,
        'categoria': categoria,
        'chegada_logica': estado['relogio_logico']  # Tempo de chegada simulado
    }

    # Enfileirar de acordo com o modo
    if estado['modo_atendimento'] == 'PADRAO':
        estado['fila_padrao'].append(novo_ingresso)
    elif estado['modo_atendimento'] == 'PRIORIDADE':
        if categoria == 'VIP':
            estado['fila_vip'].append(novo_ingresso)
        elif categoria == 'INTEIRA':
            estado['fila_inteira'].append(novo_ingresso)
        elif categoria == 'MEIA':
            estado['fila_meia'].append(novo_ingresso)

    print(f"Ingresso '{novo_ingresso['id']}' ({nome} - {categoria}) comprado e adicionado à fila.")
    estado['proximo_id'] += 1
    return estado
def _proximo_a_entrar(estado):
    """Função auxiliar para determinar quem deve sair da fila."""
    if estado['modo_atendimento'] == 'PADRAO':
        return estado['fila_padrao'] if estado['fila_padrao'] else None

    # MODO PRIORIDADE
    if estado['fila_vip']:
        return estado['fila_vip']
    elif estado['fila_inteira']:
        return estado['fila_inteira']
    elif estado['fila_meia']:
        return estado['fila_meia']
    return None

def entrar(estado):
    """
    ENTRAR
    Atende o próximo visitante (retira da fila, atualiza tempo e exibe dados).
    """
    fila_a_atender = _proximo_a_entrar(estado)

    if fila_a_atender:
        ingresso_atendido = fila_a_atender.popleft()
        
        # O relógio avança 1 minuto a cada atendimento
        estado['relogio_logico'] += 1
        
        tempo_espera = estado['relogio_logico'] - ingresso_atendido['chegada_logica']
        estado['tempo_total_espera'] += tempo_espera
        estado['contador_atendido'] += 1
        
        # Adiciona dados de atendimento para ESTATISTICAS
        ingresso_atendido['tempo_espera'] = tempo_espera
        estado['atendidos'].append(ingresso_atendido)

        print(f"--- ATENDIDO: Ingresso {ingresso_atendido['id']} ---")
        print(f"Nome: {ingresso_atendido['nome']}")
        print(f"Categoria: {ingresso_atendido['categoria']}")
        print(f"Tempo de Espera: {tempo_espera} min. (Chegada: {ingresso_atendido['chegada_logica']} | Atendimento: {estado['relogio_logico']})")
        return estado
    
    print("Fila vazia. Nenhum visitante para atender.")
    return estado

def espiar(estado):
    """
    ESPIAR
    Mostra quem é o próximo sem retirar da fila.
    """
    fila_a_espiar = _proximo_a_entrar(estado)
    
    if fila_a_espiar:
        proximo = fila_a_espiar[0]
        print(f"PRÓXIMO: Ingresso {proximo['id']} ({proximo['nome']} - {proximo['categoria']})")
    else:
        print("Fila vazia.")
        
    return estado

def _remover_por_id(fila, id_cancelar):
    """Função auxiliar para remover um ingresso por ID de um deque."""
    lista_temporaria = []
    encontrado = None
    
    # Move os itens para uma lista temporária, procurando o ID
    while fila:
        item = fila.popleft()
        if item['id'] == id_cancelar:
            encontrado = item
        else:
            lista_temporaria.append(item)
            
    # Devolve os itens não cancelados para o deque
    fila.extend(lista_temporaria)
    return encontrado

def cancelar(estado, id_cancelar):
    """
    CANCELAR <id>
    Cancela um ingresso ainda não atendido.
    """
    #  Tratamento de erro para entrada inválida
    try:
        id_cancelar = int(id_cancelar)  # Garante que é um número
    except ValueError:
        print(f"ERRO: ID '{id_cancelar}' inválido. Use um número inteiro (ex: CANCELAR 3).")
        return estado

    if estado['modo_atendimento'] == 'PADRAO':
        cancelado = _remover_por_id(estado['fila_padrao'], id_cancelar)
    else:
        # Tenta em todas as filas de prioridade
        cancelado = _remover_por_id(estado['fila_vip'], id_cancelar)
        if not cancelado:
            cancelado = _remover_por_id(estado['fila_inteira'], id_cancelar)
        if not cancelado:
            cancelado = _remover_por_id(estado['fila_meia'], id_cancelar)

    if cancelado:
        print(f"CANCELADO: Ingresso {id_cancelar} ({cancelado['nome']} - {cancelado['categoria']}) removido da fila.")
    else:
        print(f"ERRO: Ingresso {id_cancelar} não encontrado ou já foi atendido.")

    return estado

def listar(estado):
    """
    LISTAR
    Lista os pendentes na ordem de atendimento.
    """
    print(f"\n--- FILA DE ATENDIMENTO ({estado['modo_atendimento']}) ---")
    
    def _mostrar_fila(nome_fila, fila):
        if fila:
            print(f"  > {nome_fila} ({len(fila)} pendentes):")
            for i, ing in enumerate(fila, 1):
                print(f"    {i}. ID {ing['id']} ({ing['nome']} - {ing['categoria']})")
        else:
            print(f"  > {nome_fila}: Vazia.")

    if estado['modo_atendimento'] == 'PADRAO':
        _mostrar_fila("FILA PADRÃO", estado['fila_padrao'])
    else:
        _mostrar_fila("VIP", estado['fila_vip'])
        _mostrar_fila("INTEIRA", estado['fila_inteira'])
        _mostrar_fila("MEIA", estado['fila_meia'])

    print("-------------------------------------------------")
    return estado

def estatisticas(estado):
    estat = ingressos.atualizar_estatisticas(estado)
    ingressos.exibir_estatisticas(estat, estado["relogio_logico"])
    return estado

def modo(estado, novo_modo):
    """
    MODO PADRAO|PRIORIDADE
    Alterna o tipo de atendimento.
    """
    novo_modo = novo_modo.upper()
    
    if novo_modo not in ['PADRAO', 'PRIORIDADE']:
        print(f"ERRO: Modo '{novo_modo}' inválido. Use PADRAO ou PRIORIDADE.")
        return estado
        
    if novo_modo == estado['modo_atendimento']:
        print(f"O modo de atendimento já é '{novo_modo}'.")
        return estado

    # Lógica de Transição (movimentação dos ingressos)
    if novo_modo == 'PADRAO':
        # Transfere tudo para a fila_padrao, mantendo a ordem (VIP > INTEIRA > MEIA > PADRAO)
        # Se for PADRAO -> PRIORIDADE, a fila_padrao já estará vazia, mas por segurança.
        ingressos_a_mover = []
        ingressos_a_mover.extend(list(estado['fila_vip']))
        ingressos_a_mover.extend(list(estado['fila_inteira']))
        ingressos_a_mover.extend(list(estado['fila_meia']))
        ingressos_a_mover.extend(list(estado['fila_padrao'])) # Pega o que estava lá

        estado['fila_padrao'] = deque(ingressos_a_mover)
        estado['fila_vip'].clear()
        estado['fila_inteira'].clear()
        estado['fila_meia'].clear()
        
    elif novo_modo == 'PRIORIDADE':
        # Transfere da fila_padrao para as filas de prioridade
        while estado['fila_padrao']:
            ingresso = estado['fila_padrao'].popleft()
            cat = ingresso['categoria']
            if cat == 'VIP':
                estado['fila_vip'].append(ingresso)
            elif cat == 'INTEIRA':
                estado['fila_inteira'].append(ingresso)
            elif cat == 'MEIA':
                estado['fila_meia'].append(ingresso)

    estado['modo_atendimento'] = novo_modo
    print(f"Modo de atendimento alterado para: {novo_modo}")
    return estado