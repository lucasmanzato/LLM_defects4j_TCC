"""
Script to monitor and display classification progress with real-time report
"""
import json
import time
import os
from datetime import datetime

def monitor_classification():
    """Monitors classification progress with real-time statistics."""
    
    results_path = 'outputs/results_with_llm.json'
    last_count = 0
    
    print("\n" + "="*80)
    print(" LLAMA 2 CLASSIFICATION MONITORING")
    print("="*80 + "\n")
    
    while True:
        try:
            if not os.path.exists(results_path):
                print("[WAITING] Results file not yet created...")
                time.sleep(5)
                continue
            
            with open(results_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            # Count completed classifications
            classified = sum(1 for r in results if r.get('llm_classification') and 
                           r.get('llm_classification', {}).get('confianca') != 0)
            total = len(results)
            
            # Show progress if there are changes
            if classified != last_count:
                percentage = classified / total * 100
                bar_length = 50
                filled = int(bar_length * classified / total)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                print(f"\r[{bar}] {classified}/{total} ({percentage:5.1f}%)", end="", flush=True)
                
                # Every 5 bugs, show statistics
                if classified % 5 == 0:
                    print(f"\n  Elapsed time: ~{classified * 0.8:.0f}s (estimated)")
                    
                    # Partial statistics
                    confirmed = sum(1 for r in results[:classified] 
                                  if r.get('llm_classification', {}).get('eh_bug_real'))
                    if classified > 0:
                        print(f"  Confirmed bugs so far: {confirmed}/{classified} ({confirmed/classified*100:.0f}%)")
                
                last_count = classified
            
            # If finished
            if classified == total:
                print(f"\n\n[COMPLETE] Classification finished at {datetime.now().strftime('%H:%M:%S')}")
                break
            
            time.sleep(2)
            
        except json.JSONDecodeError:
            print("[WAITING] File is being written...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[CANCELLED] Monitoring interrupted by user")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(5)

def show_live_stats():
    """Shows statistics of JSON file as it is updated."""
    
    results_path = 'outputs/results_with_llm.json'
    
    print("\n" + "="*80)
    print(" REAL-TIME STATISTICS")
    print("="*80 + "\n")
    
    time.sleep(30)  # Wait a bit for processing
    
    while True:
        try:
            with open(results_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            # Count
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
                
                print(f"\nProcessed data so far: {classified}/{len(results)}")
                print(f"Confirmation rate: {confirmed}/{classified} ({confirmed/classified*100:.1f}%)\n")
                
                print(f"{'Pattern':<25} {'Confirmed':<15} {'Rate':<10}")
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
