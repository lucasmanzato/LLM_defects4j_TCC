# 📖 Documentação

Documentação técnica e guias do sistema de detecção de bugs com LLM.

## 📚 Índice

### Guias Principais
- [Arquitetura do Sistema](ARQUITETURA_SIMILARIDADE.md) - Como funciona a detecção
- [Setup do Ollama/LLaMA](OLLAMA_SETUP.md) - Configuração da IA

## 🗂️ Estrutura da Documentação

```
docs/
├── README.md                          (Este arquivo)
├── ARQUITETURA_SIMILARIDADE.md        (Arquitetura do sistema)
└── OLLAMA_SETUP.md                    (Configuração Ollama/LLaMA)
```

## 🎯 Por Onde Começar

1. **README.md** (root) - Visão geral e quick start
2. **ARQUITETURA_SIMILARIDADE.md** - Entender como o sistema funciona
3. **OLLAMA_SETUP.md** - Configurar a IA (LLaMA)
4. **RELATORIO_GUIA.md** - Interpretar os resultados

## 📊 Arquivos de Saída

O sistema gera explicações detalhadas em `outputs/`:
- `ExplicacaoOutput.txt` - Sobre defects4j_signatures.json
- `ExplicacaoResultsJSON.txt` - Sobre results.json
- `ExplicacaoResultsWithLLM.txt` - Sobre results_with_llm.json
- `ExplicacaoResultsCSV.txt` - Sobre results.csv

## 🚀 Execução Rápida

```bash
# 1. Configurar ambiente Python
python -m venv .venv
.venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar .env (ver exemplo abaixo)

# 4. Executar pipeline de detecção
python scripts/pipeline.py

# 5. Classificar com LLM (opcional)
python scripts/classify.py

# 6. Gerar relatórios
python scripts/report_markdown.py
```

## ⚙️ Configuração .env

```env
# Ollama/LLaMA Configuration
OLLAMA_ENABLED=true
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
OLLAMA_TIMEOUT=120
OLLAMA_RETRIES=2

# Pipeline Configuration
REPO_URL=https://github.com/rjust/defects4j.git
REPO_PATH=dados/defects4j
OUTPUT_PATH=outputs/results.json
SIMILARITY_THRESHOLD=0.3
TOP_K=50
```

## 🔗 Links Úteis

- [Scripts](../scripts/) - Scripts de execução
- [Código Fonte](../src/) - Módulos do sistema
- [Outputs](../outputs/) - Resultados e explicações
