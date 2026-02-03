# Integração com Ollama/LLaMA - Guia

## Status Atual

O sistema está funcionando 100% com **similaridade estrutural**. A integração com LLaMA (Ollama) pode ser adicionada como recurso opcional.

## Como Adicionar Ollama/LLaMA

### Passo 1: Instalar Ollama

Baixe em: https://ollama.ai

```bash
# Windows: execute o instalador
# Será instalado em C:\Users\<seu_user>\AppData\Local\Ollama
```

### Passo 2: Iniciar o Servidor

```bash
ollama serve
```

Vai ficar rodando em http://localhost:11434

### Passo 3: Baixar Modelo LLaMA

Em outro terminal:

```bash
ollama pull llama2
# Vai baixar ~3.8 GB
```

Ou modelos menores (mais rápidos):

```bash
ollama pull llama2:7b      # 3.8 GB (rápido)
ollama pull llama2:13b     # 7 GB (intermediário)  
ollama pull neural-chat    # 4.7 GB (otimizado para chat)
```

### Passo 4: Instalar Biblioteca Python

```bash
pip install ollama
```

### Passo 5: Ativar no .env

Edite `.env`:

```env
OLLAMA_ENABLED=true
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

### Passo 6: Executar

```bash
python scripts/pipeline.py
```

O sistema vai:
1. Detectar bugs por similaridade ✓
2. Pedir ao LLaMA para confirmar cada bug encontrado
3. Gerar score combinado (similaridade + IA)
4. Exibir mensagens quando IA atua [IA] ou tem erro [ERRO]

## Modelos Recomendados

| Modelo | Tamanho | RAM | Velocidade | Qualidade |
|--------|---------|-----|-----------|-----------|
| llama2:7b | 3.8GB | 4GB | Rápido | Boa |
| neural-chat | 4.7GB | 6GB | Rápido | Excelente |
| llama2:13b | 7GB | 8GB | Normal | Melhor |
| mistral | 4GB | 4GB | Muito rápido | Boa |

## Como Funciona a Integração

### Sem Ollama (Atual)

```
Arquivo Java → Extrator → Features → Similaridade → Score 0.93
```

### Com Ollama

```
Arquivo Java → Extrator → Features → Similaridade → Score 0.93
                                                        ↓
                                     Enviar para LLaMA: "É really um bug?"
                                                        ↓
                                     Resposta LLaMA: "Sim, 0.85 confiança"
                                                        ↓
                                     Score combinado: (0.93 + 0.85) / 2 = 0.89
```

## Mensagens Esperadas

```
[OK] Ollama conectado: http://localhost:11434
     Modelo: llama2
     
[IA] Classificando: Resource Leak... [OK] Classificado (confianca: 0.85)
[IA] Classificando: Null Dereference... [ERRO] Erro na classificacao: timeout
[AVISO] Resposta invalida
[AVISO] Ollama nao disponivel
```

## Troubleshooting

### "Ollama não disponível"
- Verifique se `ollama serve` está rodando
- Tente acessar http://localhost:11434 no navegador

### Erro de timeout
- LLaMA está lento
- Tente modelo menor: `ollama pull neural-chat`

### Erro de memória
- 4GB RAM mínimo
- Feche outros programas
- Use modelo menor (7b ao invés de 13b)

## Performance

Tempo estimado para 50 bugs:

| Modo | Tempo |
|------|-------|
| Apenas Similaridade | 2-3 min |
| + LLaMA (7b) | 30-50 min |
| + LLaMA (13b) | 1-2 horas |

Dica: Rode com top_k menor para testes!

```env
TOP_K=5
```

## Futuro

Planos para aprimorar integração:

- [ ] Cache de respostas LLM
- [ ] Processamento paralelo de classificações
- [ ] Fine-tuning de prompts
- [ ] Suporte para outros modelos (Mistral, Neural-Chat)
- [ ] API alternatives (Together.AI, Replicate)
