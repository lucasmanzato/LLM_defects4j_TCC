import os
import json
from typing import Dict, Any, Optional

# Test google.genai SDK
try:
    from google import genai
    
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("GEMINI_API_KEY not set")
        exit(1)
    
    client = genai.Client(api_key=api_key)
    
    # Simple test
    prompt = "Return valid JSON with field test: 'ok'"
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt,
        config={'temperature': 0.2, 'response_mime_type': 'application/json'}
    )
    
    print("✓ google.genai SDK works!")
    print(f"Response: {response.text[:200]}")
    
    # Test with bug classification
    code_sample = '''
    public boolean equals(Object obj) {
        if (obj == this) return true;
        return obj.equals(this);
    }
    '''
    
    bug_prompt = (
        "You are a Java bug pattern classifier based on Defects4J themes. "
        "Given a Java method snippet, analyze likely bug patterns: null deref, boundary/off-by-one, incorrect conditionals, "
        "API misuse, resource leaks, exception swallowing, string equality with ==, equals/hashCode mismatch, concurrency hazards. "
        "Return a valid JSON with fields: bug_likelihood (0..1 float), labels (array of short identifiers), reason (short string), fix (a simple fix suggestion). "
        f"Code snippet:\n{code_sample}")
    
    response2 = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=bug_prompt,
        config={'temperature': 0.2, 'response_mime_type': 'application/json'}
    )
    
    result = json.loads(response2.text)
    print("\n✓ Bug classification works!")
    print(f"bug_likelihood: {result.get('bug_likelihood')}")
    print(f"labels: {result.get('labels')}")
    print(f"reason: {result.get('reason')}")
    print(f"fix: {result.get('fix')}")
    
except ImportError as e:
    print(f"✗ google.genai not installed: {e}")
    print("Run: pip install google-genai")
except Exception as e:
    print(f"✗ Error: {e}")
