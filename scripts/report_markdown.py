"""
Generates detailed report of classification with LLaMA
"""
import json
from datetime import datetime
from collections import defaultdict

def generate_report():
    """Generates report of results with LLM classification."""
    
    # Load results
    try:
        with open('outputs/results_with_llm.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("[ERROR] File results_with_llm.json not found")
        print("[INFO] Execute classify_with_llama.py first")
        return
    
    print("\n" + "="*80)
    print(" BUG DETECTION REPORT - LLAMA 2")
    print("="*80)
    
    # General statistics
    total = len(results)
    verified = sum(1 for r in results if r.get('llm_classification', {}).get('eh_realmente_bug'))
    not_verified = total - verified
    
    print(f"\n1. EXECUTIVE SUMMARY")
    print("-" * 80)
    print(f"Date/Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Total bugs analyzed: {total}")
    print(f"Bugs confirmed by AI: {verified} ({verified/total*100:.1f}%)")
    print(f"Bugs not confirmed: {not_verified} ({not_verified/total*100:.1f}%)")
    
    # Statistics by pattern
    patterns_stats = defaultdict(lambda: {'total': 0, 'verified': 0, 'avg_score': 0, 'scores': []})
    
    for result in results:
        pattern = result.get('match', {}).get('pattern_name', 'Unknown')
        is_verified = result.get('llm_classification', {}).get('eh_realmente_bug', False)
        score = result.get('match', {}).get('score', 0)
        
        patterns_stats[pattern]['total'] += 1
        if is_verified:
            patterns_stats[pattern]['verified'] += 1
        patterns_stats[pattern]['scores'].append(score)
    
    # Calculate average
    for pattern in patterns_stats:
        scores = patterns_stats[pattern]['scores']
        patterns_stats[pattern]['avg_score'] = sum(scores) / len(scores) if scores else 0
    
    print(f"\n2. ANALYSIS BY BUG PATTERN")
    print("-" * 80)
    print(f"{'Pattern':<35} {'Total':<8} {'Confirmed':<15} {'Rate':<10} {'Avg Score':<12}")
    print("-" * 80)
    
    for pattern in sorted(patterns_stats.keys()):
        stats = patterns_stats[pattern]
        total_p = stats['total']
        verified_p = stats['verified']
        taxa = verified_p / total_p * 100 if total_p > 0 else 0
        avg_score = stats['avg_score']
        
        print(f"{pattern:<35} {total_p:<8} {verified_p:<15} {taxa:>6.1f}%    {avg_score:>6.4f}")
    
    # Top 10 most reliable bugs
    print(f"\n3. TOP 10 MOST RELIABLE BUGS")
    print("-" * 80)
    
    sorted_results = sorted(
        results,
        key=lambda x: (
            x.get('llm_classification', {}).get('confianca', 0),
            x.get('match', {}).get('score', 0)
        ),
        reverse=True
    )
    
    print(f"{'#':<4} {'Pattern':<25} {'Class':<30} {'Confidence':<12} {'Score':<10}")
    print("-" * 80)
    
    for idx, result in enumerate(sorted_results[:10], 1):
        pattern = result.get('match', {}).get('pattern_name', '?')
        classname = result.get('class', '?')[:28]
        conf = result.get('llm_classification', {}).get('confianca', 0)
        score = result.get('match', {}).get('score', 0)
        
        print(f"{idx:<4} {pattern:<25} {classname:<30} {conf:>6.2%}      {score:>6.4f}")
    
    # Bugs not confirmed
    not_confirmed = [r for r in results if not r.get('llm_classification', {}).get('eh_realmente_bug')]
    
    print(f"\n4. BUGS NOT CONFIRMED BY AI ({len(not_confirmed)} cases)")
    print("-" * 80)
    print(f"{'#':<4} {'Pattern':<25} {'Class':<30} {'Reason':<20}")
    print("-" * 80)
    
    for idx, result in enumerate(not_confirmed[:5], 1):
        pattern = result.get('match', {}).get('pattern_name', '?')
        classname = result.get('class', '?')[:28]
        motivo = result.get('llm_classification', {}).get('motivo', '?')[:18]
        
        print(f"{idx:<4} {pattern:<25} {classname:<30} {motivo:<20}")
    
    if len(not_confirmed) > 5:
        print(f"... and {len(not_confirmed) - 5} more unconfirmed bugs")
    
    # Confidence distribution
    print(f"\n5. CONFIDENCE DISTRIBUTION")
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
    
    # Recommendations
    print(f"\n6. RECOMMENDATIONS")
    print("-" * 80)
    
    if verified / total > 0.8:
        print("✓ Excellent confirmation rate (>80%)")
        print("  - Detected bugs are highly reliable")
    elif verified / total > 0.6:
        print("~ Good confirmation rate (60-80%)")
        print("  - Review unconfirmed bugs")
    else:
        print("! Low confirmation rate (<60%)")
        print("  - Adjust similarity threshold")
        print("  - Review patterns with low rate")
    
    # Save report to file
    report_text = generate_report_text(results, patterns_stats, confidence_buckets)
    
    with open('outputs/report_llm.md', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\n{'='*80}")
    print("[OK] Report saved to: outputs/report_llm.md")
    print(f"{'='*80}\n")

def generate_report_text(results, patterns_stats, confidence_buckets):
    """Generates complete markdown report text."""
    
    total = len(results)
    verified = sum(1 for r in results if r.get('llm_classification', {}).get('eh_realmente_bug'))
    not_verified = total - verified
    
    report = f"""# BUG DETECTION REPORT WITH LLAMA 2

## Date and Time
{datetime.now().strftime('%d de %B de %Y às %H:%M:%S')}

## Executive Summary

| Metric | Value |
|--------|-------|
| Total bugs analyzed | {total} |
| Bugs confirmed by AI | {verified} ({verified/total*100:.1f}%) |
| Unconfirmed bugs | {not_verified} ({not_verified/total*100:.1f}%) |
| Confirmation rate | {verified/total*100:.1f}% |

## Analysis by Bug Pattern

| Pattern | Total | Confirmed | Rate | Avg Score |
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
    report += "\n## Top 10 Most Reliable Bugs\n\n"
    
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
- **Class**: {classname}
- **Method**: {method}
- **Confidence**: {conf:.2%}
- **Reason**: {motivo}

"""
    
    # Confidence distribution
    report += "\n## Confidence Distribution\n\n"
    
    for bucket, count in sorted(confidence_buckets.items()):
        percentage = count / total * 100
        report += f"- **{bucket}**: {count} bugs ({percentage:.1f}%)\n"
    
    # Conclusions
    report += "\n## Conclusions\n\n"
    
    if verified / total > 0.8:
        report += "✓ **Excellent**: Confirmation rate above 80%\n\n"
        report += "Detected bugs are highly reliable. Recommend investing in fixes.\n"
    elif verified / total > 0.6:
        report += "~ **Good**: Confirmation rate between 60-80%\n\n"
        report += "Most bugs were confirmed. Review unconfirmed cases.\n"
    else:
        report += "! **Review**: Confirmation rate below 60%\n\n"
        report += "Consider adjusting thresholds or detection patterns.\n"
    
    report += f"\n---\n*Report generated at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n"
    
    return report

if __name__ == '__main__':
    generate_report()
