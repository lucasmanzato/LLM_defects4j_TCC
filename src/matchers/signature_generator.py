"""
Gerador de assinatura de padrões.
Cria assinaturas estruturais de exemplos de padrões de bugs.
"""
import json
import os
from typing import Dict, List
from dataclasses import dataclass, asdict

from extractors.feature_extractor import FeatureExtractor
from matchers.pattern_library import Defects4JPatterns


@dataclass
class PatternSignature:
    """Assinatura estrutural de um padrão de bug."""
    pattern_id: str
    pattern_name: str
    ast_features: Dict[str, int]
    token_sequence: List[str]
    control_flow: List[str]
    method_calls: List[str]
    operators: List[str]
    complexity_score: float
    
    def to_dict(self):
        return asdict(self)


class SignatureGenerator:
    """Gera assinaturas estruturais de exemplos de padrões."""
    
    def __init__(self):
        self.patterns = Defects4JPatterns.get_all_patterns()
        self.feature_extractor = FeatureExtractor()
    
    def generate_signature(self, pattern_id: str, example_code: str) -> PatternSignature:
        """Gera assinatura a partir do código de exemplo."""
        pattern = self.patterns[pattern_id]
        features = self.feature_extractor.extract_all_features(example_code)
        
        return PatternSignature(
            pattern_id=pattern_id,
            pattern_name=pattern.name,
            ast_features=features['ast_features'],
            token_sequence=features['token_sequence'],
            control_flow=features['control_flow'],
            method_calls=features['method_calls'],
            operators=features['operators'],
            complexity_score=features['complexity_score']
        )
    
    def build_signature_library(self) -> Dict[str, List[PatternSignature]]:
        """Constrói biblioteca completa de assinaturas de todos os padrões."""
        library = {}
        
        for pattern_id, pattern in self.patterns.items():
            signatures = []
            for example in pattern.examples:
                sig = self.generate_signature(pattern_id, example)
                signatures.append(sig)
            library[pattern_id] = signatures
        
        return library
    
    def save_signatures(self, output_path: str):
        """Salva assinaturas para JSON."""
        library = self.build_signature_library()

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        data = {
            pattern_id: [sig.to_dict() for sig in sigs]
            for pattern_id, sigs in library.items()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Salvas {len(library)} assinaturas de padrões em {output_path}")
        return output_path


if __name__ == '__main__':
    generator = SignatureGenerator()
    generator.save_signatures('defects4j_signatures.json')
