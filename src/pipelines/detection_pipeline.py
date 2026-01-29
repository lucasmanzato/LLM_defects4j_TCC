"""
Main bug detection pipeline using similarity matching.
Orchestrates: clone → extract → match → rank
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
    End-to-end pipeline for detecting bugs using structural similarity.
    
    Steps:
        1. Clone repository + Generate signatures (parallel)
        2. Extract methods from Java files
        3. Compute structural features
        4. Match against pattern signatures
        5. Rank and filter results
    """
    
    def __init__(self, repo_url: str, repo_path: str, signatures_path: str = 'outputs/defects4j_signatures.json'):
        self.repo_url = repo_url
        self.repo_path = repo_path
        self.signatures_path = signatures_path
        self.feature_extractor = FeatureExtractor()
        self.matcher = None
    
    def step1_setup(self) -> tuple:
        """Step 1: Clone repo + Generate signatures in parallel."""
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
        """Clone Java repository."""
        success = clonar_repositorio_java(self.repo_url, self.repo_path)
        return "Success" if success else "Failed"
    
    def _generate_signatures(self) -> str:
        """Generate pattern signatures."""
        generator = SignatureGenerator()
        generator.save_signatures(self.signatures_path)
        return f"Saved to {self.signatures_path}"
    
    def step2_extract_methods(self) -> List[Dict]:
        """Step 2: Extract methods from Java files."""
        print("\n" + "="*60)
        print("STEP 2: Method Extraction")
        print("="*60)
        
        extractor = JavaMethodExtractor(self.repo_path)
        methods = extractor.extract_from_directory()
        
        print(f"✓ Extracted {len(methods)} methods")
        return methods
    
    def step3_compute_features(self, methods: List[Dict]) -> List[Dict]:
        """Step 3: Compute structural features for each method."""
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
        
        print(f"✓ Computed features for {len(methods_with_features)} methods")
        return methods_with_features
    
    def step4_match_patterns(self, methods: List[Dict], threshold: float = 0.3) -> List[Dict]:
        """Step 4: Match against pattern signatures."""
        print("\n" + "="*60)
        print(f"STEP 4: Pattern Matching (threshold={threshold})")
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
        
        print(f"✓ Found {len(matched_methods)} methods with pattern matches")
        return matched_methods
    
    def step5_rank_and_filter(self, matches: List[Dict], top_k: int = 50) -> List[Dict]:
        """Step 5: Rank by similarity and select top-K."""
        print("\n" + "="*60)
        print(f"STEP 5: Ranking & Filtering (top-{top_k})")
        print("="*60)
        
        ranked = sorted(
            matches,
            key=lambda x: x.get('match', {}).get('score', 0),
            reverse=True
        )
        
        top_results = ranked[:top_k]
        print(f"✓ Selected top-{len(top_results)} results")
        return top_results
    
    def run(self, threshold: float = 0.3, top_k: int = 50, output_path: str = 'outputs/results.json'):
        """Execute complete pipeline."""
        print("\n" + "="*60)
        print(" BUG DETECTION PIPELINE - Similarity-Based Matching")
        print("="*60)
        
        # Execute steps
        self.step1_setup()
        methods = self.step2_extract_methods()
        methods_with_features = self.step3_compute_features(methods)
        matches = self.step4_match_patterns(methods_with_features, threshold)
        top_results = self.step5_rank_and_filter(matches, top_k)
        
        # Save results (JSON + CSV)
        self._save_results(top_results, output_path)
        self._export_to_csv(top_results, output_path.replace('.json', '.csv'))
        
        print("\n" + "="*60)
        print(f"✓ Pipeline completed.")
        print(f"  JSON: {output_path}")
        print(f"  CSV: {output_path.replace('.json', '.csv')}")
        print("="*60 + "\n")
        
        return top_results
    
    def _save_results(self, results: List[Dict], output_path: str):
        """Save results to JSON."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        clean_results = []
        for r in results:
            clean = {
                'file': r.get('file'),
                'class': r.get('class'),
                'method': r.get('name'),
                'match': r.get('match'),
                'all_matches': r.get('all_matches', []),
                'snippet': r.get('code', '')[:500]  # Preview
            }
            clean_results.append(clean)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clean_results, f, indent=2, ensure_ascii=False)
    
    def _export_to_csv(self, results: List[Dict], csv_path: str):
        """Export results to CSV format."""
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            
            # Header
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
            
            # Data
            for idx, result in enumerate(results, 1):
                match = result.get('match', {})
                breakdown = match.get('breakdown', {})
                snippet = result.get('snippet', '')[:200]  # Preview
                
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
