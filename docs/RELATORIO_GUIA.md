# 📊 Guia de Relatórios - LLaMA 2 Classification

## 🎯 Visão Geral

Após a execução da classificação com LLaMA 2, o sistema gera **3 tipos de relatórios** com diferentes níveis de detalhe e apresentação:

```
├── 📄 relatorio_llm.md          (Relatório em Markdown)
├── 🌐 relatorio_visual.html     (Relatório visual com gráficos)
└── 📊 results_with_llm.json     (Dados brutos em JSON)
```

---

## 1️⃣ RELATÓRIO MARKDOWN (`relatorio_llm.md`)

### O que é?
Relatório estruturado em formato Markdown, fácil de:
- Compartilhar via email, Slack, GitHub
- Editar e customizar
- Incluir em documentação
- Visualizar em qualquer editor de texto

### Como acessar?
```bash
# No VS Code:
code outputs/relatorio_llm.md

# Ou abrir em editor de texto comum
```

### Conteúdo incluído:
- ✅ Resumo executivo com estatísticas principais
- ✅ Análise por padrão de bug
- ✅ Top 10 bugs mais confiáveis
- ✅ Bugs não confirmados
- ✅ Distribuição de confiança
- ✅ Recomendações

### Exemplo de seção:
```markdown
## Análise por Padrão de Bug

| Padrão | Total | Confirmados | Taxa | Score Médio |
|--------|-------|-------------|------|-------------|
| Resource Leak | 23 | 18 | 78.3% | 0.9205 |
| Missing Null Check | 26 | 21 | 80.8% | 0.9151 |
```

---

## 2️⃣ RELATÓRIO VISUAL (`relatorio_visual.html`)

### O que é?
Relatório interativo com gráficos visuais (Charts.js):
- 📊 Gráficos de barras e pizza
- 📈 Estatísticas em cards
- 🎨 Design moderno e responsivo
- 🖱️ Interativo no navegador

### Como acessar?
```bash
# No Windows:
start outputs/relatorio_visual.html

# No Linux:
xdg-open outputs/relatorio_visual.html

# No macOS:
open outputs/relatorio_visual.html

# Ou arrastar para o navegador
```

### Visualizações incluídas:

#### 📊 Cards de Resumo
- Total de bugs analisados
- Bugs confirmados (com %)
- Bugs não confirmados
- Confiança média

#### 📈 Gráfico de Padrões
- Barras mostrando confirmados vs não confirmados
- Comparação entre tipos de bugs
- Score médio por padrão

#### 🎯 Distribuição de Confiança
- Gráfico pizza com buckets (0-20%, 20-40%, etc.)
- Porcentagem de bugs em cada nível de confiança

#### ⭐ Top 10 Bugs
- Tabela com detalhes
- Status (BUG / NÃO É BUG)
- Confiança individual

---

## 3️⃣ DADOS BRUTOS (`results_with_llm.json`)

### O que é?
Arquivo JSON completo com:
- Código original detectado
- Similaridade estrutural
- Classificação LLaMA 2
- Confiança e motivo

### Estrutura:
```json
[
  {
    "file": "caminho/do/arquivo.java",
    "class": "NomeDaClasse",
    "method": "nomeDoMetodo",
    "match": {
      "pattern_name": "Resource Leak",
      "score": 0.9286,
      "confidence": 0.9429
    },
    "snippet": "codigo do metodo...",
    "llm_classification": {
      "eh_bug_real": true,
      "confianca": 0.85,
      "motivo": "Stream não fechado..."
    }
  },
  // ... mais 49 bugs
]
```

### Como usar?
```python
import json

with open('outputs/results_with_llm.json') as f:
    results = json.load(f)

# Filtrar apenas bugs confirmados
confirmed = [r for r in results if r['llm_classification']['eh_bug_real']]
print(f"Bugs confirmados: {len(confirmed)}/{len(results)}")

# Agrupar por padrão
from collections import defaultdict
by_pattern = defaultdict(list)
for r in results:
    pattern = r['match']['pattern_name']
    by_pattern[pattern].append(r)
```

---

## 📊 Interpretando os Resultados

### Taxa de Confirmação
- **80-100%**: ✅ Excelente - Padrão muito confiável
- **60-80%**: 🟢 Bom - Revisar alguns casos
- **40-60%**: 🟡 Médio - Necessário ajuste
- **0-40%**: 🔴 Baixo - Revisar threshold

### Confiança (por bug)
- **90-100%**: Confiança muito alta
- **70-89%**: Confiança boa
- **50-69%**: Confiança moderada
- **<50%**: Confiança baixa

### Score de Similaridade
Quanto maior, melhor:
- **>0.90**: Muito similar ao padrão
- **0.80-0.90**: Similar ao padrão
- **0.70-0.80**: Moderadamente similar
- **<0.70**: Pouco similar

---

## 🚀 Fluxo de Trabalho Recomendado

```
1. Gerar Classificação
   └─ python classify_with_llama.py (30-50 min)

2. Visualizar Relatório
   └─ Abrir relatorio_visual.html no navegador

3. Revisar Top 10
   └─ Verificar bugs mais confiáveis primeiro

4. Analisar por Padrão
   └─ Focar em padrões com alta taxa de confirmação

5. Exportar Dados
   └─ Usar results_with_llm.json para ferramentas

6. Tomar Ação
   └─ Corrigir bugs ou ajustar thresholds
```

---

## 🔧 Gerar Relatórios Manualmente

Se precisar regenerar os relatórios:

```bash
# Apenas Markdown
python generate_report.py

# Apenas HTML
python generate_html_report.py

# Ambos
python run_full_pipeline.py
```

---

## 📈 Casos de Uso

### Para Desenvolvimento
- Revisar code smell e padrões problemáticos
- Priorizar refatoração
- Melhorar qualidade de código

### Para Segurança
- Identificar resource leaks
- Detectar null dereferences
- Encontrar vulnerabilidades

### Para Gerenciamento
- Relatório executivo (Markdown)
- Visualizações para stakeholders (HTML)
- Dados para BI (JSON)

---

## 💾 Arquivos Gerados

```
outputs/
├── results.json                  (50 bugs detectados)
├── results_with_llm.json        (50 bugs + classificação LLM)
├── relatorio_llm.md             (Markdown)
├── relatorio_visual.html        (HTML com gráficos)
├── defects4j_signatures.json    (Padrões usados)
└── results.csv                  (Formato tabular)
```

---

## ⚠️ Troubleshooting

### Relatório vazio/incompleto?
```bash
# Verificar se classificação terminou
python monitor_classification.py

# Regenerar após conclusão
python generate_report.py
python generate_html_report.py
```

### JSON inválido?
```bash
# Validar arquivo
python -c "import json; json.load(open('outputs/results_with_llm.json'))"
```

### Gráficos não aparecem no HTML?
- Verifique conexão com internet (CDN do Chart.js)
- Ou use arquivo HTML offline (instalar Chart.js localmente)

---

## 📞 Próximos Passos

1. ✅ **Agora**: Revisar relatórios gerados
2. 📝 **Depois**: Documentar achados
3. 🐛 **Ação**: Criar issues/tickets para bugs
4. 🔄 **Validar**: Testar correções
5. 📊 **Medir**: Acompanhar impacto

---

**Última atualização**: Relatórios gerados com LLaMA 2 e Ollama
