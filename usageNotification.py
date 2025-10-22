import psutil
import time
# Importa a biblioteca de notificação
from win10toast_click import ToastNotifier

# --- CONFIGURAÇÕES ---
CPU_THRESHOLD = 80  # Limite em % para a CPU
RAM_THRESHOLD = 80  # Limite em % para a RAM
INTERVALO_MONITORAMENTO = 10  # Segundos entre cada verificação
# ---------------------


def enviar_notificacao(titulo, mensagem):
    """Envia uma notificação nativa do Windows."""
    try:
        toaster = ToastNotifier()
        toaster.show_toast(
            titulo,
            mensagem,
            duration=10,  # Duração que a notificação fica na tela (segundos)
            threaded=True  # Para não bloquear o script enquanto a notificação é exibida
        )
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")


def iniciar_monitoramento():
    """Função principal que monitora e envia alertas."""

    # Flags de estado para evitar spam de notificações
    # (Só notifica uma vez quando cruza o limite)
    cpu_alerta_enviado = False
    ram_alerta_enviado = False

    print("--- Monitor de Alertas de Recursos ---")
    print(f"Alerta de CPU: > {CPU_THRESHOLD}%")
    print(f"Alerta de RAM: > {RAM_THRESHOLD}%")
    print(f"Verificando a cada {INTERVALO_MONITORAMENTO} segundos.")
    print("\nPressione Ctrl+C para parar.")

    try:
        while True:
            # --- 1. Coletar Dados ---
            # (psutil.cpu_percent já pausa pelo 'intervalo')
            cpu_percent = psutil.cpu_percent(interval=INTERVALO_MONITORAMENTO)
            ram_percent = psutil.virtual_memory().percent

            # Imprime o status atual no terminal
            status_atual = f"Status: CPU: {cpu_percent:5.1f}% | RAM: {ram_percent:5.1f}%"
            # Usamos \r e end='' para escrever na mesma linha (como no script anterior)
            print('\r' + status_atual + " " * 10, end='')

            # --- 2. Lógica de Alerta da CPU ---
            if cpu_percent > CPU_THRESHOLD and not cpu_alerta_enviado:
                print("\n[ALERTA] CPU acima do limite!")  # Aviso no terminal
                enviar_notificacao(
                    "Alerta de Desempenho",
                    f"Uso de CPU atingiu {cpu_percent:.1f}%!"
                )
                cpu_alerta_enviado = True  # Marca que o alerta foi enviado

            # Rearma o alerta se o uso voltar ao normal
            elif cpu_percent < CPU_THRESHOLD and cpu_alerta_enviado:
                print("\n[INFO] CPU voltou ao normal.")  # Aviso no terminal
                cpu_alerta_enviado = False

            # --- 3. Lógica de Alerta da RAM ---
            if ram_percent > RAM_THRESHOLD and not ram_alerta_enviado:
                print("\n[ALERTA] RAM acima do limite!")  # Aviso no terminal
                enviar_notificacao(
                    "Alerta de Desempenho",
                    f"Uso de RAM atingiu {ram_percent:.1f}%!"
                )
                ram_alerta_enviado = True

            # Rearma o alerta se o uso voltar ao normal
            elif ram_percent < RAM_THRESHOLD and ram_alerta_enviado:
                print("\n[INFO] RAM voltou ao normal.")  # Aviso no terminal
                ram_alerta_enviado = False

    except KeyboardInterrupt:
        print("\n\nMonitoramento interrompido pelo usuário. Até logo!")
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")


if __name__ == "__main__":
    iniciar_monitoramento()
