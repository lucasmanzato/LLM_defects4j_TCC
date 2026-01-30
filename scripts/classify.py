"""
Script para classificar bugs detectados usando LLaMA via Ollama.
Processa os 50 bugs encontrados e adiciona classificação IA.
"""
import os
import json
import sys

os.environ['OLLAMA_HOST'] = 'http://localhost:11434'

try:
    import ollama
except ImportError:
    print("[ERRO] Biblioteca ollama não instalada. Execute: pip install ollama")
    sys.exit(1)


def classify_bug_with_llama(snippet: str, pattern_name: str, class_name: str) -> dict:
    """Classifica um bug detectado usando LLaMA."""
    try:
        prompt = f"""Você é um especialista em detecção de bugs em Java. Analise este código da classe {class_name} e confirme se realmente contém o bug "{pattern_name}".

Código:
```java
{snippet[:300]}
```

Padrão procurado: {pattern_name}

Responda APENAS em JSON:
{{
    "is_real_bug": true or false,
    "confidence": número entre 0.0 e 1.0,
    "reason": breve explicação
}}"""
        
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            stream=False,
            options={
                'num_predict': 200,  # Limite de tokens para resposta rápida
                'temperature': 0.3   # Menos criatividade, mais determinístico
            }
        )
        
        text = response.get('response', '').strip()
        
        # Remover blocos de código markdown se presentes
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        # Tentar extrair JSON
        import json
        import re
        
        # Procurar JSON entre chaves
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                result = json.loads(json_str)
                # Validar estrutura
                if 'is_real_bug' in result and 'confidence' in result and 'reason' in result:
                    # Mapear nomes de campos
                    return {
                        'eh_bug_real': result.get('is_real_bug', False),
                        'confianca': float(result.get('confidence', 0)),
                        'motivo': str(result.get('reason', 'N/A'))
                    }
            except:
                pass
        
        # Se não conseguir fazer parse perfeito, tente extrair informações
        is_bug = 'sim' in text.lower() or 'verdadeiro' in text.lower() or 'bug' in text.lower() or 'yes' in text.lower() or 'true' in text.lower()
        
        # Tentar extrair confiança (procurar números)
        conf_match = re.search(r'(\d+\.?\d*)\s*(?:%|confidence|confiança)', text.lower())
        confidence = float(conf_match.group(1)) / 100 if conf_match else 0.5
        
        return {
            'eh_bug_real': is_bug,
            'confianca': min(1.0, max(0.0, confidence)),
            'motivo': text[:100] if text else 'Resposta LLaMA'
        }
            
    except Exception as e:
        print(f"[ERRO] Classificação: {e}")
        return None


def main():
    results_path = 'outputs/results.json'
    
    if not os.path.exists(results_path):
        print(f"[ERRO] Arquivo {results_path} não encontrado")
        return
    
    print("\n" + "="*60)
    print(" CLASSIFICAÇÃO COM LLAMA")
    print("="*60)
    
    # Carregar resultados
    with open(results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"\n[INFO] Carregados {len(results)} bugs")
    print("[INFO] Classificando com LLaMA... (pode levar ~30-50 minutos)")
    
    # Classificar cada bug
    for idx, result in enumerate(results, 1):
        snippet = result.get('snippet', '')
        pattern = result.get('match', {}).get('pattern_name', '')
        class_name = result.get('class', '')
        
        if snippet and pattern:
            print(f"\n[{idx}/{len(results)}] {class_name} - {pattern}...", end=" ", flush=True)
            
            classification = classify_bug_with_llama(snippet, pattern, class_name)
            
            if classification:
                result['llm_classification'] = classification
                is_real = classification.get('eh_bug_real', False)
                confidence = classification.get('confianca', 0)
                
                status = "BUG CONFIRMADO" if is_real else "NÃO É UM BUG"
                print(f"[{status}] (conf: {confidence:.2f})")
            else:
                result['llm_classification'] = None
                print("[ERRO]")
    
    # Salvar resultados atualizados
    output_path = 'outputs/results_with_llm.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print(f"[OK] Resultados salvos em: {output_path}")
    print("="*60 + "\n")
    
    # Gerar relatório
    print("[INFO] Gerando relatório...")
    try:
        from report_markdown import generate_report
        generate_report()
    except ImportError:
        print("[AVISO] Não foi possível gerar relatório. Execute: python report_markdown.py")


if __name__ == '__main__':
    main()
