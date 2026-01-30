"""
Cria um relatório de exemplo mostrando o que será gerado
"""

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                RELATÓRIO DE DETECÇÃO DE BUGS - LLaMA 2                        ║
║                                                                                ║
║  Status: ⏳ Processando... (Classificação em andamento)                        ║
╚════════════════════════════════════════════════════════════════════════════════╝

📊 RESUMO EXECUTIVO
───────────────────────────────────────────────────────────────────────────────

Total de métodos analisados:        9.683
Bugs detectados (similaridade):     50 (0,5%)
Padrões detectados:                 3
  • Resource Leak:                  23 bugs (46%)
  • Missing Null Check:             26 bugs (52%)
  • Null Dereference:               1 bug (2%)

Confiança média dos resultados:     92,37%
Taxa de confirmação esperada:       75-90%


📈 DADOS SENDO COLETADOS
───────────────────────────────────────────────────────────────────────────────

Cada bug passa por análise com LLaMA 2:
  ✓ Leitura do código-fonte
  ✓ Verificação de contexto
  ✓ Análise de padrão específico
  ✓ Cálculo de confiança
  ✓ Explicação do resultado

Tempo estimado: ~30-50 minutos (processamento paralelo possível)


🎯 PADRÕES DE BUG DETECTADOS
───────────────────────────────────────────────────────────────────────────────

1. RESOURCE LEAK
   - Descrição: Recurso (stream, conexão) não fechado
   - Score de similaridade: 0,9205
   - Bugs encontrados: 23

2. MISSING NULL CHECK  
   - Descrição: Acesso a variável sem verificação de null
   - Score de similaridade: 0,9151
   - Bugs encontrados: 26

3. NULL DEREFERENCE
   - Descrição: Desreferência de ponteiro nulo
   - Score de similaridade: 0,9200
   - Bugs encontrados: 1


📊 GRÁFICOS E VISUALIZAÇÕES
───────────────────────────────────────────────────────────────────────────────

Ao término, você terá acesso a:

  1. Gráfico de Taxa de Confirmação por Padrão
     └─ Mostra qual padrão tem maior taxa de confirmação

  2. Distribuição de Confiança
     └─ Histograma com buckets de 0-20%, 20-40%, etc.

  3. Top 10 Bugs Mais Confiáveis
     └─ Ranking com confiança e status

  4. Análise de Falsos Positivos
     └─ Bugs descartados pela IA e motivos


🗂️ ARQUIVOS DE SAÍDA
───────────────────────────────────────────────────────────────────────────────

✓ outputs/results_with_llm.json
  └─ Dados brutos com classificação LLM

✓ outputs/relatorio_llm.md
  └─ Relatório em Markdown (fácil leitura)

✓ outputs/relatorio_visual.html
  └─ Relatório visual com gráficos interativos

✓ outputs/results.csv
  └─ Dados em formato tabular


💡 COMO USAR OS RESULTADOS
───────────────────────────────────────────────────────────────────────────────

1. Abra outputs/relatorio_visual.html em seu navegador
   → Visualize gráficos interativos e estatísticas

2. Use outputs/relatorio_llm.md para compartilhar
   → Formato padrão Markdown
   
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
