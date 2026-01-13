# Detecção de Bugs em Java usando Similaridade Estrutural

Sistema de detecção de bugs baseado em padrões do Defects4J usando matching por similaridade estrutural.

## 📋 Estrutura do Projeto

```
LLM_defects4j_TCC/
├── src/                      # Código fonte
│   ├── extractors/           # Extração de código e features
│   │   ├── java_parser.py    # Parser de métodos Java
│   │   └── feature_extractor.py  # Extração de features estruturais
│   ├── matchers/             # Lógica de matching
│   │   ├── pattern_library.py    # Biblioteca de padrões Defects4J
│   │   ├── signature_generator.py # Gerador de assinaturas
│   │   └── similarity_matcher.py  # Matcher por similaridade
│   ├── pipelines/            # Pipelines de execução
│   │   └── detection_pipeline.py  # Pipeline completo
│   └── utils/                # Utilitários
│       └── repo_cloner.py    # Clonagem de repositórios
├── dados/                    # Repositórios clonados
├── outputs/                  # Resultados da análise
├── docs/                     # Documentação adicional
├── main.py                   # Ponto de entrada principal
├── requirements.txt          # Dependências Python
└── .env                      # Configurações
```

## 🚀 Início Rápido

### 1. Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração

Edite o arquivo `.env`:

```env
REPO_URL=https://github.com/apache/commons-lang.git
REPO_PATH=dados/commons-lang
OUTPUT_PATH=outputs/results.json
SIMILARITY_THRESHOLD=0.3
TOP_K=50
```

### 3. Execução

```bash
python main.py
```

## 📊 Como Funciona

### Pipeline de 5 Passos

**PASSO 1: Setup Paralelo**
- Thread 1: Clona repositório Java
- Thread 2: Gera assinaturas dos padrões Defects4J

**PASSO 2: Extração de Métodos**
- Parseia arquivos `.java` usando AST (javalang)
- Extrai métodos individuais

**PASSO 3: Computação de Features**
Para cada método, extrai:
- AST features (contagem de nós)
- Token sequence (identificadores, keywords)
- Control flow (if, for, while, try/catch)
- Method calls (métodos invocados)
- Operators (==, !=, &&, etc)
- Complexity score (ciclomática)

**PASSO 4: Matching por Similaridade**
Calcula similaridade multi-dimensional:
- Cosine similarity para AST (35%)
- Jaccard similarity para control flow (25%)
- Jaccard similarity para method calls (20%)
- Jaccard similarity para operators (10%)
- LCS para token sequence (10%)

**PASSO 5: Ranking e Filtragem**
- Ordena por score de similaridade
- Retorna top-K resultados

## 🎯 Padrões Detectados

1. **Null Dereference**: Acesso sem verificação de null
2. **Boundary Error**: Off-by-one em arrays/loops
3. **String Equality**: Uso de == ao invés de .equals()
4. **Empty Exception**: Catch vazio que engole exceções
5. **Resource Leak**: Recursos não fechados
6. **Missing Null Check**: Falta de verificação antes de equals()

## 📄 Output

### JSON (`outputs/results.json`)
```json
{
  "file": "path/File.java",
  "class": "ClassName",
  "method": "methodName",
  "match": {
    "pattern_id": "null-dereference",
    "pattern_name": "Null Dereference",
    "score": 0.67,
    "confidence": 0.72,
    "breakdown": {...}
  },
  "snippet": "código..."
}
```

### CSV (`outputs/results.csv`)
Planilha com colunas: rank, file, class, method, pattern_id, similarity_score, confidence, breakdown de métricas.

## ⚙️ Configurações Avançadas

### Ajustar Threshold
Altere `SIMILARITY_THRESHOLD` no `.env` (padrão: 0.3)
- Valores mais baixos: mais resultados, menos precisos
- Valores mais altos: menos resultados, mais precisos

### Ajustar Pesos das Métricas
Edite `src/matchers/similarity_matcher.py`:
```python
WEIGHTS = {
    'ast': 0.35,
    'control_flow': 0.25,
    'methods': 0.20,
    'operators': 0.10,
    'tokens': 0.10
}
```

## 🛠 Desenvolvimento

### Adicionar Novo Padrão
1. Edite `src/matchers/pattern_library.py`
2. Adicione ao dicionário `PATTERNS`
3. Forneça exemplos de código

### Estrutura Modular
- **Extractors**: Lógica de parsing e extração
- **Matchers**: Algoritmos de matching
- **Pipelines**: Orquestração de steps
- **Utils**: Funções auxiliares

## 📚 Documentação Adicional

- [ARQUITETURA_SIMILARIDADE.md](ARQUITETURA_SIMILARIDADE.md): Detalhes técnicos
- [CHANGELOG.md](CHANGELOG.md): Histórico de versões
- [TROUBLESHOOTING.txt](TROUBLESHOOTING.txt): Resolução de problemas

## 🤝 Contribuindo

Mantenha o código limpo e organizado:
- Use type hints
- Docstrings em funções públicas
- Separe responsabilidades por módulos
- Testes em `tests/` (quando criados)

## 📝 Licença

MIT License - Projeto acadêmico TCC

## 👤 Autor

Lucas Manzato - TCC 2026
