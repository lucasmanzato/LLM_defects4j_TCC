# Nova Arquitetura: Matching por Similaridade Estrutural

## Visão Geral
Sistema redesenhado para detectar bugs usando **similaridade estrutural** com padrões conhecidos do Defects4J, em vez de regex heurístico.

## Fluxo do Pipeline

### 1. Setup Paralelo (Passo 1)
Executa simultaneamente:
- **Thread 1**: Clonagem do repositório Java
- **Thread 2**: Geração de assinaturas estruturais dos padrões Defects4J

### 2. Extração de Métodos (Passo 2)
- Parseia todos os `.java` do repositório clonado
- Extrai métodos usando `javalang` (AST parser)
- Fallback para regex quando AST falha

### 3. Computação de Features (Passo 3)
Para cada método, extrai:
- **AST Features**: Contagem de nós (IfStatement, ForStatement, MethodInvocation, etc)
- **Token Sequence**: Sequência de identificadores, keywords e operadores
- **Control Flow**: Estruturas de controle (if, for, while, try, catch)
- **Method Calls**: Métodos invocados (`.equals()`, `.toString()`, etc)
- **Operators**: Operadores usados (==, !=, &&, ||, etc)
- **Complexity Score**: Complexidade ciclomática aproximada

### 4. Matching por Similaridade (Passo 4)
Calcula similaridade multi-dimensional:
- **Cosine Similarity** para AST features (35% do score)
- **Jaccard Similarity** para control flow (25%)
- **Jaccard Similarity** para method calls (20%)
- **Jaccard Similarity** para operators (10%)
- **LCS (Longest Common Subsequence)** para tokens (10%)

Threshold configurável (padrão: 0.3)

### 5. Ranking e Filtragem (Passo 5)
- Ordena por score de similaridade
- Retorna top-K resultados (padrão: 50)

## Componentes Implementados

### `defects4j_patterns.py`
- **Classe**: `Defects4JPatternExtractor`
- **Função**: Extrai padrões estruturais de exemplos conhecidos
- **Padrões suportados**:
  - `null-dereference`: Acesso sem null check
  - `boundary-error`: Off-by-one
  - `string-equality-operator`: String == em vez de .equals()
  - `empty-exception-handler`: Catch vazio
  - `resource-leak`: Recursos não fechados
  - `missing-null-check`: Falta verificação antes de equals()

### `structural_matcher.py`
- **Classe**: `StructuralMatcher`
- **Função**: Calcula similaridade entre código e assinaturas
- **Métricas**:
  - Cosine similarity (vetores de features)
  - Jaccard similarity (conjuntos)
  - LCS (sequências)

### `similarity_pipeline.py`
- **Classe**: `SimilarityBasedPipeline`
- **Função**: Orquestra todo o fluxo
- **Execução paralela**: Setup em threads simultâneas

## Vantagens sobre Regex Heurístico

1. **Mais Robusto**: Não depende de padrões textuais exatos
2. **Flexível**: Captura variações de código que expressam o mesmo padrão
3. **Graduado**: Score de similaridade em vez de match binário
4. **Interpretável**: Breakdown de quais features contribuíram
5. **Escalável**: Fácil adicionar novos padrões (basta exemplos)

## Configuração (.env)

```
REPO_URL=https://github.com/apache/commons-lang.git
REPO_PATH=dados/commons-lang
OUT_PATH=dados/similarity_results.json
SIMILARITY_THRESHOLD=0.3
TOP_K=50
```

## Execução

```bash
python similarity_pipeline.py
```

## Output

JSON com estrutura:
```json
[
  {
    "file": "path/to/File.java",
    "class": "ClassName",
    "name": "methodName",
    "pattern_match": {
      "pattern_id": "null-dereference",
      "pattern_name": "Acesso a referência nula sem verificação",
      "score": 0.67,
      "confidence": 0.72,
      "matched_features": {
        "ast": 0.24,
        "control_flow": 0.15,
        "methods": 0.18,
        "operators": 0.06,
        "tokens": 0.04
      }
    },
    "all_patterns": [...],
    "snippet": "código do método..."
  }
]
```

## Próximos Passos

1. **Calibração**: Ajustar pesos das métricas baseado em validação
2. **Expansão**: Adicionar mais padrões do Defects4J
3. **LLM Híbrido**: Usar Gemini para refinar top matches
4. **Validação**: Comparar com bugs reais do Defects4J
