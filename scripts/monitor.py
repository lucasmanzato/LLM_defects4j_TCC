"""
Script para monitorar e mostrar progresso da classificação com relatório em tempo real
"""
import json
import time
import os
from datetime import datetime

def monitor_classification():
    """Monitora o progresso da classificação com estatísticas em tempo real."""
    
    results_path = 'outputs/results_with_llm.json'
    last_count = 0
    
    print("\n" + "="*80)
    print(" MONITORAMENTO DE CLASSIFICAÇÃO COM LLAMA 2")
    print("="*80 + "\n")
    
    while True:
        try:
            if not os.path.exists(results_path):
                print("[AGUARDANDO] Arquivo de resultados ainda não gerado...")
                time.sleep(5)
                continue
            
            with open(results_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            # Contar classificações completas
            classified = sum(1 for r in results if r.get('llm_classification') and 
                           r.get('llm_classification', {}).get('confianca') != 0)
            total = len(results)
            
            # Mostrar progresso se houver mudança
            if classified != last_count:
                percentage = classified / total * 100
                bar_length = 50
                filled = int(bar_length * classified / total)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                print(f"\r[{bar}] {classified}/{total} ({percentage:5.1f}%)", end="", flush=True)
                
                # A cada 5 bugs, mostrar estatísticas
                if classified % 5 == 0:
                    print(f"\n  Tempo decorrido: ~{classified * 0.8:.0f}s (estimado)")
                    
                    # Estatísticas parciais
                    confirmed = sum(1 for r in results[:classified] 
                                  if r.get('llm_classification', {}).get('eh_bug_real'))
                    if classified > 0:
                        print(f"  Bugs confirmados até agora: {confirmed}/{classified} ({confirmed/classified*100:.0f}%)")
                
                last_count = classified
            
            # Se terminou
            if classified == total:
                print(f"\n\n[CONCLUIDO] Classificação finalizada em {datetime.now().strftime('%H:%M:%S')}")
                break
            
            time.sleep(2)
            
        except json.JSONDecodeError:
            print("[AGUARDANDO] Arquivo sendo escrito...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[CANCELADO] Monitoramento interrompido pelo usuário")
            break
        except Exception as e:
            print(f"[ERRO] {e}")
            time.sleep(5)

def show_live_stats():
    """Mostra estatísticas do arquivo JSON conforme é atualizado."""
    
    results_path = 'outputs/results_with_llm.json'
    
    print("\n" + "="*80)
    print(" ESTATÍSTICAS EM TEMPO REAL")
    print("="*80 + "\n")
    
    time.sleep(30)  # Aguardar um pouco de processamento
    
    while True:
        try:
            with open(results_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            # Contar
            classified = sum(1 for r in results if r.get('llm_classification', {}).get('motivo', '').lower() != 'erro ao parsear resposta')
            confirmed = sum(1 for r in results if r.get('llm_classification', {}).get('eh_bug_real'))
            
            if classified > 0:
                from collections import defaultdict
                patterns_stats = defaultdict(lambda: {'confirmed': 0, 'total': 0})
                
                for r in results[:classified]:
                    pattern = r.get('match', {}).get('pattern_name', '?')
                    is_bug = r.get('llm_classification', {}).get('eh_bug_real', False)
                    patterns_stats[pattern]['total'] += 1
                    if is_bug:
                        patterns_stats[pattern]['confirmed'] += 1
                
                print(f"\nDados processados até agora: {classified}/{len(results)}")
                print(f"Taxa de confirmação: {confirmed}/{classified} ({confirmed/classified*100:.1f}%)\n")
                
                print(f"{'Padrão':<25} {'Confirmados':<15} {'Taxa':<10}")
                print("-" * 50)
                
                for pattern in sorted(patterns_stats.keys()):
                    stats = patterns_stats[pattern]
                    total_p = stats['total']
                    conf_p = stats['confirmed']
                    taxa = conf_p / total_p * 100 if total_p > 0 else 0
                    print(f"{pattern:<25} {conf_p}/{total_p:<13} {taxa:>6.1f}%")
            
            time.sleep(10)
            
        except:
            time.sleep(5)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'stats':
        show_live_stats()
    else:
        monitor_classification()
