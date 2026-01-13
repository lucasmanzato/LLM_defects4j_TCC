"""
Teste rápido da integração com Google Gemini API
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_api():
    """Testa se a API Gemini está funcionando."""
    api_key = os.environ.get('GEMINI_API_KEY')
    model = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')
    
    if not api_key:
        print("❌ GEMINI_API_KEY não encontrada no .env")
        return False
    
    print(f"✓ API Key encontrada: {api_key[:10]}...")
    print(f"✓ Modelo: {model}")
    
    try:
        from google import genai
        print("✓ Biblioteca google-genai importada")
        
        client = genai.Client(api_key=api_key)
        print("✓ Cliente Gemini inicializado")
        
        # Teste simples
        response = client.models.generate_content(
            model=model,
            contents="Responda apenas 'OK' se você está funcionando."
        )
        
        result = response.text.strip()
        print(f"✓ Resposta da API: {result}")
        print("\n🎉 A API Gemini está FUNCIONANDO!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao testar API: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("\n⚠️  Quota da API esgotada. A API existe mas está sem créditos.")
        elif "403" in str(e) or "API_KEY_INVALID" in str(e):
            print("\n⚠️  API Key inválida ou sem permissões.")
        
        return False

if __name__ == '__main__':
    print("="*60)
    print(" TESTE DE INTEGRAÇÃO - Google Gemini API")
    print("="*60)
    print()
    test_gemini_api()
