import os
from bug_filter_llm import FilterPipeline, save_results

if __name__ == '__main__':
    repo_path = os.environ.get('REPO_PATH') or os.path.join(os.getcwd(), 'dados', 'commons-lang')
    out_path = os.environ.get('OUT_PATH') or os.path.join(os.getcwd(), 'dados', 'bug_snippets.json')
    use_llm_env = os.environ.get('USE_LLM', '1')
    use_llm = use_llm_env.strip() not in ('0', 'false', 'False')

    # Optional filtering controls
    patterns_env = os.environ.get('PATTERNS')  # comma-separated
    patterns = [p.strip() for p in patterns_env.split(',')] if patterns_env else None
    strict_env = os.environ.get('STRICT_FILTER', '0')
    strict = strict_env.strip() in ('1', 'true', 'True')
    top_k_env = os.environ.get('TOP_K')
    try:
        top_k = int(top_k_env) if top_k_env else 50
    except ValueError:
        top_k = 50

    pipeline = FilterPipeline(repo_path, use_llm=use_llm)
    results = pipeline.run(top_k=top_k, patterns=patterns, strict=strict)
    save_results(results, out_path)
    print(f"Saved {len(results)} snippets to {out_path}")
