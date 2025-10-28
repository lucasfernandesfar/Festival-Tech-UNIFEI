# terminal.py
import fila
import pilha
import Roteiro

def ajuda():
    return (
        "\nComandos disponíveis:\n"
        "-----------------------------------\n"
        "COMPRAR <nome> <categoria>\n"
        "ENTRAR\n"
        "ESPIAR\n"
        "CANCELAR <id>\n"
        "LISTAR\n"
        "ESTATISTICAS\n"
        "MODO <PADRAO|PRIORIDADE>\n"
        "IR <caminho>              (caminhos absolutos (/IA/Visao) ou relativos (Palco, Robótica)\n"
        "VOLTAR\n"
        "AVANCAR\n"
        "ONDE\n"
        "DESFAZER\n"
        "REFAZER\n"
        "SAIR\n"
        "-----------------------------------"
    )

def main():
    # --- ESTADOS INICIAIS (mantidos dentro da função) ---
    estado_fila = fila.ESTADO_INICIAL.copy()
    local_atual = "/"
    voltar_pilha = []
    avancar_pilha = []
    estado_pilha = {
        "local_atual": "/",
        "voltar_pilha": [],
        "avancar_pilha": [],
        "estado_geral_simulado": "Normal",
    }

    # Historicos separados para fila e para "estado_pilha"
    historico_undo_fila = []
    historico_redo_fila = []
    historico_undo_pilha = []
    historico_redo_pilha = []

    print("=== SISTEMA DE TERMINAL ===")
    print("Digite 'AJUDA' para ver os comandos disponíveis.")

    while True:
        comando = input("\n> ").strip()

        if not comando:
            continue

        partes = comando.split()
        cmd = partes[0].upper()

        # --- AJUDA / SAIR ---
        if cmd == "AJUDA":
            print(ajuda())
        elif cmd == "SAIR":
            print("Encerrando o sistema...")
            break

        # --- FILA (agora com UNDO/REDO via pilha._aplicar_comando) ---
        elif cmd == "COMPRAR" and len(partes) >= 3:
            nome = partes[1]
            categoria = partes[2]
            estado_fila, historico_undo_fila, historico_redo_fila = pilha._aplicar_comando(
                estado_fila, historico_undo_fila, historico_redo_fila, fila.comprar, nome, categoria
            )

        elif cmd == "ENTRAR":
            estado_fila, historico_undo_fila, historico_redo_fila = pilha._aplicar_comando(
                estado_fila, historico_undo_fila, historico_redo_fila, fila.entrar
            )

        elif cmd == "ESPIAR":
            estado_fila = fila.espiar(estado_fila)

        elif cmd == "CANCELAR" and len(partes) == 2:
            estado_fila, historico_undo_fila, historico_redo_fila = pilha._aplicar_comando(
                estado_fila, historico_undo_fila, historico_redo_fila, fila.cancelar, partes[1]
            )

        elif cmd == "LISTAR":
            estado_fila = fila.listar(estado_fila)

        elif cmd == "ESTATISTICAS":
            estado_fila = fila.estatisticas(estado_fila)

        elif cmd == "MODO" and len(partes) == 2:
            estado_fila, historico_undo_fila, historico_redo_fila = pilha._aplicar_comando(
                estado_fila, historico_undo_fila, historico_redo_fila, fila.modo, partes[1]
            )

        # --- ROTEIRO ---
        elif cmd == "IR" and len(partes) == 2:
            local_atual, voltar_pilha, avancar_pilha = Roteiro.ir_local(
                partes[1], local_atual, voltar_pilha, avancar_pilha
            )

        elif cmd == "VOLTAR":
            local_atual, voltar_pilha, avancar_pilha = Roteiro.voltar_local(
                local_atual, voltar_pilha, avancar_pilha
            )

        elif cmd == "AVANCAR":
            local_atual, voltar_pilha, avancar_pilha = Roteiro.avancar_local(
                local_atual, voltar_pilha, avancar_pilha
            )

        elif cmd == "ONDE":
            Roteiro.onde(local_atual)

        # --- PILHA (DESFAZER / REFAZER) para o estado de navegação/simulado (estado_pilha) ---
        elif cmd == "DESFAZER":
            # Primeiro tenta desfazer ações na FILA (se houver histórico)
            if historico_undo_fila:
                estado_fila, historico_undo_fila, historico_redo_fila = pilha.desfazer(
                    estado_fila, historico_undo_fila, historico_redo_fila
                )
                # mensagem genérica; fila restaurada
                print("OK: desfaz ação na fila.")
            # Senão tenta desfazer ações no estado_pilha (navegação)
            elif historico_undo_pilha:
                estado_pilha, historico_undo_pilha, historico_redo_pilha = pilha.desfazer(
                    estado_pilha, historico_undo_pilha, historico_redo_pilha
                )
                print("OK: desfaz ação de navegação.")
            else:
                print("ERRO DESFAZER: Nada a desfazer.")

        elif cmd == "REFAZER":
            # tenta refazer na fila primeiro, depois no estado_pilha
            if historico_redo_fila:
                estado_fila, historico_undo_fila, historico_redo_fila = pilha.refazer(
                    estado_fila, historico_undo_fila, historico_redo_fila
                )
                print("OK: refaz ação na fila.")
            elif historico_redo_pilha:
                estado_pilha, historico_undo_pilha, historico_redo_pilha = pilha.refazer(
                    estado_pilha, historico_undo_pilha, historico_redo_pilha
                )
                print("OK: refaz ação de navegação.")
            else:
                print("ERRO REFAZER: Nada a refazer.")

        else:
            print("Comando inválido. Digite 'AJUDA' para ver a lista de comandos.")


if __name__ == "__main__":
    main()
