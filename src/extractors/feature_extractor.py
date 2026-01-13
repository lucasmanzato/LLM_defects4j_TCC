"""
Feature extraction from Java code for pattern matching.
Computes structural signatures from source code.
"""
import re
from typing import Dict, List
from collections import Counter

try:
    import javalang
    JAVALANG_AVAILABLE = True
except ImportError:
    JAVALANG_AVAILABLE = False


class FeatureExtractor:
    """Extracts structural features from Java code."""
    
    @staticmethod
    def extract_all_features(code: str) -> Dict:
        """
        Extract complete feature set from code.
        
        Returns:
            Dict with keys: ast_features, token_sequence, control_flow,
                          method_calls, operators, complexity_score
        """
        if not code:
            return {
                'ast_features': {},
                'token_sequence': [],
                'control_flow': [],
                'method_calls': [],
                'operators': [],
                'complexity_score': 0.0
            }
        
        return {
            'ast_features': FeatureExtractor.extract_ast_features(code),
            'token_sequence': FeatureExtractor.extract_tokens(code),
            'control_flow': FeatureExtractor.extract_control_flow(code),
            'method_calls': FeatureExtractor.extract_method_calls(code),
            'operators': FeatureExtractor.extract_operators(code),
            'complexity_score': FeatureExtractor.calculate_complexity(code)
        }
    
    @staticmethod
    def extract_ast_features(code: str) -> Dict[str, int]:
        """Extract AST node counts."""
        features = Counter()
        
        if JAVALANG_AVAILABLE:
            try:
                tree = javalang.parse.parse(code)
                for path, node in tree:
                    features[type(node).__name__] += 1
                return dict(features)
            except:
                pass
        
        # Fallback: regex-based counting
        features['IfStatement'] = len(re.findall(r'\bif\s*\(', code))
        features['ForStatement'] = len(re.findall(r'\bfor\s*\(', code))
        features['WhileStatement'] = len(re.findall(r'\bwhile\s*\(', code))
        features['MethodInvocation'] = len(re.findall(r'\w+\s*\(', code))
        features['TryStatement'] = len(re.findall(r'\btry\s*\{', code))
        
        return dict(features)
    
    @staticmethod
    def extract_tokens(code: str) -> List[str]:
        """Extract token sequence (identifiers, keywords, operators)."""
        if JAVALANG_AVAILABLE:
            try:
                tokens = []
                for token in javalang.tokenizer.tokenize(code):
                    if isinstance(token, (javalang.tokenizer.Identifier,
                                        javalang.tokenizer.Keyword,
                                        javalang.tokenizer.Operator)):
                        tokens.append(str(token.value))
                return tokens[:50]  # Limit length
            except:
                pass
        
        # Fallback
        tokens = re.findall(r'\b\w+\b|[=!<>]+|[+\-*/]', code)
        return tokens[:50]
    
    @staticmethod
    def extract_control_flow(code: str) -> List[str]:
        """Extract control flow structures."""
        structures = []
        patterns = {
            'if': r'\bif\s*\(',
            'else': r'\belse\b',
            'for': r'\bfor\s*\(',
            'while': r'\bwhile\s*\(',
            'switch': r'\bswitch\s*\(',
            'try': r'\btry\s*\{',
            'catch': r'\bcatch\s*\(',
            'finally': r'\bfinally\s*\{'
        }
        
        for name, pattern in patterns.items():
            if re.search(pattern, code):
                structures.append(name)
        
        return structures
    
    @staticmethod
    def extract_method_calls(code: str) -> List[str]:
        """Extract method call names."""
        # Pattern: .methodName( or methodName(
        calls = re.findall(r'\.(\w+)\s*\(', code)
        calls += re.findall(r'^(\w+)\s*\(', code, re.MULTILINE)
        return list(set(calls))[:20]  # Unique, limited
    
    @staticmethod
    def extract_operators(code: str) -> List[str]:
        """Extract operators used."""
        operators = re.findall(r'(==|!=|<=|>=|<|>|&&|\|\||!|\+\+|--|=)', code)
        return list(set(operators))
    
    @staticmethod
    def calculate_complexity(code: str) -> float:
        """Calculate cyclomatic complexity (approximation)."""
        decision_points = len(re.findall(
            r'\b(if|for|while|case|\?|&&|\|\|)\b', code
        ))
        return 1.0 + decision_points


if __name__ == '__main__':
    # Test
    test_code = """
    public void test(String s) {
        if (s == null) {
            return;
        }
        for (int i = 0; i < s.length(); i++) {
            System.out.println(s);
        }
    }
    """
    features = FeatureExtractor.extract_all_features(test_code)
    print(features)
