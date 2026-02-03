# 📚 Scripts

Todos os scripts principais do projeto.

## 🚀 Quick Start

```bash
# Execute a pipeline completa
python scripts/pipeline.py

# Classifique com LLaMA
python scripts/classify.py

# Gere relatórios
python scripts/report_markdown.py
```

## 📋 Scripts Disponíveis

### `pipeline.py`
**Função**: Detecção de bugs por similaridade estrutural
- Clona repositório
- Extrai features de Java
- Calcula similaridade
- Rankeia bugs

```bash
python scripts/pipeline.py
```

### `classify.py`
**Função**: Classificação com LLaMA 2
- Analisa bugs detectados
- Confirma se são reais
- Calcula confiança
- Gera motivos

```bash
python scripts/classify.py
```

### `report_markdown.py`
**Função**: Gera relatório em Markdown

```bash
python scripts/report_markdown.py
```

### `report_html.py`
**Função**: Gera relatório HTML interativo com gráficos

```bash
python scripts/report_html.py
```

### `monitor.py`
**Função**: Monitora progresso em tempo real

```bash
python scripts/monitor.py
```

## 📁 Estrutura

```
scripts/
├── pipeline.py           (Detecção)
├── classify.py           (LLaMA)
├── report_markdown.py    (MD)
├── report_html.py        (HTML)
└── monitor.py            (Monitor)
```

## 🔗 Referências

- [Documentação](../docs/)
- [Guia de Relatórios](../docs/RELATORIO_GUIA.md)
- [Arquitetura](../docs/ARQUITETURA_SIMILARIDADE.md)
