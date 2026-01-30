"""
Biblioteca de padrões Defects4J.
Define padrões conhecidos de bugs do conjunto Defects4J.
"""
from typing import Dict, List
from dataclasses import dataclass, asdict
import json


@dataclass
class BugPattern:
    """Representa um padrão de bug conhecido."""
    pattern_id: str
    name: str
    description: str
    examples: List[str]
    
    def to_dict(self):
        return asdict(self)


class Defects4JPatterns:
    """Biblioteca de padrões conhecidos de bugs Defects4J."""
    
    PATTERNS = {
        'null-dereference': BugPattern(
            pattern_id='null-dereference',
            name='Null Dereference',
            description='Acesso a referência nula sem verificação prévia',
            examples=[
                'if (obj.method()) { }',
                'return obj.field;',
                'obj.equals(other)'
            ]
        ),
        'boundary-error': BugPattern(
            pattern_id='boundary-error',
            name='Boundary Error',
            description='Erro de limite (off-by-one) em arrays/loops',
            examples=[
                'for (int i = 0; i <= array.length; i++)',
                'if (index <= size)',
                'substring(0, str.length())'
            ]
        ),
        'string-equality-operator': BugPattern(
            pattern_id='string-equality-operator',
            name='String Equality with ==',
            description='Comparação de String com == ao invés de .equals()',
            examples=[
                'if (str1 == str2)',
                'str == "value"',
                'return s1 == s2'
            ]
        ),
        'empty-exception-handler': BugPattern(
            pattern_id='empty-exception-handler',
            name='Empty Exception Handler',
            description='Bloco catch vazio que engole exceções',
            examples=[
                'try { } catch (Exception e) { }',
                'catch (IOException ignored) { }'
            ]
        ),
        'resource-leak': BugPattern(
            pattern_id='resource-leak',
            name='Resource Leak',
            description='Recurso não fechado (sem try-with-resources)',
            examples=[
                'InputStream is = new FileInputStream(file);',
                'Connection conn = getConnection();'
            ]
        ),
        'missing-null-check': BugPattern(
            pattern_id='missing-null-check',
            name='Missing Null Check',
            description='Falta de verificação de null antes de operação',
            examples=[
                'if (obj.equals(other))',
                'obj.toString()',
                'value.equals(expected)'
            ]
        )
    }
    
    @classmethod
    def get_pattern(cls, pattern_id: str) -> BugPattern:
        """Get pattern by ID."""
        return cls.PATTERNS.get(pattern_id)
    
    @classmethod
    def get_all_patterns(cls) -> Dict[str, BugPattern]:
        """Get all patterns."""
        return cls.PATTERNS.copy()
    
    @classmethod
    def get_pattern_ids(cls) -> List[str]:
        """Get all pattern IDs."""
        return list(cls.PATTERNS.keys())
    
    @classmethod
    def save_to_json(cls, output_path: str):
        """Save patterns to JSON."""
        data = {
            pid: pattern.to_dict()
            for pid, pattern in cls.PATTERNS.items()
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    patterns = Defects4JPatterns.get_all_patterns()
    print(f"Loaded {len(patterns)} patterns:")
    for pid, pattern in patterns.items():
        print(f"  - {pattern.name}")
