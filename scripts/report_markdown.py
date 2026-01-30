"""
Gera relatório detalhado da classificação com LLaMA
"""
import json
from datetime import datetime
from collections import defaultdict

def generate_report():
    """Gera relatório dos resultados com classificação LLM."""
    
    # Carregar resultados
    try:
        with open('outputs/results_with_llm.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("[ERRO] Arquivo results_with_llm.json nao encontrado")
        print("[INFO] Execute classify_with_llama.py primeiro")
        return
    
    print("\n" + "="*80)
    print(" RELATORIO DE DETECCAO DE BUGS - LLAMA 2")
    print("="*80)
    
    # Estatísticas gerais
    total = len(results)
    verified = sum(1 for r in results if r.get('llm_classification', {}).get('eh_realmente_bug'))
    not_verified = total - verified
    
    print(f"\n1. RESUMO EXECUTIVO")
    print("-" * 80)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Total de bugs analisados: {total}")
    print(f"Bugs confirmados pela IA: {verified} ({verified/total*100:.1f}%)")
    print(f"Bugs nao confirmados: {not_verified} ({not_verified/total*100:.1f}%)")
    
    # Estatísticas por padrão
    patterns_stats = defaultdict(lambda: {'total': 0, 'verified': 0, 'avg_score': 0, 'scores': []})
    
    for result in results:
        pattern = result.get('match', {}).get('pattern_name', 'Unknown')
        is_verified = result.get('llm_classification', {}).get('eh_realmente_bug', False)
        score = result.get('match', {}).get('score', 0)
        
        patterns_stats[pattern]['total'] += 1
        if is_verified:
            patterns_stats[pattern]['verified'] += 1
        patterns_stats[pattern]['scores'].append(score)
    
    # Calcular média
    for pattern in patterns_stats:
        scores = patterns_stats[pattern]['scores']
        patterns_stats[pattern]['avg_score'] = sum(scores) / len(scores) if scores else 0
    
    print(f"\n2. ANALISE POR PADRÃO DE BUG")
    print("-" * 80)
    print(f"{'Padrão':<35} {'Total':<8} {'Confirmados':<15} {'Taxa':<10} {'Score Médio':<12}")
    print("-" * 80)
    
    for pattern in sorted(patterns_stats.keys()):
        stats = patterns_stats[pattern]
        total_p = stats['total']
        verified_p = stats['verified']
        taxa = verified_p / total_p * 100 if total_p > 0 else 0
        avg_score = stats['avg_score']
        
        print(f"{pattern:<35} {total_p:<8} {verified_p:<15} {taxa:>6.1f}%    {avg_score:>6.4f}")
    
    # Top 10 bugs mais confiáveis
    print(f"\n3. TOP 10 BUGS MAIS CONFIÁVEIS")
    print("-" * 80)
    
    sorted_results = sorted(
        results,
        key=lambda x: (
            x.get('llm_classification', {}).get('confianca', 0),
            x.get('match', {}).get('score', 0)
        ),
        reverse=True
    )
    
    print(f"{'#':<4} {'Padrão':<25} {'Classe':<30} {'Confiança':<12} {'Score':<10}")
    print("-" * 80)
    
    for idx, result in enumerate(sorted_results[:10], 1):
        pattern = result.get('match', {}).get('pattern_name', '?')
        classname = result.get('class', '?')[:28]
        conf = result.get('llm_classification', {}).get('confianca', 0)
        score = result.get('match', {}).get('score', 0)
        
        print(f"{idx:<4} {pattern:<25} {classname:<30} {conf:>6.2%}      {score:>6.4f}")
    
    # Bugs não confirmados
    not_confirmed = [r for r in results if not r.get('llm_classification', {}).get('eh_realmente_bug')]
    
    print(f"\n4. BUGS NÃO CONFIRMADOS PELA IA ({len(not_confirmed)} casos)")
    print("-" * 80)
    print(f"{'#':<4} {'Padrão':<25} {'Classe':<30} {'Motivo':<20}")
    print("-" * 80)
    
    for idx, result in enumerate(not_confirmed[:5], 1):
        pattern = result.get('match', {}).get('pattern_name', '?')
        classname = result.get('class', '?')[:28]
        motivo = result.get('llm_classification', {}).get('motivo', '?')[:18]
        
        print(f"{idx:<4} {pattern:<25} {classname:<30} {motivo:<20}")
    
    if len(not_confirmed) > 5:
        print(f"... e mais {len(not_confirmed) - 5} bugs não confirmados")
    
    # Distribuição de confiança
    print(f"\n5. DISTRIBUIÇÃO DE CONFIANÇA")
    print("-" * 80)
    
    confidence_buckets = {
        '0.0-0.2': 0,
        '0.2-0.4': 0,
        '0.4-0.6': 0,
        '0.6-0.8': 0,
        '0.8-1.0': 0,
    }
    
    for result in results:
        conf = result.get('llm_classification', {}).get('confianca', 0)
        if conf < 0.2:
            confidence_buckets['0.0-0.2'] += 1
        elif conf < 0.4:
            confidence_buckets['0.2-0.4'] += 1
        elif conf < 0.6:
            confidence_buckets['0.4-0.6'] += 1
        elif conf < 0.8:
            confidence_buckets['0.6-0.8'] += 1
        else:
            confidence_buckets['0.8-1.0'] += 1
    
    for bucket, count in sorted(confidence_buckets.items()):
        percentage = count / total * 100
        bar = '█' * int(percentage / 2)
        print(f"{bucket}: {bar:<50} {count:>3} ({percentage:>5.1f}%)")
    
    # Recomendações
    print(f"\n6. RECOMENDAÇÕES")
    print("-" * 80)
    
    if verified / total > 0.8:
        print("✓ Excelente taxa de confirmação (>80%)")
        print("  - Os bugs detectados são altamente confiáveis")
    elif verified / total > 0.6:
        print("~ Boa taxa de confirmação (60-80%)")
        print("  - Revisar os bugs não confirmados")
    else:
        print("! Taxa baixa de confirmação (<60%)")
        print("  - Ajustar threshold de similaridade")
        print("  - Revisar padrões com baixa taxa")
    
    # Salvar relatório em arquivo
    report_text = generate_report_text(results, patterns_stats, confidence_buckets)
    
    with open('outputs/relatorio_llm.md', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\n{'='*80}")
    print("[OK] Relatório salvo em: outputs/relatorio_llm.md")
    print(f"{'='*80}\n")

def generate_report_text(results, patterns_stats, confidence_buckets):
    """Gera texto completo do relatório em Markdown."""
    
    total = len(results)
    verified = sum(1 for r in results if r.get('llm_classification', {}).get('eh_realmente_bug'))
    not_verified = total - verified
    
    report = f"""# RELATÓRIO DE DETECÇÃO DE BUGS COM LLAMA 2

## Data e Hora
{datetime.now().strftime('%d de %B de %Y às %H:%M:%S')}

## Resumo Executivo

| Métrica | Valor |
|---------|-------|
| Total de bugs analisados | {total} |
| Bugs confirmados pela IA | {verified} ({verified/total*100:.1f}%) |
| Bugs não confirmados | {not_verified} ({not_verified/total*100:.1f}%) |
| Taxa de confirmação | {verified/total*100:.1f}% |

## Análise por Padrão de Bug

| Padrão | Total | Confirmados | Taxa | Score Médio |
|--------|-------|-------------|------|-------------|
"""
    
    for pattern in sorted(patterns_stats.keys()):
        stats = patterns_stats[pattern]
        total_p = stats['total']
        verified_p = stats['verified']
        taxa = verified_p / total_p * 100 if total_p > 0 else 0
        avg_score = stats['avg_score']
        
        report += f"| {pattern} | {total_p} | {verified_p} | {taxa:.1f}% | {avg_score:.4f} |\n"
    
    # Top 10 bugs
    report += "\n## Top 10 Bugs Mais Confiáveis\n\n"
    
    sorted_results = sorted(
        results,
        key=lambda x: x.get('llm_classification', {}).get('confianca', 0),
        reverse=True
    )
    
    for idx, result in enumerate(sorted_results[:10], 1):
        pattern = result.get('match', {}).get('pattern_name', '?')
        classname = result.get('class', '?')
        method = result.get('method', '?')
        conf = result.get('llm_classification', {}).get('confianca', 0)
        motivo = result.get('llm_classification', {}).get('motivo', 'N/A')
        
        report += f"""### {idx}. {pattern}
- **Classe**: {classname}
- **Método**: {method}
- **Confiança**: {conf:.2%}
- **Motivo**: {motivo}

"""
    
    # Distribuição de confiança
    report += "\n## Distribuição de Confiança\n\n"
    
    for bucket, count in sorted(confidence_buckets.items()):
        percentage = count / total * 100
        report += f"- **{bucket}**: {count} bugs ({percentage:.1f}%)\n"
    
    # Conclusões
    report += "\n## Conclusões\n\n"
    
    if verified / total > 0.8:
        report += "✓ **Excelente**: Taxa de confirmação acima de 80%\n\n"
        report += "Os bugs detectados são altamente confiáveis. Recomenda-se investir em correção.\n"
    elif verified / total > 0.6:
        report += "~ **Bom**: Taxa de confirmação entre 60-80%\n\n"
        report += "A maioria dos bugs foi confirmada. Revisar os casos não confirmados.\n"
    else:
        report += "! **Revisar**: Taxa de confirmação abaixo de 60%\n\n"
        report += "Considere ajustar os thresholds ou padrões de detecção.\n"
    
    report += f"\n---\n*Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n"
    
    return report

if __name__ == '__main__':
    generate_report()
