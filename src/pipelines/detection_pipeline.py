"""
Pipeline principal de detecção de bugs usando correspondência de similaridade.
Orquestra: clonar → extrair → encontrar → classificar
"""
import os
import json
import csv
import concurrent.futures
from typing import List, Dict, Any
from pathlib import Path

from utils.repo_cloner import clonar_repositorio_java
from extractors.java_parser import JavaMethodExtractor
from extractors.feature_extractor import FeatureExtractor
from matchers.signature_generator import SignatureGenerator
from matchers.similarity_matcher import SimilarityMatcher


class BugDetectionPipeline:
    """
    Pipeline de ponta a ponta para detectar bugs usando similaridade estrutural.
    
    Passos:
        1. Clonar repositório + Gerar assinaturas (paralelo)
        2. Extrair métodos de arquivos Java
        3. Calcular características estruturais
        4. Encontrar correspondências contra assinaturas de padrões
        5. Classificar e filtrar resultados
    """
    
    def __init__(self, repo_url: str, repo_path: str, signatures_path: str = 'outputs/defects4j_signatures.json'):
        self.repo_url = repo_url
        self.repo_path = repo_path
        self.signatures_path = signatures_path
        self.feature_extractor = FeatureExtractor()
        self.matcher = None
    
    def step1_setup(self) -> tuple:
        """Passo 1: Clonar repo + Gerar assinaturas em paralelo."""
        print("\n" + "="*60)
        print("STEP 1: Setup (Parallel)")
        print("="*60)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_clone = executor.submit(self._clone_repository)
            future_sigs = executor.submit(self._generate_signatures)
            
            clone_result = future_clone.result()
            sig_result = future_sigs.result()
        
        print(f"✓ Clone: {clone_result}")
        print(f"✓ Signatures: {sig_result}")
        return clone_result, sig_result
    
    def _clone_repository(self) -> str:
        """Clona repositório Java."""
        success = clonar_repositorio_java(self.repo_url, self.repo_path)
        return "Success" if success else "Failed"
    
    def _generate_signatures(self) -> str:
        """Gera assinaturas de padrões."""
        generator = SignatureGenerator()
        generator.save_signatures(self.signatures_path)
        return f"Saved to {self.signatures_path}"
    
    def step2_extract_methods(self) -> List[Dict]:
        """Passo 2: Extrair métodos de arquivos Java."""
        print("\n" + "="*60)
        print("STEP 2: Method Extraction")
        print("="*60)
        
        extractor = JavaMethodExtractor(self.repo_path)
        methods = extractor.extract_from_directory()
        
        print(f"✓ Extraídos {len(methods)} métodos")
        return methods
    
    def step3_compute_features(self, methods: List[Dict]) -> List[Dict]:
        """Passo 3: Calcular características estruturais para cada método."""
        print("\n" + "="*60)
        print("STEP 3: Feature Computation")
        print("="*60)
        
        methods_with_features = []
        for method in methods:
            code = method.get('code', '')
            if not code:
                continue
            
            features = self.feature_extractor.extract_all_features(code)
            method['features'] = features
            methods_with_features.append(method)
        
        print(f"✓ Características calculadas para {len(methods_with_features)} métodos")
        return methods_with_features
    
    def step4_match_patterns(self, methods: List[Dict], threshold: float = 0.3) -> List[Dict]:
        """Passo 4: Encontrar correspondências contra assinaturas de padrões."""
        print("\n" + "="*60)
        print(f"PASSO 4: Correspondência de Padrões (limiar={threshold})")
        print("="*60)
        
        self.matcher = SimilarityMatcher(self.signatures_path)
        
        matched_methods = []
        for method in methods:
            features = method.get('features')
            if not features:
                continue
            
            matches = self.matcher.match(features, threshold)
            
            if matches:
                best_match = matches[0]
                method['match'] = {
                    'pattern_id': best_match.pattern_id,
                    'pattern_name': best_match.pattern_name,
                    'score': best_match.similarity_score,
                    'confidence': best_match.confidence,
                    'breakdown': best_match.feature_breakdown
                }
                method['all_matches'] = [
                    {
                        'pattern_id': m.pattern_id,
                        'score': m.similarity_score,
                        'confidence': m.confidence
                    }
                    for m in matches
                ]
                matched_methods.append(method)
        
        print(f"✓ Encontrados {len(matched_methods)} métodos com correspondências de padrão")
        return matched_methods
    
    def step5_rank_and_filter(self, matches: List[Dict], top_k: int = 50) -> List[Dict]:
        """Passo 5: Classificar por similaridade e selecionar top-K."""
        print("\n" + "="*60)
        print(f"PASSO 5: Classificação & Filtragem (top-{top_k})")
        print("="*60)
        
        ranked = sorted(
            matches,
            key=lambda x: x.get('match', {}).get('score', 0),
            reverse=True
        )
        
        top_results = ranked[:top_k]
        print(f"✓ Selecionados top-{len(top_results)} resultados")
        return top_results
    
    def run(self, threshold: float = 0.3, top_k: int = 50, output_path: str = 'outputs/results.json'):
        """Executa pipeline completo."""
        print("\n" + "="*60)
        print(" PIPELINE DE DETECÇÃO DE BUGS - Correspondência Baseada em Similaridade")
        print("="*60)
        
        # Executar passos
        self.step1_setup()
        methods = self.step2_extract_methods()
        methods_with_features = self.step3_compute_features(methods)
        matches = self.step4_match_patterns(methods_with_features, threshold)
        top_results = self.step5_rank_and_filter(matches, top_k)
        
        # Salvar resultados (JSON + CSV)
        self._save_results(top_results, output_path)
        self._export_to_csv(top_results, output_path.replace('.json', '.csv'))
        
        print("\n" + "="*60)
        print(f"✓ Pipeline concluído.")
        print(f"  JSON: {output_path}")
        print(f"  CSV: {output_path.replace('.json', '.csv')}")
        print("="*60 + "\n")
        
        return top_results
    
    def _save_results(self, results: List[Dict], output_path: str):
        """Salva resultados em JSON."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        clean_results = []
        for r in results:
            clean = {
                'file': r.get('file'),
                'class': r.get('class'),
                'method': r.get('name'),
                'match': r.get('match'),
                'all_matches': r.get('all_matches', []),
                'snippet': r.get('code', '')[:500]  # Visualização prévia
            }
            clean_results.append(clean)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clean_results, f, indent=2, ensure_ascii=False)
    
    def _export_to_csv(self, results: List[Dict], csv_path: str):
        """Exporta resultados em formato CSV."""
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            
            # Cabeçalho
            writer.writerow([
                'rank',
                'file',
                'class',
                'method',
                'pattern_id',
                'pattern_name',
                'similarity_score',
                'confidence',
                'ast_score',
                'control_flow_score',
                'methods_score',
                'operators_score',
                'tokens_score',
                'snippet_preview'
            ])
            
            # Dados
            for idx, result in enumerate(results, 1):
                match = result.get('match', {})
                breakdown = match.get('breakdown', {})
                snippet = result.get('snippet', '')[:200]  # Visualização prévia
                
                writer.writerow([
                    idx,
                    result.get('file', ''),
                    result.get('class', ''),
                    result.get('method', ''),
                    match.get('pattern_id', ''),
                    match.get('pattern_name', ''),
                    f"{match.get('score', 0):.4f}",
                    f"{match.get('confidence', 0):.4f}",
                    f"{breakdown.get('ast', 0):.4f}",
                    f"{breakdown.get('control_flow', 0):.4f}",
                    f"{breakdown.get('methods', 0):.4f}",
                    f"{breakdown.get('operators', 0):.4f}",
                    f"{breakdown.get('tokens', 0):.4f}",
                    snippet
                ])


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    
    repo_url = os.environ.get('REPO_URL', 'https://github.com/apache/commons-lang.git')
    repo_path = os.environ.get('REPO_PATH', 'dados/commons-lang')
    threshold = float(os.environ.get('SIMILARITY_THRESHOLD', '0.3'))
    top_k = int(os.environ.get('TOP_K', '50'))
    
    pipeline = BugDetectionPipeline(repo_url, repo_path)
    pipeline.run(threshold=threshold, top_k=top_k)
