"""
Script principal para executar toda a pipeline com geração de relatórios
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    """Executa a pipeline completa de classificação e geração de relatórios."""
    
    print("\n" + "="*80)
    print(" PIPELINE DE DETECÇÃO E CLASSIFICAÇÃO DE BUGS COM LLAMA 2")
    print("="*80 + "\n")
    
    # 1. Executar classificação
    print("[1/3] Iniciando classificação com LLaMA 2...")
    print("-" * 80)
    
    proc = subprocess.Popen(
        [sys.executable, 'classify_with_llama.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Monitorar output
    while proc.poll() is None:
        try:
            line = proc.stdout.readline()
            if line:
                print(line.rstrip())
        except:
            break
    
    # Pegar último output se houver
    remaining_output = proc.stdout.read()
    if remaining_output:
        print(remaining_output)
    
    if proc.returncode != 0:
        print(f"[ERRO] Classificação falhou com código {proc.returncode}")
        return
    
    print("\n[OK] Classificação concluída!\n")
    
    # 2. Gerar relatório markdown
    print("[2/3] Gerando relatório em Markdown...")
    print("-" * 80)
    
    try:
        from generate_report import generate_report
        generate_report()
    except Exception as e:
        print(f"[ERRO] Falha ao gerar relatório Markdown: {e}")
    
    # 3. Gerar relatório HTML
    print("[3/3] Gerando relatório visual em HTML...")
    print("-" * 80)
    
    try:
        from generate_html_report import generate_html_report
        generate_html_report()
    except Exception as e:
        print(f"[ERRO] Falha ao gerar relatório HTML: {e}")
    
    # Resumo final
    print("\n" + "="*80)
    print(" PIPELINE CONCLUÍDA!")
    print("="*80)
    print("\nArquivos gerados:")
    print("  📊 outputs/results_with_llm.json - Resultados com classificação LLM")
    print("  📄 outputs/relatorio_llm.md - Relatório em Markdown")
    print("  🌐 outputs/relatorio_visual.html - Relatório visual em HTML")
    print("\nPróximos passos:")
    print("  1. Abra outputs/relatorio_visual.html no navegador")
    print("  2. Revise os bugs confirmados pela IA")
    print("  3. Use os dados para validação e correção\n")

if __name__ == '__main__':
    main()
