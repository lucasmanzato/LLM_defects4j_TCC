"""
Script that waits for classification completion and generates reports automatically
"""
import json
import time
import os
from datetime import datetime

def wait_for_classification():
    """Waits for classification to complete."""
    
    print("\n" + "="*80)
    print(" WAITING FOR LLAMA 2 CLASSIFICATION TO COMPLETE")
    print("="*80 + "\n")
    
    results_path = 'outputs/results_with_llm.json'
    last_count = 0
    
    while True:
        try:
            if not os.path.exists(results_path):
                print("[WAITING] Results file not yet created...")
                time.sleep(10)
                continue
            
            with open(results_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            # Count valid classifications (not "Parse error")
            classified = sum(1 for r in results if r.get('llm_classification') 
                           and r.get('llm_classification', {}).get('motivo', '').lower() != 'erro ao parsear resposta')
            
            total = len(results)
            
            if classified > last_count:
                percentage = classified / total * 100
                bar_length = 50
                filled = int(bar_length * classified / total)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                elapsed = (classified * 0.8)  # Estimate: ~0.8s per bug
                remaining = ((total - classified) * 0.8)
                
                print(f"\r[{bar}] {classified}/{total} ({percentage:5.1f}%) | "
                      f"Time: {elapsed:5.0f}s | Remaining: ~{remaining:5.0f}s", 
                      end="", flush=True)
                
                last_count = classified
            
            # If finished
            if classified == total:
                print(f"\n\n✅ CLASSIFICATION COMPLETE!")
                print(f"   Timestamp: {datetime.now().strftime('%H:%M:%S')}")
                return results
            
            time.sleep(3)
            
        except json.JSONDecodeError:
            print("[INFO] File is being written...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[CANCELLED] Wait interrupted")
            return None
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(5)

def generate_reports():
    """Generates all reports."""
    
    print("\n" + "="*80)
    print(" GENERATING REPORTS")
    print("="*80 + "\n")
    
    try:
        print("[1/2] Generating Markdown report...")
        from report_markdown import generate_report
        generate_report()
    except Exception as e:
        print(f"[ERROR] Failed to generate Markdown: {e}")
    
    try:
        print("[2/2] Generating HTML report...")
        from report_html import generate_html_report
        generate_html_report()
    except Exception as e:
        print(f"[ERROR] Failed to generate HTML: {e}")

def show_summary(results):
    """Shows results summary."""
    
    print("\n" + "="*80)
    print(" RESULTS SUMMARY")
    print("="*80 + "\n")
    
    total = len(results)
    confirmed = sum(1 for r in results if r.get('llm_classification', {}).get('eh_bug_real'))
    
    # Stats by pattern
    from collections import defaultdict
    patterns = defaultdict(lambda: {'total': 0, 'confirmed': 0})
    
    for r in results:
        pattern = r.get('match', {}).get('pattern_name', 'Unknown')
        patterns[pattern]['total'] += 1
        if r.get('llm_classification', {}).get('eh_bug_real'):
            patterns[pattern]['confirmed'] += 1
    
    print(f"Total bugs analyzed:       {total}")
    print(f"Confirmed bugs:            {confirmed} ({confirmed/total*100:.1f}%)")
    print(f"Unconfirmed bugs:          {total-confirmed} ({(total-confirmed)/total*100:.1f}%)\n")
    
    print(f"{'Pattern':<25} {'Total':<8} {'Confirmed':<15} {'Rate':<10}")
    print("-" * 60)
    
    for pattern in sorted(patterns.keys()):
        stats = patterns[pattern]
        total_p = stats['total']
        conf_p = stats['confirmed']
        taxa = conf_p / total_p * 100 if total_p > 0 else 0
        print(f"{pattern:<25} {total_p:<8} {conf_p:<15} {taxa:>6.1f}%")

def main():
    """Executes the complete flow."""
    
    # Wait for completion
    results = wait_for_classification()
    
    if results is None:
        return
    
    # Show summary
    show_summary(results)
    
    # Generate reports
    generate_reports()
    
    # Final message
    print("\n" + "="*80)
    print(" ✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\n📊 Available reports:\n")
    print("  1. 📄 outputs/report_llm.md")
    print("     └─ Markdown (share via email/chat)\n")
    print("  2. 🌐 outputs/report_visual.html")
    print("     └─ HTML with charts (open in browser)\n")
    print("  3. 📊 outputs/results_with_llm.json")
    print("     └─ Raw data (import in tools)\n")
    print("  📖 Read: RELATORIO_GUIA.md for more details\n")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
