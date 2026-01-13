"""
Similarity-based pattern matcher.
Compares code features against pattern signatures.
"""
import json
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Match:
    """Represents a pattern match with similarity score."""
    pattern_id: str
    pattern_name: str
    similarity_score: float
    confidence: float
    feature_breakdown: Dict[str, float]


class SimilarityMatcher:
    """
    Matches code against pattern signatures using multi-dimensional similarity.
    
    Metrics:
        - Cosine similarity for AST features (35%)
        - Jaccard similarity for control flow (25%)
        - Jaccard similarity for method calls (20%)
        - Jaccard similarity for operators (10%)
        - Sequence similarity for tokens (10%)
    """
    
    # Weights for each similarity component
    WEIGHTS = {
        'ast': 0.35,
        'control_flow': 0.25,
        'methods': 0.20,
        'operators': 0.10,
        'tokens': 0.10
    }
    
    def __init__(self, signatures_path: str):
        """Load pattern signatures from JSON."""
        with open(signatures_path, 'r', encoding='utf-8') as f:
            self.signatures = json.load(f)
        print(f"✓ Loaded signatures for {len(self.signatures)} patterns")
    
    def cosine_similarity(self, vec1: Dict, vec2: Dict) -> float:
        """Cosine similarity between feature vectors."""
        all_keys = set(vec1.keys()) | set(vec2.keys())
        if not all_keys:
            return 0.0
        
        dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in all_keys)
        mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)
    
    def jaccard_similarity(self, set1: set, set2: set) -> float:
        """Jaccard similarity between sets."""
        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    def sequence_similarity(self, seq1: List, seq2: List) -> float:
        """LCS-based sequence similarity."""
        if not seq1 or not seq2:
            return 0.0
        
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        lcs_length = dp[m][n]
        return lcs_length / max(m, n)
    
    def calculate_similarity(self, features: Dict, signature: Dict) -> Tuple[float, Dict]:
        """Calculate weighted similarity score."""
        scores = {}
        
        # AST features (cosine)
        ast_sim = self.cosine_similarity(
            features.get('ast_features', {}),
            signature.get('ast_features', {})
        )
        scores['ast'] = ast_sim * self.WEIGHTS['ast']
        
        # Control flow (Jaccard)
        cf_sim = self.jaccard_similarity(
            set(features.get('control_flow', [])),
            set(signature.get('control_flow', []))
        )
        scores['control_flow'] = cf_sim * self.WEIGHTS['control_flow']
        
        # Method calls (Jaccard)
        method_sim = self.jaccard_similarity(
            set(features.get('method_calls', [])),
            set(signature.get('method_calls', []))
        )
        scores['methods'] = method_sim * self.WEIGHTS['methods']
        
        # Operators (Jaccard)
        op_sim = self.jaccard_similarity(
            set(features.get('operators', [])),
            set(signature.get('operators', []))
        )
        scores['operators'] = op_sim * self.WEIGHTS['operators']
        
        # Tokens (sequence)
        token_sim = self.sequence_similarity(
            features.get('token_sequence', [])[:30],
            signature.get('token_sequence', [])[:30]
        )
        scores['tokens'] = token_sim * self.WEIGHTS['tokens']
        
        total_score = sum(scores.values())
        return total_score, scores
    
    def match(self, features: Dict, threshold: float = 0.3) -> List[Match]:
        """Match features against all pattern signatures."""
        matches = []
        
        for pattern_id, pattern_sigs in self.signatures.items():
            best_score = 0.0
            best_breakdown = {}
            
            # Test against all signatures of this pattern
            for signature in pattern_sigs:
                score, breakdown = self.calculate_similarity(features, signature)
                if score > best_score:
                    best_score = score
                    best_breakdown = breakdown
            
            # Add match if above threshold
            if best_score >= threshold:
                active_features = sum(1 for v in best_breakdown.values() if v > 0.01)
                confidence = min((best_score + active_features * 0.05) / 1.25, 1.0)
                
                matches.append(Match(
                    pattern_id=pattern_id,
                    pattern_name=pattern_sigs[0].get('pattern_name', pattern_id),
                    similarity_score=best_score,
                    confidence=confidence,
                    feature_breakdown=best_breakdown
                ))
        
        # Sort by score descending
        matches.sort(key=lambda x: x.similarity_score, reverse=True)
        return matches


if __name__ == '__main__':
    # Test
    matcher = SimilarityMatcher('defects4j_signatures.json')
    test_features = {
        'ast_features': {'IfStatement': 1},
        'control_flow': ['if'],
        'method_calls': ['equals'],
        'operators': ['=='],
        'token_sequence': ['if', 'str', '==', 'null']
    }
    matches = matcher.match(test_features, threshold=0.2)
    for m in matches:
        print(f"{m.pattern_id}: {m.similarity_score:.2f}")
