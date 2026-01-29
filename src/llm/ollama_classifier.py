"""
Classificador de bugs usando LLaMA via Ollama (versão corrigida).
"""
import os
import json
from typing import Dict, Any, Optional


class OllamaClassifier:
    """
    Classifica snippets de código Java usando LLaMA via Ollama.
    """
    
    def __init__(self, model: str = "llama2", host: str = "http://localhost:11434"):
        """
        Inicializa o classificador Ollama.
        
        Args:
            model: Modelo LLaMA a usar (default: llama2)
            host: URL do servidor Ollama (default: localhost:11434)
        """
        self.model = model
        self.host = host
        self.client = None
        self.is_available = False
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa cliente Ollama com verificação de disponibilidade."""
        try:
            import ollama
            
            # Tentar conectar ao servidor Ollama
            try:
                # Verificar se o servidor está rodando
                os.environ['OLLAMA_HOST'] = self.host
                response = ollama.list()
                self.client = ollama
                self.is_available = True
                print(f"[OK] Ollama conectado: {self.host}")
                print(f"     Modelo: {self.model}")
            except Exception as e:
                print(f"[AVISO] Ollama nao disponivel: {e}")
                print(f"        Inicie com: ollama serve")
                self.is_available = False
                
        except ImportError:
            print("[AVISO] Biblioteca 'ollama' nao instalada")
            print("        Execute: pip install ollama")
            self.is_available = False
    
    def classify_snippet(self, snippet: str, pattern_name: str) -> Optional[Dict[str, Any]]:
        """
        Classifica um snippet de código usando LLaMA.
        
        Args:
            snippet: Código Java a classificar
            pattern_name: Nome do padrão detectado
            
        Returns:
            Dicionário com classificação ou None se falhar
        """
        if not self.is_available or not self.client:
            return None
        
        try:
            prompt = f"""Voce eh um expert em detectar bugs em Java. Analise este codigo e confirme se realmente contem o padrao "{pattern_name}".

Codigo:
```java
{snippet[:500]}
```

Responda APENAS em JSON:
{{
    "eh_realmente_bug": true/false,
    "confianca": 0.0-1.0,
    "motivo": "explicacao breve"
}}"""
            
            print(f"   [IA] Classificando: {pattern_name}...", end=" ", flush=True)
            
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False
            )
            
            # Extrair resposta
            text = response.get('response', '').strip()
            
            # Tentar parsear JSON
            try:
                result = json.loads(text)
                confianca = result.get('confianca', 0)
                print(f"[OK] Classificado (confianca: {confianca:.2f})")
                return result
            except json.JSONDecodeError:
                print(f"[AVISO] Resposta invalida")
                return None
                
        except Exception as e:
            print(f"[ERRO] Erro na classificacao: {e}")
            return None
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde da conexão com Ollama."""
        return {
            'available': self.is_available,
            'model': self.model,
            'host': self.host,
            'status': 'OK' if self.is_available else 'Offline'
        }
