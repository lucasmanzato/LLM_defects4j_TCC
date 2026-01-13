import os
import re
import json
from typing import List, Dict, Any, Optional, Tuple

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Optional: use javalang if available for robust Java parsing
try:
    import javalang
    HAS_JAVALANG = True
except Exception:
    HAS_JAVALANG = False

class JavaSnippetExtractor:
    """
    Extracts Java method-level snippets from source files.
    Uses javalang if available; otherwise falls back to naive regex.
    """

    def __init__(self, root_dir: str):
        self.root_dir = os.path.abspath(root_dir)

    def list_java_files(self) -> List[str]:
        files = []
        for r, d, f in os.walk(self.root_dir):
            for name in f:
                if name.endswith('.java'):
                    files.append(os.path.join(r, name))
        return files

    def extract_methods(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as fh:
            code = fh.read()
        if HAS_JAVALANG:
            try:
                tree = javalang.parse.parse(code)
                methods = []
                for _, class_decl in tree.filter(javalang.tree.TypeDeclaration):
                    class_name = getattr(class_decl, 'name', None)
                    for method in getattr(class_decl, 'methods', []):
                        start_pos = getattr(method, 'position', None)
                        method_src = self._slice_source_by_position(code, start_pos, method)
                        methods.append({
                            'class': class_name,
                            'name': method.name,
                            'file': file_path,
                            'code': method_src or self._fallback_method_text(code, method.name),
                        })
                return methods
            except Exception:
                # Fallback to regex
                return self._regex_extract_methods(code, file_path)
        else:
            return self._regex_extract_methods(code, file_path)

    def _slice_source_by_position(self, code: str, start_pos, method_obj) -> Optional[str]:
        # javalang doesn't provide end positions; naive brace matching from start
        if not start_pos:
            return None
        lines = code.splitlines()
        # Convert to 0-based index
        i = start_pos[0] - 1
        # Join from start line
        tail = "\n".join(lines[i:])
        # Find first '{' after method header
        header_end = tail.find('{')
        if header_end == -1:
            return None
        start_idx = header_end
        brace_count = 0
        end_idx = None
        for idx, ch in enumerate(tail[start_idx:], start=start_idx):
            if ch == '{':
                brace_count += 1
            elif ch == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = idx + 1
                    break
        if end_idx:
            return tail[:end_idx]
        return None

    def _regex_extract_methods(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        methods = []
        # Very naive: find method signatures and balance braces
        signature_pattern = re.compile(r"(public|protected|private|static|\s)+[\w\<\>\[\]]+\s+(\w+)\s*\([^\)]*\)\s*\{", re.MULTILINE)
        for m in signature_pattern.finditer(code):
            name = m.group(2)
            start = m.start()
            end = self._find_matching_brace(code, m.end()-1)
            if end:
                snippet = code[start:end]
                methods.append({'class': None, 'name': name, 'file': file_path, 'code': snippet})
        return methods

    def _find_matching_brace(self, code: str, start_idx: int) -> Optional[int]:
        brace_count = 0
        for idx in range(start_idx, len(code)):
            ch = code[idx]
            if ch == '{':
                brace_count += 1
            elif ch == '}':
                brace_count -= 1
                if brace_count == 0:
                    return idx + 1
        return None

    def _fallback_method_text(self, code: str, method_name: str) -> Optional[str]:
        # Fallback: search by method name
        idx = code.find(method_name)
        if idx == -1:
            return None
        start_brace = code.find('{', idx)
        if start_brace == -1:
            return None
        return code[idx:self._find_matching_brace(code, start_brace) or len(code)]


class HeuristicBugDetector:
    """
    Applies regex-based heuristics inspired by common Defects4J bug themes.
    Returns a score and labels indicating potential bug patterns.
    """

    def detect(self, code: str) -> Tuple[float, List[str]]:
        labels = []
        score = 0.0

        # 1. String equality using '=='
        if re.search(r"if\s*\([^\)]*==[^\)]*\)", code):
            if '"' in code or "'" in code:
                labels.append('string-equality-using-==')
                score += 0.2

        # 2. Off-by-one on array length
        if re.search(r"for\s*\([^;]*;[^;]*<=\s*\w+\.length;[^\)]*\)", code):
            labels.append('off-by-one-length')
            score += 0.25

        # 3. Empty catch blocks
        if re.search(r"catch\s*\([^\)]*\)\s*\{\s*\}", code):
            labels.append('empty-catch')
            score += 0.2

        # 4. Swallowed exception (catch with only comment or log w/o rethrow)
        if re.search(r"catch\s*\([^\)]*\)\s*\{\s*(//.*)?\s*\}", code):
            labels.append('swallowed-exception')
            score += 0.2

        # 5. Resource not closed (no try-with-resources)
        if re.search(r"new\s+(File(Input|Output)Stream|Buffered(Reader|Writer)|InputStream|OutputStream)", code) and not re.search(r"try\s*\(", code):
            labels.append('resource-not-closed')
            score += 0.25

        # 6. Potential null deref: calling equals without null-check
        if re.search(r"\w+\.equals\([^\)]*\)", code) and not re.search(r"if\s*\([^\)]*!=\s*null\)", code):
            labels.append('equals-without-null-check')
            score += 0.2

        score = min(score, 1.0)
        return score, labels


class FixSuggester:
    """
    Provides simple heuristic fix suggestions for detected labels.
    """

    def suggest(self, labels: List[str], code: str) -> Dict[str, Any]:
        suggestions = []
        for label in labels:
            if label == 'string-equality-using-==':
                suggestions.append('Substituir comparações de String com "==" por ".equals()".')
            elif label == 'off-by-one-length':
                suggestions.append('Em laços com length, trocar "<= length" por "< length".')
            elif label == 'empty-catch':
                suggestions.append('Evitar catch vazio: registrar, repropagar ou tratar adequadamente.')
            elif label == 'swallowed-exception':
                suggestions.append('Evitar engolir exceções: adicionar log e repropagar ou tratar.')
            elif label == 'resource-not-closed':
                suggestions.append('Usar try-with-resources para garantir fechamento de recursos.')
            elif label == 'equals-without-null-check':
                suggestions.append('Adicionar verificação de null antes de chamar equals().')
        return {
            'heuristic_fix': suggestions or None
        }


class LLMFilter:
    """
    Optional LLM-based classification using Google Gemini.
    If GEMINI_API_KEY is present, attempts to classify snippets;
    otherwise returns None to use heuristics only.
    """

    def __init__(self, model: Optional[str] = None):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.model = model or os.environ.get('GEMINI_MODEL') or 'gemini-1.5-flash'
        self._client = None
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")
                self._client = None

    def classify(self, snippet: str, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self._client:
            return None
        prompt = (
            "You are a Java bug pattern classifier based on Defects4J themes. "
            "Given a Java method snippet, analyze likely bug patterns: null deref, boundary/off-by-one, incorrect conditionals, "
            "API misuse, resource leaks, exception swallowing, string equality with ==, equals/hashCode mismatch, concurrency hazards. "
            "Return a valid JSON with fields: bug_likelihood (0..1 float), labels (array of short identifiers), reason (short string), fix (a simple fix suggestion). "
            "Do NOT include markdown code blocks or extra text, only the JSON object.")
        
        content = json.dumps({
            'file': metadata.get('file'),
            'class': metadata.get('class'),
            'name': metadata.get('name'),
            'code': snippet,
        }, ensure_ascii=False)
        
        try:
            # Try to use the configured model; fall back to gemini-2.0-flash if not available
            model_name = self.model
            try:
                model = self._client.GenerativeModel(model_name)
                response = model.generate_content(
                    f"{prompt}\n\nCode snippet metadata:\n{content}",
                    generation_config={"temperature": 0.2}
                )
            except Exception as model_err:
                # Fallback to gemini-2.0-flash
                if "not found" in str(model_err) or "not supported" in str(model_err):
                    model = self._client.GenerativeModel("gemini-2.0-flash")
                    response = model.generate_content(
                        f"{prompt}\n\nCode snippet metadata:\n{content}",
                        generation_config={"temperature": 0.2}
                    )
                else:
                    raise
            txt = response.text.strip()
            # Remove markdown code blocks if present
            if txt.startswith("```"):
                txt = txt[txt.find("\n")+1:]
            if txt.endswith("```"):
                txt = txt[:txt.rfind("```")]
            return json.loads(txt)
        except json.JSONDecodeError as e:
            print(f"Failed to parse Gemini response as JSON: {e}")
            return None
        except Exception as e:
            print(f"Gemini classification error: {e}")
            return None


class FilterPipeline:
    def __init__(self, root_dir: str, use_llm: bool = True):
        self.root_dir = os.path.abspath(root_dir)
        self.extractor = JavaSnippetExtractor(self.root_dir)
        self.detector = HeuristicBugDetector()
        self.llm = LLMFilter() if use_llm else None
        self.suggester = FixSuggester()

    def run(self, top_k: int = 50, patterns: Optional[List[str]] = None, strict: bool = False) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        files = self.extractor.list_java_files()
        for f in files:
            methods = self.extractor.extract_methods(f)
            for m in methods:
                score, labels = self.detector.detect(m['code'])
                llm_result = None
                if self.llm:
                    llm_result = self.llm.classify(m['code'], m)
                combined_score = max(score, llm_result.get('bug_likelihood', 0.0) if llm_result else score)
                combined_labels = list(set(labels + (llm_result.get('labels', []) if llm_result else [])))
                suggestion = self.suggester.suggest(combined_labels, m['code'])
                if llm_result and llm_result.get('fix'):
                    suggestion['llm_fix'] = llm_result.get('fix')
                # Apply label-based filtering if patterns provided
                if patterns:
                    label_set = set(combined_labels)
                    patterns_set = set([p.strip() for p in patterns if p and p.strip()])
                    if strict:
                        # require all patterns to be present
                        if not patterns_set.issubset(label_set):
                            continue
                    else:
                        # require any overlap
                        if label_set.isdisjoint(patterns_set):
                            continue
                results.append({
                    'file': m['file'],
                    'class': m['class'],
                    'name': m['name'],
                    'heuristic_score': score,
                    'heuristic_labels': labels,
                    'llm': llm_result,
                    'score': combined_score,
                    'labels': combined_labels,
                    'snippet': m['code'],
                    'suggestion': suggestion,
                })
        # Sort by combined score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]


def save_results(results: List[Dict[str, Any]], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(results, fh, ensure_ascii=False, indent=2)


def main():
    repo_path = os.environ.get('REPO_PATH') or os.path.join(os.getcwd(), 'dados', 'commons-lang')
    out_path = os.environ.get('OUT_PATH') or os.path.join(os.getcwd(), 'dados', 'bug_snippets.json')
    use_llm_env = os.environ.get('USE_LLM', '1')
    use_llm = use_llm_env.strip() not in ('0', 'false', 'False')

    pipeline = FilterPipeline(repo_path, use_llm=use_llm)
    results = pipeline.run(top_k=50)
    save_results(results, out_path)
    print(f"Saved {len(results)} snippets to {out_path}")


if __name__ == '__main__':
    main()
