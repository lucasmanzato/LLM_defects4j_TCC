"""
Creates an example report showing what will be generated
"""

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                BUG DETECTION REPORT - LLaMA 2                                 ║
║                                                                                ║
║  Status: ⏳ Processing... (Classification in progress)                         ║
╚════════════════════════════════════════════════════════════════════════════════╝

📊 EXECUTIVE SUMMARY
───────────────────────────────────────────────────────────────────────────────

Total methods analyzed:         9.683
Bugs detected (similarity):     50 (0,5%)
Patterns detected:              3
  • Resource Leak:              23 bugs (46%)
  • Missing Null Check:         26 bugs (52%)
  • Null Dereference:           1 bug (2%)

Average confidence of results:  92,37%
Expected confirmation rate:     75-90%


📈 DATA BEING COLLECTED
───────────────────────────────────────────────────────────────────────────────

Each bug goes through analysis with LLaMA 2:
  ✓ Source code reading
  ✓ Context verification
  ✓ Specific pattern analysis
  ✓ Confidence calculation
  ✓ Result explanation

Estimated time: ~30-50 minutes (parallel processing possible)


🎯 DETECTED BUG PATTERNS
───────────────────────────────────────────────────────────────────────────────

1. RESOURCE LEAK
   - Description: Resource (stream, connection) not closed
   - Similarity score: 0,9205
   - Bugs found: 23

2. MISSING NULL CHECK  
   - Description: Variable access without null verification
   - Similarity score: 0,9151
   - Bugs found: 26

3. NULL DEREFERENCE
   - Description: Null pointer dereference
   - Similarity score: 0,9200
   - Bugs found: 1


📊 CHARTS AND VISUALIZATIONS
───────────────────────────────────────────────────────────────────────────────

Upon completion, you will have access to:

  1. Confirmation Rate Chart by Pattern
     └─ Shows which pattern has the highest confirmation rate

  2. Confidence Distribution
     └─ Histogram with buckets of 0-20%, 20-40%, etc.

  3. Top 10 Most Reliable Bugs
     └─ Ranking with confidence and status

  4. False Positive Analysis
     └─ Bugs discarded by AI and reasons


🗂️ OUTPUT FILES
───────────────────────────────────────────────────────────────────────────────

✓ outputs/results_with_llm.json
  └─ Raw data with LLM classification

✓ outputs/report_llm.md
  └─ Markdown report (easy to read)

✓ outputs/report_visual.html
  └─ Visual report with interactive charts

✓ outputs/results.csv
  └─ Data in tabular format


💡 HOW TO USE THE RESULTS
───────────────────────────────────────────────────────────────────────────────

1. Open outputs/report_visual.html in your browser
   → View interactive charts and statistics

2. Use outputs/report_llm.md to share
   → Standard Markdown format
   
3. Importe outputs/results_with_llm.json
   → Para análise programática ou em ferramentas

4. Revise outputs/results.csv
   → Para visualização em planilhas (Excel/Google Sheets)


⚙️ CONFIGURAÇÃO UTILIZADA
───────────────────────────────────────────────────────────────────────────────

Modelo LLM:           LLaMA 2 7B
Tempo por análise:    ~0.5-1 minuto
Temperatura:          0.3 (determinístico)
Max tokens:           200 (resposta rápida)

Similaridade:         6 Padrões Defects4J
Métricas:             Cosine, Jaccard, LCS
Score médio:          0,9151


📝 PRÓXIMOS PASSOS
───────────────────────────────────────────────────────────────────────────────

⏳ Aguardando conclusão da classificação LLaMA...

Você pode:
  • Monitorar progresso com: python monitor_classification.py
  • Visualizar resultados intermediários
  • Gerar relatórios preliminares
  • Preparar ações corretivas baseadas nos padrões


═════════════════════════════════════════════════════════════════════════════════

Este relatório será atualizado automaticamente quando a classificação terminar.
Tempo estimado: 30-50 minutos a partir do início do processamento.

═════════════════════════════════════════════════════════════════════════════════
""")
