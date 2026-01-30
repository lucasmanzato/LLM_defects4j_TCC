"""
Ponto de entrada principal para o sistema de detecção de bugs.
"""
import sys
import os
from pathlib import Path

# Adicionar src ao caminho
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from pipelines.detection_pipeline import BugDetectionPipeline
from dotenv import load_dotenv


def main():
    """Executa pipeline de detecção de bugs."""
    load_dotenv()
    
    # Configuração
    repo_url = os.environ.get('REPO_URL', 'https://github.com/apache/commons-lang.git')
    repo_path = os.environ.get('REPO_PATH', 'dados/commons-lang')
    output_path = os.environ.get('OUTPUT_PATH', 'outputs/results.json')
    threshold = float(os.environ.get('SIMILARITY_THRESHOLD', '0.3'))
    top_k = int(os.environ.get('TOP_K', '50'))
    
    # Executar pipeline
    pipeline = BugDetectionPipeline(repo_url, repo_path)
    results = pipeline.run(
        threshold=threshold,
        top_k=top_k,
        output_path=output_path
    )
    
    print(f"\n✓ Análise concluída!")
    print(f"  Encontrados {len(results)} bugs potenciais")
    print(f"  Resultados: {output_path}")
    print(f"  CSV: {output_path.replace('.json', '.csv')}")


if __name__ == '__main__':
    main()
