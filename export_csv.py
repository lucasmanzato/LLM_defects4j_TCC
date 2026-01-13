import json
import csv
import os

def export_to_csv(json_path: str, csv_path: str):
    """Export bug snippets from JSON to CSV for analysis."""
    with open(json_path, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['file', 'class', 'method', 'score', 'labels', 'heuristic_fix', 'llm_fix']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in data:
            suggestion = item.get('suggestion', {})
            heur_fix = suggestion.get('heuristic_fix', [])
            llm_fix = suggestion.get('llm_fix')
            
            writer.writerow({
                'file': os.path.basename(item['file']),
                'class': item.get('class') or 'N/A',
                'method': item['name'],
                'score': item['score'],
                'labels': '; '.join(item.get('labels', [])),
                'heuristic_fix': '; '.join(heur_fix) if heur_fix else 'N/A',
                'llm_fix': llm_fix if llm_fix else 'N/A'
            })
    
    print(f"✓ Exported {len(data)} snippets to {csv_path}")

if __name__ == '__main__':
    json_path = os.environ.get('IN_PATH') or os.path.join('..', 'dados', 'bug_snippets.json')
    csv_path = os.environ.get('CSV_PATH') or os.path.join('..', 'dados', 'bug_snippets.csv')
    export_to_csv(json_path, csv_path)
