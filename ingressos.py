# ingressos.py
from collections import deque


# MODELO E CRIAÇÃO DE INGRESSOS


def criar_ingresso(proximo_id, nome, categoria, tempo_chegada):
    """
    Cria um dicionário representando um ingresso.
    """
    categoria = categoria.upper()
    if categoria not in ["VIP", "INTEIRA", "MEIA"]:
        return None, f"ERRO: Categoria '{categoria}' inválida. Use VIP, INTEIRA ou MEIA."

    ingresso = {
        "id": proximo_id,
        "nome": nome,
        "categoria": categoria,
        "chegada_logica": tempo_chegada,
        "tempo_espera": 0
    }
    return ingresso, None



# FUNÇÕES DE ESTATÍSTICAS


def inicializar_estatisticas():
    """
    Cria o dicionário inicial de estatísticas.
    """
    return {
        "total_pendente": 0,
        "total_atendido": 0,
        "tempo_total_espera": 0,
        "tempo_medio": 0,
        "pendente_por_categoria": {"VIP": 0, "INTEIRA": 0, "MEIA": 0},
        "atendido_por_categoria": {"VIP": 0, "INTEIRA": 0, "MEIA": 0}
    }


def atualizar_estatisticas(estado):
    """
    Atualiza o dicionário de estatísticas com base no estado atual das filas e atendimentos.
    """
    estat = inicializar_estatisticas()

    # --- Contar pendentes ---
    if estado["modo_atendimento"] == "PADRAO":
        _contar_fila(estat, estado["fila_padrao"])
    else:
        _contar_fila(estat, estado["fila_vip"])
        _contar_fila(estat, estado["fila_inteira"])
        _contar_fila(estat, estado["fila_meia"])

    # --- Contar atendidos ---
    for ingresso in estado["atendidos"]:
        cat = ingresso["categoria"]
        estat["atendido_por_categoria"][cat] += 1
        estat["total_atendido"] += 1
        estat["tempo_total_espera"] += ingresso.get("tempo_espera", 0)

    if estat["total_atendido"] > 0:
        estat["tempo_medio"] = estat["tempo_total_espera"] / estat["total_atendido"]

    return estat


def _contar_fila(estat, fila):
    """
    Função auxiliar que soma os ingressos de uma fila às estatísticas.
    """
    for ing in fila:
        estat["total_pendente"] += 1
        estat["pendente_por_categoria"][ing["categoria"]] += 1


def exibir_estatisticas(estat, relogio_logico):
    """
    Exibe as estatísticas formatadas.
    """
    print("\n--- ESTATÍSTICAS ---")
    print(f"Relógio Lógico Atual: {relogio_logico} minutos")
    print(f"Total Pendente: {estat['total_pendente']}")
    print(f"Total Atendido: {estat['total_atendido']}")
    print(f"Tempo Médio de Espera: {estat['tempo_medio']:.2f} minutos")

    print("\nContagem por Categoria (PENDENTE):")
    for cat, qtd in estat["pendente_por_categoria"].items():
        print(f"  - {cat}: {qtd}")

    print("\nContagem por Categoria (ATENDIDO):")
    for cat, qtd in estat["atendido_por_categoria"].items():
        print(f"  - {cat}: {qtd}")
    print("--------------------")

# TESTE INDEPENDENTE 

def main():
    """
    Teste isolado do módulo de ingressos.
    """
    from collections import deque

    # Estado simulado
    estado = {
        "modo_atendimento": "PRIORIDADE",
        "fila_vip": deque([{"id": 1, "nome": "Ana", "categoria": "VIP"}]),
        "fila_inteira": deque([{"id": 2, "nome": "Bruno", "categoria": "INTEIRA"}]),
        "fila_meia": deque(),
        "fila_padrao": deque(),
        "atendidos": [{"id": 3, "nome": "Clara", "categoria": "MEIA", "tempo_espera": 3}],
        "relogio_logico": 5
    }

    estat = atualizar_estatisticas(estado)
    exibir_estatisticas(estat, estado["relogio_logico"])


if __name__ == "__main__":
    main()
