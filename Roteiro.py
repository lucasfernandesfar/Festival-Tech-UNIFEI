# As "pilhas" e o "local atual" (estado) devem ser inicializados
# e mantidos no código que chamará estas funções, por exemplo:
#
# LOCAL_ATUAL = "/"  # Local inicial
# VOLTAR_PILHA = []  # Pilha 'VOLTAR'
# AVANCAR_PILHA = [] # Pilha 'AVANCAR'

# --- Funções de Roteiro do Visitante (Pilhas) ---

def ir_local(caminho, local_atual, voltar_pilha, avancar_pilha):
    """
    IR <caminho>
    Altera o local atual. Empilha o local anterior em VOLTAR e limpa AVANCAR.
    Caminhos absolutos (ex: /IA/Visao) ou relativos (ex: Palco).
    """
    if not isinstance(caminho, str) or not caminho:
        print("ERRO: O caminho deve ser uma string não vazia.")
        return local_atual, voltar_pilha, avancar_pilha

    novo_local = ""

    # 1. Determinar o novo local
    if caminho.startswith('/'):
        # Caminho absoluto
        if caminho == "/":
             novo_local = "/"
        elif caminho.endswith('/'):
            novo_local = caminho[:-1] # Remove barra final para padronizar
        else:
            novo_local = caminho
    else:
        # Caminho relativo
        partes_caminho_atual = [p for p in local_atual.split('/') if p]

        # Tratar '..' (subir um nível)
        partes_caminho_novo = []
        for parte in caminho.split('/'):
            if parte == '..':
                if partes_caminho_atual:
                    partes_caminho_atual.pop()
            elif parte and parte != '.':
                partes_caminho_novo.append(parte)

        # Junta o caminho atual base com o caminho relativo
        if partes_caminho_novo:
            novo_local = "/" + "/".join(partes_caminho_atual + partes_caminho_novo)
        elif partes_caminho_atual:
             novo_local = "/" + "/".join(partes_caminho_atual)
        else:
             novo_local = "/" # Se era "/", continua em "/"

    # Garantir que o local mínimo é a raiz
    if not novo_local:
         novo_local = "/"

    # 2. Empilhar o local atual (se for diferente)
    if local_atual != novo_local:
        voltar_pilha.append(local_atual)
        
        # 3. Limpar AVANCAR
        avancar_pilha.clear()
        
        # 4. Atualizar o local
        print(f"INFO: Movendo de '{local_atual}' para '{novo_local}'.")
        return novo_local, voltar_pilha, avancar_pilha
    else:
        print(f"INFO: Já está em '{local_atual}'. Nenhuma mudança feita.")
        return local_atual, voltar_pilha, avancar_pilha


def voltar_local(local_atual, voltar_pilha, avancar_pilha):
    """
    VOLTAR
    Retorna ao local anterior (move do topo de VOLTAR para AVANCAR).
    """
    if not voltar_pilha:
        print("ERRO: Pilha VOLTAR vazia. Não é possível retornar.")
        return local_atual, voltar_pilha, avancar_pilha
    
    # Move local atual para AVANCAR
    avancar_pilha.append(local_atual)
    
    # Retira o local anterior de VOLTAR e define como novo local atual
    novo_local = voltar_pilha.pop()
    
    print(f"INFO: Retornando para '{novo_local}'.")
    return novo_local, voltar_pilha, avancar_pilha


def avancar_local(local_atual, voltar_pilha, avancar_pilha):
    """
    AVANCAR
    Avança novamente (move do topo de AVANCAR para VOLTAR).
    """
    if not avancar_pilha:
        print("ERRO: Pilha AVANCAR vazia. Não é possível avançar.")
        return local_atual, voltar_pilha, avancar_pilha

    # Move local atual para VOLTAR
    voltar_pilha.append(local_atual)
    
    # Retira o local avançado de AVANCAR e define como novo local atual
    novo_local = avancar_pilha.pop()
    
    print(f"INFO: Avançando para '{novo_local}'.")
    return novo_local, voltar_pilha, avancar_pilha


def onde(local_atual):
    """
    ONDE
    Mostra o local atual (ex.: /Palco).
    """
    print(f"Local atual: {local_atual}")


def mapa_simples(voltar_pilha, local_atual, avancar_pilha):
    """
    MAPA (bônus)
    Mostra visualização textual simples dos locais visitados.
    """
    print("\n--- MAPA DE NAVEGAÇÃO ---")
    
    # 1. Pilha VOLTAR (Locais anteriores, do mais recente ao mais antigo)
    if voltar_pilha:
        print("<- VOLTAR:")
        # Exibe do topo para a base (topo = último elemento da lista)
        for i, local in enumerate(reversed(voltar_pilha)):
            print(f"  ({len(voltar_pilha) - i}) {local}")
    else:
        print("<- VOLTAR: (Vazio)")

    # 2. Local Atual
    print(f"\n-> LOCAL ATUAL: {local_atual}")

    # 3. Pilha AVANCAR (Locais futuros, do mais recente ao mais antigo)
    if avancar_pilha:
        print("\n-> AVANÇAR:")
        # Exibe do topo para a base (topo = último elemento da lista)
        for i, local in enumerate(reversed(avancar_pilha)):
            print(f"  ({len(avancar_pilha) - i}) {local}")
    else:
        print("\n-> AVANÇAR: (Vazio)")
    print("-------------------------")


# --- EXEMPLO DE USO (apenas para testar o funcionamento) ---
"""
# Inicialização do estado
LOCAL_ATUAL = "/"
VOLTAR_PILHA = []
AVANCAR_PILHA = []

# Chamada das funções
print("--- TESTE INICIAL ---")
onde(LOCAL_ATUAL)
mapa_simples(VOLTAR_PILHA, LOCAL_ATUAL, AVANCAR_PILHA)

# 1. IR para Palco (Relativo, a partir de /)
LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA = ir_local("Palco", LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA)
onde(LOCAL_ATUAL)

# 2. IR para IA/Visao (Absoluto)
LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA = ir_local("/IA/Visao", LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA)
onde(LOCAL_ATUAL)

# 3. VOLTAR
LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA = voltar_local(LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA)
onde(LOCAL_ATUAL)

# 4. IR para Robótica (Relativo, a partir de /)
LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA = ir_local("Robótica", LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA)
onde(LOCAL_ATUAL)

# 5. AVANCAR (Deve falhar)
LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA = avancar_local(LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA)
onde(LOCAL_ATUAL)

# 6. VOLTAR
LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA = voltar_local(LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA)
onde(LOCAL_ATUAL)

# 7. AVANCAR (Deve funcionar)
LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA = avancar_local(LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA)
onde(LOCAL_ATUAL)

# 8. Teste de caminho relativo '..' (a partir de /Robótica)
LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA = ir_local("..", LOCAL_ATUAL, VOLTAR_PILHA, AVANCAR_PILHA)
onde(LOCAL_ATUAL)

# 9. Teste MAPA
mapa_simples(VOLTAR_PILHA, LOCAL_ATUAL, AVANCAR_PILHA)
"""