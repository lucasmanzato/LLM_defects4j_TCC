import os
import sys
import shutil
import subprocess

def instalar_dependencias():
    """
    Verifica e instala as dependências necessárias (GitPython).
    Útil para ambientes como Google Colab.
    """
    try:
        import git
        print("GitPython já está instalado.")
    except ImportError:
        print("GitPython não encontrado. Instalando...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "GitPython"])
            print("GitPython instalado com sucesso.")
            global git
            import git
        except Exception as e:
            print(f"Falha ao instalar GitPython: {e}")
            sys.exit(1)

# Chama a instalação de dependências logo no início
instalar_dependencias()
import git

def clonar_repositorio_java(url_repo, diretorio_destino):
    """
    Clona um repositório GitHub para um diretório local.

    Args:
        url_repo (str): A URL do repositório Git.
        diretorio_destino (str): O caminho local onde o repositório será salvo.

    Returns:
        str: O caminho absoluto do diretório clonado, ou None se falhar.
    """
    try:
        # Converte para caminho absoluto para evitar ambiguidades
        caminho_absoluto = os.path.abspath(diretorio_destino)
        
        print(f"--- Iniciando processo de aquisição ---")
        print(f"URL: {url_repo}")
        print(f"Destino: {caminho_absoluto}")

        # Verifica se o diretório já existe
        if os.path.exists(caminho_absoluto):
            # Verifica se já é um repositório git
            if os.path.exists(os.path.join(caminho_absoluto, ".git")):
                print(f"O diretório '{caminho_absoluto}' já existe e é um repositório Git.")
                print("Mantendo o repositório existente (pule esta etapa se quiser forçar um novo clone).")
                return caminho_absoluto
            else:
                print(f"O diretório '{caminho_absoluto}' existe mas não parece ser um repositório Git. Limpando...")
                # Remove o diretório existente para garantir um clone limpo
                # Tratamento para arquivos read-only no Windows pode ser necessário, mas shutil.rmtree costuma funcionar
                shutil.rmtree(caminho_absoluto)
        
        # Cria o diretório pai se não existir
        os.makedirs(os.path.dirname(caminho_absoluto), exist_ok=True)

        # Tenta clonar
        print("Clonando repositório...")
        git.Repo.clone_from(url_repo, caminho_absoluto)
        print("Clonagem concluída com sucesso!")
        
        return caminho_absoluto

    except git.exc.GitCommandError as e:
        print(f"Erro específico do Git ao clonar: {e}")
        return None
    except OSError as e:
        print(f"Erro de sistema de arquivos (permissão, caminho inválido, etc): {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def contar_arquivos_java(diretorio_projeto):
    """
    Conta quantos arquivos com extensão .java existem no diretório fornecido.
    
    Args:
        diretorio_projeto (str): Caminho do diretório do projeto.
    """
    if not diretorio_projeto or not os.path.exists(diretorio_projeto):
        print("Diretório inválido fornecido para contagem.")
        return

    contador_java = 0
    print(f"Verificando arquivos .java em: {diretorio_projeto}")

    for raiz, diretorios, arquivos in os.walk(diretorio_projeto):
        for arquivo in arquivos:
            if arquivo.endswith(".java"):
                contador_java += 1
    
    print(f"Total de arquivos .java encontrados: {contador_java}")
    
    # Validação simples
    if contador_java > 0:
        print("Confirmação: O repositório parece conter código Java.")
    else:
        print("Aviso: Nenhum arquivo .java encontrado. Verifique se o repositório está correto.")

if __name__ == "__main__":
    # Exemplo de uso
    # URL de um projeto Java popular (Apache Commons Lang) frequentemente usado em estudos de defeitos
    url_exemplo = "https://github.com/apache/commons-lang.git"
    destino_exemplo = "./dados/commons-lang"

    caminho_repo = clonar_repositorio_java(url_exemplo, destino_exemplo)
    
    if caminho_repo:
        contar_arquivos_java(caminho_repo)
