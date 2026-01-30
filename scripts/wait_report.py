"""
Script que aguarda conclusão da classificação e gera relatórios automaticamente
"""
import json
import time
import os
from datetime import datetime

def wait_for_classification():
    """Aguarda conclusão da classificação."""
    
    print("\n" + "="*80)
    print(" AGUARDANDO CONCLUSÃO DA CLASSIFICAÇÃO COM LLAMA 2")
    print("="*80 + "\n")
    
    results_path = 'outputs/results_with_llm.json'
    last_count = 0
    
    while True:
        try:
            if not os.path.exists(results_path):
                print("[AGUARDANDO] Arquivo de resultados ainda não criado...")
                time.sleep(10)
                continue
            
            with open(results_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            # Contar classificações válidas (não "Parse error")
            classified = sum(1 for r in results if r.get('llm_classification') 
                           and r.get('llm_classification', {}).get('motivo', '').lower() != 'erro ao parsear resposta')
            
            total = len(results)
            
            if classified > last_count:
                percentage = classified / total * 100
                bar_length = 50
                filled = int(bar_length * classified / total)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                elapsed = (classified * 0.8)  # Estimativa: ~0.8s por bug
                remaining = ((total - classified) * 0.8)
                
                print(f"\r[{bar}] {classified}/{total} ({percentage:5.1f}%) | "
                      f"Tempo: {elapsed:5.0f}s | Restante: ~{remaining:5.0f}s", 
                      end="", flush=True)
                
                last_count = classified
            
            # Se terminou
            if classified == total:
                print(f"\n\n✅ CLASSIFICAÇÃO CONCLUÍDA!")
                print(f"   Horário: {datetime.now().strftime('%H:%M:%S')}")
                return results
            
            time.sleep(3)
            
        except json.JSONDecodeError:
            print("[INFO] Arquivo está sendo escrito...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[CANCELADO] Espera interrompida")
            return None
        except Exception as e:
            print(f"[ERRO] {e}")
            time.sleep(5)

def generate_reports():
    """Gera todos os relatórios."""
    
    print("\n" + "="*80)
    print(" GERANDO RELATÓRIOS")
    print("="*80 + "\n")
    
    try:
        print("[1/2] Gerando relatório Markdown...")
        from report_markdown import generate_report
        generate_report()
    except Exception as e:
        print(f"[ERRO] Falha ao gerar Markdown: {e}")
    
    try:
        print("[2/2] Gerando relatório HTML...")
        from report_html import generate_html_report
        generate_html_report()
    except Exception as e:
        print(f"[ERRO] Falha ao gerar HTML: {e}")

def show_summary(results):
    """Mostra resumo dos resultados."""
    
    print("\n" + "="*80)
    print(" RESUMO DE RESULTADOS")
    print("="*80 + "\n")
    
    total = len(results)
    confirmed = sum(1 for r in results if r.get('llm_classification', {}).get('eh_bug_real'))
    
    # Estatísticas por padrão
    from collections import defaultdict
    patterns = defaultdict(lambda: {'total': 0, 'confirmed': 0})
    
    for r in results:
        pattern = r.get('match', {}).get('pattern_name', 'Desconhecido')
        patterns[pattern]['total'] += 1
        if r.get('llm_classification', {}).get('eh_bug_real'):
            patterns[pattern]['confirmed'] += 1
    
    print(f"Total de bugs analisados:  {total}")
    print(f"Bugs confirmados:          {confirmed} ({confirmed/total*100:.1f}%)")
    print(f"Bugs não confirmados:      {total-confirmed} ({(total-confirmed)/total*100:.1f}%)\n")
    
    print(f"{'Padrão':<25} {'Total':<8} {'Confirmados':<15} {'Taxa':<10}")
    print("-" * 60)
    
    for pattern in sorted(patterns.keys()):
        stats = patterns[pattern]
        total_p = stats['total']
        conf_p = stats['confirmed']
        taxa = conf_p / total_p * 100 if total_p > 0 else 0
        print(f"{pattern:<25} {total_p:<8} {conf_p:<15} {taxa:>6.1f}%")

def main():
    """Executa o fluxo completo."""
    
    # Aguardar conclusão
    results = wait_for_classification()
    
    if results is None:
        return
    
    # Mostrar resumo
    show_summary(results)
    
    # Gerar relatórios
    generate_reports()
    
    # Mensagem final
    print("\n" + "="*80)
    print(" ✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print("="*80)
    print("\n📊 Relatórios disponíveis:\n")
    print("  1. 📄 outputs/relatorio_llm.md")
    print("     └─ Markdown (compartilhar por email/chat)\n")
    print("  2. 🌐 outputs/relatorio_visual.html")
    print("     └─ HTML com gráficos (abrir no navegador)\n")
    print("  3. 📊 outputs/results_with_llm.json")
    print("     └─ Dados brutos (importar em ferramentas)\n")
    print("  📖 Leia: RELATORIO_GUIA.md para mais detalhes\n")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
