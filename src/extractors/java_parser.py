"""
Analisador de código Java e extrator de métodos.
Usa javalang para análise AST com alternativa regex.
"""
import os
import re
from typing import List, Dict, Any
from pathlib import Path

try:
    import javalang
    JAVALANG_AVAILABLE = True
except ImportError:
    JAVALANG_AVAILABLE = False
    print("Aviso: javalang não disponível, usando alternativa regex")


class JavaMethodExtractor:
    """Extrai métodos de arquivos de código-fonte Java."""
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
    
    def extract_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extrai métodos de um único arquivo Java.
        
        Retorna:
            Lista de dicionários com chaves: file, class, name, code
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            return []
        
        if JAVALANG_AVAILABLE:
            return self._extract_with_javalang(file_path, content)
        else:
            return self._extract_with_regex(file_path, content)
    
    def _extract_with_javalang(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Extrai usando analisador AST."""
        methods = []
        try:
            tree = javalang.parse.parse(content)
            for path, node in tree.filter(javalang.tree.MethodDeclaration):
                # Obter nome da classe
                class_name = None
                for p in path:
                    if isinstance(p, javalang.tree.ClassDeclaration):
                        class_name = p.name
                        break
                
                # Extrair código do método (aproximação)
                start_pos = node.position.line if node.position else 0
                lines = content.split('\n')
                method_code = self._extract_method_body(lines, start_pos - 1)
                
                methods.append({
                    'file': file_path,
                    'class': class_name,
                    'name': node.name,
                    'code': method_code
                })
        except Exception:
            # Alternativa para regex em caso de erro de análise
            return self._extract_with_regex(file_path, content)
        
        return methods
    
    def _extract_with_regex(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Extrai usando padrões regex."""
        methods = []
        
        # Padrão para declaração de método
        pattern = r'(public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}'
        
        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            method_name = match.group(2)
            method_code = match.group(0)
            
            methods.append({
                'file': file_path,
                'class': None,  # Difícil de extrair confiável com regex
                'name': method_name,
                'code': method_code
            })
        
        return methods
    
    def _extract_method_body(self, lines: List[str], start_line: int) -> str:
        """Extrai corpo do método contando chaves."""
        if start_line >= len(lines):
            return ""
        
        brace_count = 0
        method_lines = []
        started = False
        
        for i in range(start_line, len(lines)):
            line = lines[i]
            method_lines.append(line)
            
            for char in line:
                if char == '{':
                    brace_count += 1
                    started = True
                elif char == '}':
                    brace_count -= 1
                    if started and brace_count == 0:
                        return '\n'.join(method_lines)
        
        return '\n'.join(method_lines)
    
    def extract_from_directory(self) -> List[Dict[str, Any]]:
        """Extract methods from all Java files in directory."""
        all_methods = []
        java_files = list(Path(self.root_dir).rglob('*.java'))
        
        for java_file in java_files:
            methods = self.extract_from_file(str(java_file))
            all_methods.extend(methods)
        
        return all_methods


if __name__ == '__main__':
    # Test
    extractor = JavaMethodExtractor('dados/commons-lang')
    methods = extractor.extract_from_directory()
    print(f"Extracted {len(methods)} methods")
