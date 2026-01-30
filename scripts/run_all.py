"""
Main script to execute the entire pipeline with report generation
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    """Executes the complete classification and report generation pipeline."""
    
    print("\n" + "="*80)
    print(" BUG DETECTION AND CLASSIFICATION PIPELINE WITH LLAMA 2")
    print("="*80 + "\n")
    
    # 1. Run classification
    print("[1/3] Starting classification with LLaMA 2...")
    print("-" * 80)
    
    proc = subprocess.Popen(
        [sys.executable, 'classify.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Monitor output
    while proc.poll() is None:
        try:
            line = proc.stdout.readline()
            if line:
                print(line.rstrip())
        except:
            break
    
    # Get last output if any
    remaining_output = proc.stdout.read()
    if remaining_output:
        print(remaining_output)
    
    if proc.returncode != 0:
        print(f"[ERROR] Classification failed with code {proc.returncode}")
        return
    
    print("\n[OK] Classification complete!\n")
    
    # 2. Generate markdown report
    print("[2/3] Generating Markdown report...")
    print("-" * 80)
    
    try:
        from report_markdown import generate_report
        generate_report()
    except Exception as e:
        print(f"[ERROR] Failed to generate Markdown report: {e}")
    
    # 3. Generate HTML report
    print("[3/3] Generating visual HTML report...")
    print("-" * 80)
    
    try:
        from report_html import generate_html_report
        generate_html_report()
    except Exception as e:
        print(f"[ERROR] Failed to generate HTML report: {e}")
    
    # Final summary
    print("\n" + "="*80)
    print(" PIPELINE COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  📊 outputs/results_with_llm.json - Results with LLM classification")
    print("  📄 outputs/report_llm.md - Markdown report")
    print("  🌐 outputs/report_visual.html - Visual HTML report")
    print("\nNext steps:")
    print("  1. Open outputs/report_visual.html in browser")
    print("  2. Review bugs confirmed by AI")
    print("  3. Use data for validation and fixes\n")

if __name__ == '__main__':
    main()
