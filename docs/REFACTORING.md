# Refatoração do Código - Estrutura Modular

## 📊 Antes vs Depois

### Antes (Estrutura Monolítica)
```
LLM_defects4j_TCC/
├── data_acquisition.py          # Tudo junto
├── bug_filter_llm.py             # Heurísticas misturadas
├── defects4j_patterns.py         # Padrões
├── structural_matcher.py         # Matching
├── similarity_pipeline.py        # Pipeline
├── export_csv.py                 # Utilitários
├── run_filter.py                 # Runner
├── test_gemini.py                # Testes temporários
└── test_new_sdk.py               # Testes temporários
```

### Depois (Estrutura Modular)
```
LLM_defects4j_TCC/
├── src/
│   ├── extractors/               # 📥 Extração de dados
│   │   ├── java_parser.py        #   - Parser de métodos Java
│   │   └── feature_extractor.py  #   - Extração de features
│   ├── matchers/                 # 🎯 Lógica de matching
│   │   ├── pattern_library.py    #   - Biblioteca de padrões
│   │   ├── signature_generator.py #   - Gerador de assinaturas
│   │   └── similarity_matcher.py  #   - Cálculo de similaridade
│   ├── pipelines/                # 🔄 Orquestração
│   │   └── detection_pipeline.py  #   - Pipeline completo
│   └── utils/                    # 🛠️ Utilitários
│       └── repo_cloner.py        #   - Clonagem de repositórios
├── dados/                        # 📁 Dados
├── outputs/                      # 📊 Resultados
├── docs/                         # 📖 Documentação
└── main.py                       # 🚀 Entry point
```

## ✨ Melhorias Implementadas

### 1. Separação de Responsabilidades
**Antes**: Código misturado em arquivos grandes  
**Depois**: Cada módulo com responsabilidade única

#### Extractors (src/extractors/)
- `java_parser.py`: Parsing de código Java
  - Classe `JavaMethodExtractor`
  - AST parsing com javalang
  - Fallback para regex
  
- `feature_extractor.py`: Extração de features estruturais
  - Features AST (contagem de nós)
  - Token sequences
  - Control flow
  - Method calls
  - Operators
  - Complexity metrics

#### Matchers (src/matchers/)
- `pattern_library.py`: Definição de padrões Defects4J
  - 6 padrões de bugs documentados
  - Estrutura dataclass para type safety
  
- `signature_generator.py`: Geração de assinaturas
  - Converte padrões em assinaturas estruturais
  - Exporta para JSON
  
- `similarity_matcher.py`: Cálculo de similaridade
  - Multi-dimensional matching
  - 5 métricas diferentes (cosine, jaccard, LCS)
  - Pesos configuráveis

#### Pipelines (src/pipelines/)
- `detection_pipeline.py`: Orquestração completa
  - 5 passos bem definidos
  - Execução paralela onde possível
  - Export para JSON + CSV integrado

#### Utils (src/utils/)
- `repo_cloner.py`: Clonagem de repositórios
  - Validação de repositórios Java
  - Instalação automática de dependências

### 2. Imports Absolutos
**Antes**: Imports relativos problemáticos  
**Depois**: Imports absolutos a partir de `src/`

```python
# Antes (com erros)
from ..extractors.feature_extractor import FeatureExtractor

# Depois (limpo)
from extractors.feature_extractor import FeatureExtractor
```

### 3. Type Hints e Documentação
**Antes**: Pouca documentação  
**Depois**: Docstrings completos e type hints

```python
def step2_extract_methods(self) -> List[Dict[str, Any]]:
    """
    Extract all methods from Java source files.
    
    Returns:
        List of method dictionaries with code, name, class, file
    """
```

### 4. Estrutura de Pacotes Python
**Antes**: Arquivos soltos  
**Depois**: Pacotes Python adequados com `__init__.py`

```
src/
├── __init__.py
├── extractors/
│   └── __init__.py
├── matchers/
│   └── __init__.py
├── pipelines/
│   └── __init__.py
└── utils/
    └── __init__.py
```

### 5. CSV Export Integrado
**Antes**: Script separado `export_csv.py`  
**Depois**: Integrado no pipeline principal

```python
# Agora em detection_pipeline.py
def _export_to_csv(self, results: List[Dict], csv_path: str):
    """Export results to CSV format."""
    # Gera CSV automaticamente junto com JSON
```

### 6. Entry Point Limpo
**Antes**: Múltiplos runners (`run_filter.py`, etc)  
**Depois**: Único `main.py` bem estruturado

```python
# main.py - simples e direto
def main():
    load_dotenv()
    pipeline = BugDetectionPipeline(repo_url, repo_path)
    results = pipeline.run(threshold, top_k, output_path)
    print(f"✓ Found {len(results)} potential bugs")
```

### 7. Organização de Outputs
**Antes**: Arquivos misturados na raiz  
**Depois**: Estrutura organizada

```
outputs/
├── defects4j_signatures.json  # Assinaturas geradas
├── results.json               # Resultados JSON
└── results.csv                # Resultados CSV

docs/
├── ARQUITETURA_SIMILARIDADE.md  # Arquitetura técnica
└── REFACTORING.md                # Este documento
```

## 📋 Arquivos Removidos

Arquivos obsoletos removidos para manter clareza:

1. `bug_filter_llm.py` → Refatorado para `matchers/`
2. `data_acquisition.py` → Refatorado para `utils/repo_cloner.py`
3. `defects4j_patterns.py` → Refatorado para `matchers/pattern_library.py`
4. `structural_matcher.py` → Refatorado para `matchers/similarity_matcher.py`
5. `similarity_pipeline.py` → Refatorado para `pipelines/detection_pipeline.py`
6. `export_csv.py` → Integrado no pipeline
7. `export_similarity_csv.py` → Integrado no pipeline
8. `run_filter.py` → Substituído por `main.py`
9. `test_gemini.py` → Testes temporários
10. `test_new_sdk.py` → Testes temporários

## 🎯 Benefícios da Refatoração

### Manutenibilidade
- ✅ Código mais fácil de entender
- ✅ Mudanças localizadas em módulos específicos
- ✅ Testes unitários facilitados

### Escalabilidade
- ✅ Novos extractors podem ser adicionados facilmente
- ✅ Novos padrões em `pattern_library.py`
- ✅ Novos matchers podem ser implementados

### Qualidade
- ✅ Type hints para IDEs e linters
- ✅ Docstrings completos
- ✅ Estrutura de pacotes Python adequada

### Usabilidade
- ✅ Entry point único e simples
- ✅ Outputs organizados
- ✅ CSV export automático

## 🚀 Como Usar

```bash
# Simples e direto
python main.py
```

## 📚 Próximos Passos Sugeridos

1. **Testes Unitários**
   ```
   tests/
   ├── test_extractors.py
   ├── test_matchers.py
   └── test_pipelines.py
   ```

2. **Configuração Avançada**
   - Adicionar CLI com argparse
   - Perfis de configuração (.env.dev, .env.prod)

3. **Otimizações**
   - Cache de assinaturas
   - Paralelização de feature extraction
   - Batch processing

4. **Documentação**
   - Sphinx para API docs
   - Exemplos de uso
   - Tutoriais

## ✅ Checklist de Qualidade

- [x] Código organizado em módulos
- [x] Separação de responsabilidades
- [x] Type hints
- [x] Docstrings
- [x] Estrutura de pacotes Python
- [x] Imports limpos
- [x] Entry point único
- [x] Outputs organizados
- [x] README atualizado
- [x] Documentação técnica
