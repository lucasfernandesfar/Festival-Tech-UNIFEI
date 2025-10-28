# --- Funções Auxiliares de Estado ---

def _salvar_estado(estado_atual):
    """Cria uma cópia profunda *manual* e suficiente do estado atual.
    Sem usar import copy. Lida com: listas, dicionários, e objetos tipo deque (copiados pela sua classe).
    """
    estado_copiado = {}

    for chave, valor in estado_atual.items():
        # Lists -> shallow copy
        if isinstance(valor, list):
            # Se a lista contém dicionários, copie cada dicionário também (cópia rasa de cada dict).
            nova_lista = []
            for item in valor:
                if isinstance(item, dict):
                    nova_lista.append(item.copy())
                else:
                    nova_lista.append(item)
            estado_copiado[chave] = nova_lista

        # Dicts -> shallow copy (as chaves internas no seu estado são simples)
        elif isinstance(valor, dict):
            novo_dict = {}
            for k, v in valor.items():
                # Se v for lista/dict/deque, faça cópia rasa (tratamento limitado)
                if isinstance(v, list):
                    novo_dict[k] = v[:]
                elif isinstance(v, dict):
                    novo_dict[k] = v.copy()
                else:
                    novo_dict[k] = v
            estado_copiado[chave] = novo_dict

        # Objetos tipo deque (ou semelhantes) -> detecta por métodos e recria usando o mesmo tipo
        elif hasattr(valor, 'append') and hasattr(valor, 'popleft'):
            # type(valor)(list(valor)) -> reconstrói deque sem importar collections
            try:
                estado_copiado[chave] = type(valor)(list(valor))
            except Exception:
                # fallback: transforma em lista
                estado_copiado[chave] = list(valor)

        # Outros tipos imutáveis (int, str, bool, None) -> atribuição direta
        else:
            estado_copiado[chave] = valor

    return estado_copiado

def _aplicar_comando(estado_atual, historico_undo, historico_redo, comando_funcao, *args):
    """
    Wrapper que executa um comando que altera o estado.
    1. Salva o estado atual em UNDO.
    2. Limpa REDO.
    3. Executa a função do comando.
    4. Retorna o novo estado e os históricos atualizados.
    """
    # 1. Salvar o estado ANTES da alteração
    historico_undo.append(_salvar_estado(estado_atual))

    # 2. Limpar o histórico REDO
    historico_redo.clear()
    
    # 3. Executar o comando (a função deve retornar o novo estado)
    novo_estado = comando_funcao(estado_atual, *args)

    return novo_estado, historico_undo, historico_redo

def desfazer(estado_atual, historico_undo, historico_redo):
    """
    DESFAZER - desfaz a última ação.
    Move o estado atual para HISTORICO_REDO e restaura o estado do HISTORICO_UNDO.
    """
    if not historico_undo:
        print("ERRO DESFAZER: Histórico UNDO vazio. Nada a desfazer.")
        return estado_atual, historico_undo, historico_redo

    # Move o estado atual para o REDO
    historico_redo.append(_salvar_estado(estado_atual))

    # Restaura o estado anterior (cópia independente)
    estado_restaurado = _salvar_estado(historico_undo.pop())

    print("INFO DESFAZER: Ação desfeita com sucesso.")
    return estado_restaurado, historico_undo, historico_redo


def refazer(estado_atual, historico_undo, historico_redo):
    """
    REFAZER - refaz a última ação desfeita.
    Move o estado atual para HISTORICO_UNDO e restaura o estado do HISTORICO_REDO.
    """
    if not historico_redo:
        print("ERRO REFAZER: Histórico REDO vazio. Nada a refazer.")
        return estado_atual, historico_undo, historico_redo
    
    # O estado ATUAL se torna o anterior para UNDO
    historico_undo.append(_salvar_estado(estado_atual))
    
    # Restaura o estado refeito do REDO
    estado_restaurado = _salvar_estado(historico_redo.pop())
    
    print("INFO REFAZER: Ação refeita com sucesso.")
    return estado_restaurado, historico_undo, historico_redo

def comando_ir(estado_antigo, caminho):
    """Implementa IR <caminho>. Retorna o novo estado."""
    
    estado = _salvar_estado(estado_antigo) # Trabalha numa cópia
    local_atual = estado['local_atual']
    voltar_pilha = estado['voltar_pilha']
    avancar_pilha = estado['avancar_pilha']

    if not isinstance(caminho, str) or not caminho:
        print("ERRO IR: O caminho deve ser uma string não vazia.")
        return estado_antigo

    # (Lógica IR simplificada, para o foco ser UNDO/REDO)
    if caminho.startswith('/'):
        novo_local = caminho.rstrip('/') if caminho != '/' else '/'
    else:
        # Lógica de caminho relativo: apensar se não for a raiz
        if local_atual == "/":
            novo_local = "/" + caminho
        else:
            novo_local = local_atual + "/" + caminho

    if local_atual != novo_local:
        voltar_pilha.append(local_atual)
        avancar_pilha.clear()
        estado['local_atual'] = novo_local
        print(f"INFO IR: Navegando para '{novo_local}'.")
        return estado
    else:
        print(f"INFO IR: Já está em '{local_atual}'.")
        return estado_antigo # Retorna o estado antigo se não houver mudança


def comando_voltar(estado_antigo):
    """Implementa VOLTAR. Retorna o novo estado."""
    estado = _salvar_estado(estado_antigo)
    local_atual = estado['local_atual']
    voltar_pilha = estado['voltar_pilha']
    avancar_pilha = estado['avancar_pilha']

    if not voltar_pilha:
        print("ERRO VOLTAR: Pilha VOLTAR vazia. Não é possível retornar.")
        return estado_antigo
    
    avancar_pilha.append(local_atual)
    novo_local = voltar_pilha.pop()
    estado['local_atual'] = novo_local
    
    print(f"INFO VOLTAR: Retornando para '{novo_local}'.")
    return estado


def comando_avancar(estado_antigo):
    """Implementa AVANCAR. Retorna o novo estado."""
    estado = _salvar_estado(estado_antigo)
    local_atual = estado['local_atual']
    voltar_pilha = estado['voltar_pilha']
    avancar_pilha = estado['avancar_pilha']

    if not avancar_pilha:
        print("ERRO AVANCAR: Pilha AVANCAR vazia. Não é possível avançar.")
        return estado_antigo

    voltar_pilha.append(local_atual)
    novo_local = avancar_pilha.pop()
    estado['local_atual'] = novo_local
    
    print(f"INFO AVANCAR: Avançando para '{novo_local}'.")
    return estado

def comando_mudar_modo(estado_antigo, novo_modo):
    """Simula um comando de alteração de estado (MODO)."""
    estado = _salvar_estado(estado_antigo)

    if estado['estado_geral_simulado'] == novo_modo:
         print(f"INFO MODO: Já está no modo '{novo_modo}'.")
         return estado_antigo
         
    estado['estado_geral_simulado'] = novo_modo
    print(f"INFO MODO: Alterando modo para '{novo_modo}'.")
    return estado


# --- Funções de Consulta (Não Alteram Estado/Histórico) ---

def onde(estado_atual):
    """ONDE - Consulta."""
    print(f"Local atual: {estado_atual['local_atual']}")
    print(f"Modo atual: {estado_atual['estado_geral_simulado']}")


def estatisticas(estado_atual, historico_undo, historico_redo):
    """ESTATISTICAS - Consulta (bônus)."""
    print("\n--- ESTATÍSTICAS DO SISTEMA ---")
    print(f"Local: {estado_atual['local_atual']}")
    print(f"Modo: {estado_atual['estado_geral_simulado']}")
    print(f"Histórico VOLTAR: {len(estado_atual['voltar_pilha'])} itens")
    print(f"Histórico AVANCAR: {len(estado_atual['avancar_pilha'])} itens")
    print(f"Histórico DESFAZER (UNDO): {len(historico_undo)} estados salvos")
    print(f"Histórico REFAZER (REDO): {len(historico_redo)} estados salvos")
    print("-------------------------------")


# --- EXEMPLO DE USO ---
"""
# 1. Inicialização do estado e históricos
ESTADO_ATUAL = {
    "local_atual": "/",
    "voltar_pilha": [],
    "avancar_pilha": [],
    "estado_geral_simulado": "Normal",
}
HISTORICO_UNDO = []
HISTORICO_REDO = []

print("--- ESTADO INICIAL ---")
onde(ESTADO_ATUAL)
estatisticas(ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO)

# 2. Comando IR (Altera Estado)
print("\n--- AÇÃO 1: IR para /Palco ---")
ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO = _aplicar_comando(
    ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO, comando_ir, "/Palco"
)
onde(ESTADO_ATUAL)
estatisticas(ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO) # UNDO = 1, REDO = 0

# 3. Comando MODO (Altera Estado)
print("\n--- AÇÃO 2: MODO Vendedor ---")
ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO = _aplicar_comando(
    ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO, comando_mudar_modo, "Vendedor"
)
onde(ESTADO_ATUAL)
estatisticas(ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO) # UNDO = 2, REDO = 0

# 4. Desfazer (Restaura AÇÃO 2)
print("\n--- AÇÃO 3: DESFAZER (Restaura MODO Normal) ---")
ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO = desfazer(
    ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO
)
onde(ESTADO_ATUAL)
estatisticas(ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO) # UNDO = 1, REDO = 1

# 5. Refazer (Restaura AÇÃO 2)
print("\n--- AÇÃO 4: REFAZER (Restaura MODO Vendedor) ---")
ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO = refazer(
    ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO
)
onde(ESTADO_ATUAL)
estatisticas(ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO) # UNDO = 2, REDO = 0

# 6. Nova Ação (Limpa REDO)
print("\n--- AÇÃO 5: IR para Robótica ---")
ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO = _aplicar_comando(
    ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO, comando_ir, "Robótica"
)
onde(ESTADO_ATUAL)
estatisticas(ESTADO_ATUAL, HISTORICO_UNDO, HISTORICO_REDO) # UNDO = 3, REDO = 0
"""