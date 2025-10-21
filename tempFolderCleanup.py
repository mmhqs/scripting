import os
import tempfile


def limpar_pasta_temporaria():
    """
    Esta função apaga todos os arquivos na pasta temporária do sistema.
    Ela não remove subdiretórios.
    """
    # Obtém o caminho da pasta temporária do sistema operacional
    pasta_temp = tempfile.gettempdir()
    arquivos_apagados = 0
    arquivos_falharam = 0

    print(f"Limpando a pasta: {pasta_temp}\n")

    # Lista todos os itens (arquivos e pastas) no diretório temporário
    for nome_do_arquivo in os.listdir(pasta_temp):
        # Cria o caminho completo para o arquivo
        caminho_do_arquivo = os.path.join(pasta_temp, nome_do_arquivo)

        # Tenta apagar o arquivo
        try:
            # Verifica se é um arquivo (e não uma pasta) antes de apagar
            if os.path.isfile(caminho_do_arquivo) or os.path.islink(caminho_do_arquivo):
                os.unlink(caminho_do_arquivo)
                arquivos_apagados += 1

        except Exception as e:
            arquivos_falharam += 1

    print("\n--- Limpeza concluída ---")
    print(f"Total de arquivos apagados: {arquivos_apagados}")
    print(
        f"Total de falhas (arquivos em uso ou sem permissão): {arquivos_falharam}")


if __name__ == "__main__":
    limpar_pasta_temporaria()
