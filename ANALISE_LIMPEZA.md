# 📋 ANÁLISE DE ARQUIVOS - RELATÓRIO DE LIMPEZA

## 🔍 ARQUIVOS PARA REMOVER

### Testes/Debug (Obsoletos)
- ❌ `test_gemini_api.py` - Teste da Gemini API (quota esgotada, não mais usado)
- ❌ `RELATORIO.txt` - Relatório antigo (duplicado em RELATORIO_GUIA.md)
- ❌ `TROUBLESHOOTING.txt` - Troubleshooting antigo (menos detalhado)
- ❌ `CHANGELOG.md` - Histórico antigo (usar git log)

### Setup (Uma execução)
- ❓ `setup_ollama.py` - Script one-time para setup Ollama (pode ser removido após uso)

## 📚 DOCUMENTAÇÃO PARA CONSOLIDAR

### Manter (Core)
- ✅ `README.md` - Documentação principal
- ✅ `RELATORIO_GUIA.md` - Guia de uso dos relatórios
- ✅ `LIMPEZA.md` - Documentação da limpeza

### Consolidar em /docs
- `IMPLEMENTACAO_RELATORIOS.md` → docs/IMPLEMENTACAO.md
- `SUMARIO_RELATORIOS.md` → docs/SUMARIO.md
- `docs/ARQUITETURA_SIMILARIDADE.md` (mantém)
- `docs/OLLAMA_SETUP.md` (mantém)
- `docs/REFACTORING.md` (mantém)

## 🐍 SCRIPTS PRINCIPAIS (Manter)

### Pipeline Principal
- ✅ `main.py` - Entry point para detecção de bugs

### Classificação com LLM
- ✅ `classify_with_llama.py` - Classificação com LLaMA 2
- ✅ `show_report_preview.py` - Preview dos relatórios

### Geração de Relatórios
- ✅ `generate_report.py` - Markdown
- ✅ `generate_html_report.py` - HTML com gráficos

### Monitoramento
- ✅ `monitor_classification.py` - Monitoramento em tempo real
- ✅ `wait_and_report.py` - Aguarda conclusão

### Orquestração
- ✅ `run_full_pipeline.py` - Pipeline completa

## 📦 SRC/ (Modular - Manter como está)

```
src/
├── extractors/
│   ├── java_parser.py ✅
│   └── feature_extractor.py ✅
├── matchers/
│   ├── pattern_library.py ✅
│   ├── signature_generator.py ✅
│   └── similarity_matcher.py ✅
├── pipelines/
│   └── detection_pipeline.py ✅
├── llm/
│   └── ollama_classifier.py ✅
├── utils/
│   └── repo_cloner.py ✅
└── __init__.py ✅
```

## 📁 ESTRUTURA PROPOSTA

```
LLM_defects4j_TCC/
├── README.md                         (Principal)
├── LIMPEZA.md                        (Documentação de limpeza)
├── .env                              (Configuração)
├── .gitignore                        (Git)
├── requirements.txt                  (Dependências)
│
├── scripts/                          (Scripts novos)
│   ├── pipeline.py                   (main.py renomeado)
│   ├── classify.py                   (classify_with_llama.py)
│   ├── report_preview.py             (show_report_preview.py)
│   ├── report_markdown.py            (generate_report.py)
│   ├── report_html.py                (generate_html_report.py)
│   ├── monitor.py                    (monitor_classification.py)
│   ├── wait_report.py                (wait_and_report.py)
│   └── run_all.py                    (run_full_pipeline.py)
│
├── src/                              (Módulos mantidos)
│   ├── extractors/
│   ├── matchers/
│   ├── pipelines/
│   ├── llm/
│   └── utils/
│
└── docs/                             (Documentação)
    ├── README.md                     (Índice de docs)
    ├── RELATORIO_GUIA.md             (Guia de relatórios)
    ├── ARQUITETURA_SIMILARIDADE.md
    ├── OLLAMA_SETUP.md
    ├── REFACTORING.md
    ├── SUMARIO.md                    (de SUMARIO_RELATORIOS.md)
    └── IMPLEMENTACAO.md              (de IMPLEMENTACAO_RELATORIOS.md)
```

## 🗑️ RESUMO DA LIMPEZA

### Remover (8 arquivos)
- test_gemini_api.py
- RELATORIO.txt
- TROUBLESHOOTING.txt
- CHANGELOG.md
- setup_ollama.py (opcional)

### Mover para scripts/
- main.py → scripts/pipeline.py
- classify_with_llama.py → scripts/classify.py
- show_report_preview.py → scripts/report_preview.py
- generate_report.py → scripts/report_markdown.py
- generate_html_report.py → scripts/report_html.py
- monitor_classification.py → scripts/monitor.py
- wait_and_report.py → scripts/wait_report.py
- run_full_pipeline.py → scripts/run_all.py

### Mover para docs/
- IMPLEMENTACAO_RELATORIOS.md → docs/IMPLEMENTACAO.md
- SUMARIO_RELATORIOS.md → docs/SUMARIO.md
- RELATORIO_GUIA.md → docs/RELATORIO_GUIA.md

### Manter no root
- README.md
- LIMPEZA.md
- .env
- requirements.txt
- .gitignore

## ✅ BENEFÍCIOS

1. **Organização clara** - Separação entre scripts, docs e código
2. **Sem duplicatas** - Um README por seção
3. **Mais limpo** - Remove arquivos obsoletos
4. **Manutenível** - Estrutura intuitiva
5. **Profissional** - Padrão de projeto bem conhecido
