"""
Script to classify detected bugs using LLaMA via Ollama.
Processes the 50 bugs found and adds AI classification.
"""
import os
import json
import sys

os.environ['OLLAMA_HOST'] = 'http://localhost:11434'

try:
    import ollama
except ImportError:
    print("[ERROR] ollama library not installed. Execute: pip install ollama")
    sys.exit(1)


def classify_bug_with_llama(snippet: str, pattern_name: str, class_name: str) -> dict:
    """Classifies a detected bug using LLaMA."""
    try:
        prompt = f"""You are an expert at detecting bugs in Java. Analyze this code from class {class_name} and confirm if it really contains the bug "{pattern_name}".

Code:
```java
{snippet[:300]}
```

Pattern searched: {pattern_name}

Respond ONLY in JSON:
{{
    "is_real_bug": true or false,
    "confidence": number between 0.0 and 1.0,
    "reason": brief explanation
}}"""
        
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            stream=False,
            options={
                'num_predict': 200,  # Token limit for fast response
                'temperature': 0.3   # Less creativity, more deterministic
            }
        )
        
        text = response.get('response', '').strip()
        
        # Remove markdown code blocks if present
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        # Try to extract JSON
        import json
        import re
        
        # Search for JSON between braces
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                result = json.loads(json_str)
                # Validate structure
                if 'is_real_bug' in result and 'confidence' in result and 'reason' in result:
                    # Map field names
                    return {
                        'eh_bug_real': result.get('is_real_bug', False),
                        'confianca': float(result.get('confidence', 0)),
                        'motivo': str(result.get('reason', 'N/A'))
                    }
            except:
                pass
        
        # If unable to parse perfectly, try to extract information
        is_bug = 'yes' in text.lower() or 'true' in text.lower() or 'bug' in text.lower()
        
        # Try to extract confidence (search for numbers)
        conf_match = re.search(r'(\d+\.?\d*)\s*(?:%|confidence)', text.lower())
        confidence = float(conf_match.group(1)) / 100 if conf_match else 0.5
        
        return {
            'eh_bug_real': is_bug,
            'confianca': min(1.0, max(0.0, confidence)),
            'motivo': text[:100] if text else 'LLaMA response'
        }
            
    except Exception as e:
        print(f"[ERROR] Classification: {e}")
        return None


def main():
    results_path = 'outputs/results.json'
    
    if not os.path.exists(results_path):
        print(f"[ERROR] File {results_path} not found")
        return
    
    print("\n" + "="*60)
    print(" CLASSIFICATION WITH LLAMA")
    print("="*60)
    
    # Load results
    with open(results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"\n[INFO] Loaded {len(results)} bugs")
    print("[INFO] Classifying with LLaMA... (may take ~30-50 minutes)")
    
    # Classify each bug
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
                
                status = "BUG CONFIRMED" if is_real else "NOT A BUG"
                print(f"[{status}] (conf: {confidence:.2f})")
            else:
                result['llm_classification'] = None
                print("[ERROR]")
    
    # Save updated results
    output_path = 'outputs/results_with_llm.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print(f"[OK] Results saved to: {output_path}")
    print("="*60 + "\n")
    
    # Generate report
    print("[INFO] Generating report...")
    try:
        from report_markdown import generate_report
        generate_report()
    except ImportError:
        print("[WARNING] Could not generate report. Execute: python report_markdown.py")


if __name__ == '__main__':
    main()
