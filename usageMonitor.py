import psutil
import sys


def criar_barra_progresso(percentual, largura=20):
    preenchido = int(largura * percentual / 100)
    barra = '█' * preenchido + '-' * (largura - preenchido)
    return f"|{barra}|"


def exibir_monitor_linha_unica(intervalo=1):
    try:
        print("\n")
        print(f"Monitoramento atualizando a cada {intervalo}s")
        print("Pressione Ctrl+C para sair.")
        print("\n")

        while True:
            cpu_percent = psutil.cpu_percent(interval=intervalo)
            ram_percent = psutil.virtual_memory().percent

            barra_cpu = criar_barra_progresso(cpu_percent)
            barra_ram = criar_barra_progresso(ram_percent)

            linha_saida = f"CPU: {barra_cpu} {cpu_percent:5.1f}%   |   RAM: {barra_ram} {ram_percent:5.1f}%  "

            # \r (Carriage Return) move o cursor para o início da linha ATUAL
            # end='' (ou sys.stdout.write) evita que o print pule para a próxima linha
            sys.stdout.write('\r' + linha_saida)
            sys.stdout.flush()  # Força o Python a "despejar" o texto na tela

    except KeyboardInterrupt:
        print("\n\nMonitoramento interrompido pelo usuário. Até logo!\n")
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")


if __name__ == "__main__":
    exibir_monitor_linha_unica(intervalo=1)
