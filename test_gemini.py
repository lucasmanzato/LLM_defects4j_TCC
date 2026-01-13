import os
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.environ.get('GEMINI_API_KEY')
print(f"✓ GEMINI_API_KEY loaded: {bool(api_key)}")
if api_key:
    print(f"  Key starts with: {api_key[:20]}...")

try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Simple test prompt
    response = model.generate_content(
        'Return valid JSON with field "test": "ok"',
        generation_config={"temperature": 0.2}
    )
    print("✓ Gemini API works!")
    print(f"  Response: {response.text[:100]}")
except Exception as e:
    print(f"✗ Gemini API error: {e}")
