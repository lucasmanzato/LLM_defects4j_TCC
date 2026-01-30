"""
Main entry point for bug detection system.
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from pipelines.detection_pipeline import BugDetectionPipeline
from dotenv import load_dotenv


def main():
    """Run bug detection pipeline."""
    load_dotenv()
    
    # Configuration
    repo_url = os.environ.get('REPO_URL', 'https://github.com/apache/commons-lang.git')
    repo_path = os.environ.get('REPO_PATH', 'dados/commons-lang')
    output_path = os.environ.get('OUTPUT_PATH', 'outputs/results.json')
    threshold = float(os.environ.get('SIMILARITY_THRESHOLD', '0.3'))
    top_k = int(os.environ.get('TOP_K', '50'))
    
    # Run pipeline
    pipeline = BugDetectionPipeline(repo_url, repo_path)
    results = pipeline.run(
        threshold=threshold,
        top_k=top_k,
        output_path=output_path
    )
    
    print(f"\n✓ Analysis complete!")
    print(f"  Found {len(results)} potential bugs")
    print(f"  Results: {output_path}")
    print(f"  CSV: {output_path.replace('.json', '.csv')}")


if __name__ == '__main__':
    main()
