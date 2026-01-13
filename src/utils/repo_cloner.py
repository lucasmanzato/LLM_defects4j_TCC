"""
Repository cloner for Java projects.
Handles git operations and validation.
"""
import os
import sys
from pathlib import Path


def instalar_dependencias():
    """Instala GitPython dinamicamente se necessário."""
    try:
        import importlib
        git = importlib.import_module('git')
        globals()['git'] = git
        print("GitPython já está instalado.")
    except ImportError:
        print("GitPython não encontrado. Instalando...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'GitPython'])
        import importlib
        git = importlib.import_module('git')
        globals()['git'] = git
        print("GitPython instalado com sucesso!")


def clonar_repositorio_java(url: str, destino: str) -> bool:
    """
    Clona um repositório Git e valida se contém arquivos Java.
    
    Args:
        url: URL do repositório Git
        destino: Caminho de destino para clonagem
        
    Returns:
        True se bem-sucedido, False caso contrário
    """
    instalar_dependencias()
    
    print("--- Iniciando clonagem de repositório ---")
    print(f"URL: {url}")
    print(f"Destino: {os.path.abspath(destino)}")
    
    # Verifica se já existe
    if os.path.exists(destino):
        if os.path.isdir(os.path.join(destino, '.git')):
            print(f"Repositório já existe em '{destino}'.")
            print("Mantendo repositório existente.")
            return contar_arquivos_java(destino) > 0
        else:
            print(f"Erro: '{destino}' existe mas não é um repositório Git.")
            return False
    
    # Clona repositório
    try:
        print("Clonando repositório...")
        git.Repo.clone_from(url, destino)
        print("✓ Clonagem concluída")
    except Exception as e:
        print(f"✗ Erro ao clonar: {e}")
        return False
    
    # Valida arquivos Java
    java_count = contar_arquivos_java(destino)
    if java_count > 0:
        print(f"✓ Encontrados {java_count} arquivos .java")
        return True
    else:
        print("✗ Nenhum arquivo .java encontrado")
        return False


def contar_arquivos_java(diretorio: str) -> int:
    """Conta arquivos .java no diretório."""
    count = 0
    for root, dirs, files in os.walk(diretorio):
        count += sum(1 for f in files if f.endswith('.java'))
    return count


if __name__ == '__main__':
    # Teste básico
    url_teste = 'https://github.com/apache/commons-lang.git'
    destino_teste = 'dados/commons-lang'
    clonar_repositorio_java(url_teste, destino_teste)
