"""
Script para setup e teste do Ollama/LLaMA
"""
import subprocess
import sys
import os

def install_ollama():
    """Instala Ollama se não estiver presente."""
    print("📥 Instalando dependência ollama...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ollama"])
    print("✓ Ollama instalado")

def check_ollama_server():
    """Verifica se servidor Ollama está rodando."""
    try:
        import ollama
        print("🔍 Verificando servidor Ollama...")
        
        try:
            response = ollama.list(host="http://localhost:11434")
            print("✓ Servidor Ollama respondendo!")
            return True
        except Exception as e:
            print(f"❌ Servidor Ollama não respondendo: {e}")
            print("\n📋 Para iniciar Ollama, abra um terminal e execute:")
            print("   ollama serve")
            return False
            
    except ImportError:
        print("⚠️  Biblioteca ollama não instalada")
        return False

def pull_llama_model():
    """Baixa modelo LLaMA se não estiver presente."""
    try:
        import ollama
        print("\n📥 Verificando modelo LLaMA...")
        
        try:
            response = ollama.list(host="http://localhost:11434")
            models = [m.get('name') for m in response.get('models', [])]
            
            if 'llama2:latest' in models or any('llama2' in m for m in models):
                print("✓ LLaMA 2 já está instalado")
                return True
            else:
                print("⬇️  Baixando LLaMA 2 (pode demorar alguns minutos)...")
                print("   Tamanho: ~3.8 GB")
                
                response = ollama.pull("llama2", host="http://localhost:11434")
                print("✓ LLaMA 2 baixado com sucesso!")
                return True
                
        except Exception as e:
            print(f"❌ Erro ao gerenciar modelos: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_llama():
    """Testa geração de texto com LLaMA."""
    try:
        import ollama
        print("\n🧪 Testando LLaMA...")
        
        response = ollama.generate(
            model="llama2",
            prompt="Responda com uma só palavra: OK",
            host="http://localhost:11434"
        )
        
        result = response.get('response', '').strip()
        print(f"✓ Resposta LLaMA: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    print("="*60)
    print(" SETUP OLLAMA/LLAMA2")
    print("="*60)
    
    # Passo 1: Instalar ollama
    try:
        import ollama
        print("✓ Biblioteca ollama já instalada")
    except ImportError:
        install_ollama()
    
    # Passo 2: Verificar servidor
    print()
    if not check_ollama_server():
        print("\n⚠️  Inicie o servidor Ollama antes de continuar")
        return False
    
    # Passo 3: Baixar modelo
    print()
    if not pull_llama_model():
        print("\n⚠️  Erro ao baixar modelo")
        return False
    
    # Passo 4: Testar
    print()
    if not test_llama():
        print("\n⚠️  Erro no teste de geração")
        return False
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETO!")
    print("="*60)
    print("\n📝 Para usar Ollama no pipeline:")
    print("   1. Edite .env e altere: OLLAMA_ENABLED=true")
    print("   2. Execute: python main.py")
    print("\n💡 Para manter Ollama rodando em background:")
    print("   - Linux/Mac: ollama serve &")
    print("   - Windows: Abra novo terminal com 'ollama serve'")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
