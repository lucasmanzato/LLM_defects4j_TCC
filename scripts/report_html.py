"""
Gera relatório visual em HTML com gráficos dos resultados
"""
import json
from datetime import datetime
from collections import defaultdict

def _is_confirmed(result: dict) -> bool:
    """Retorna True se a LLM confirmou o bug, aceitando chaves legadas."""
    llm = result.get('llm_classification', {}) or {}
    return bool(llm.get('eh_bug_real', llm.get('eh_realmente_bug', llm.get('is_real_bug', False))))


def generate_html_report():
    """Gera relatório em HTML com estatísticas visuais."""
    
    try:
        with open('outputs/results_with_llm.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("[ERRO] Arquivo results_with_llm.json nao encontrado")
        return
    
    # Coletar estatísticas
    total = len(results)
    verified = sum(1 for r in results if _is_confirmed(r))
    not_verified = total - verified
    
    # Confiança média
    confidences = [r.get('llm_classification', {}).get('confianca', 0) 
                  for r in results if r.get('llm_classification')]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    # Stats por padrão
    patterns_stats = defaultdict(lambda: {'total': 0, 'verified': 0, 'avg_score': 0, 'scores': []})
    
    for result in results:
        pattern = result.get('match', {}).get('pattern_name', 'Unknown')
        is_verified = _is_confirmed(result)
        score = result.get('match', {}).get('score', 0)
        
        patterns_stats[pattern]['total'] += 1
        if is_verified:
            patterns_stats[pattern]['verified'] += 1
        patterns_stats[pattern]['scores'].append(score)
    
    for pattern in patterns_stats:
        scores = patterns_stats[pattern]['scores']
        patterns_stats[pattern]['avg_score'] = sum(scores) / len(scores) if scores else 0
    
    # Distribuição de confiança
    confidence_buckets = {
        '0% - 20%': len([c for c in confidences if c < 0.2]),
        '20% - 40%': len([c for c in confidences if 0.2 <= c < 0.4]),
        '40% - 60%': len([c for c in confidences if 0.4 <= c < 0.6]),
        '60% - 80%': len([c for c in confidences if 0.6 <= c < 0.8]),
        '80% - 100%': len([c for c in confidences if c >= 0.8]),
    }
    
    # Gerar HTML
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Detecção de Bugs - LLaMA 2</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .stat-card h3 {{
            color: #333;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
            color: #666;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-percent {{
            font-size: 1.2em;
            color: #999;
            margin-top: 5px;
        }}
        
        .chart-container {{
            position: relative;
            height: 400px;
            margin-bottom: 40px;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        th {{
            background: #f8f9fa;
            color: #333;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .badge-danger {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .badge-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        
        footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 24px;
            background: #e9ecef;
            border-radius: 12px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.85em;
            transition: width 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Relatório de Detecção de Bugs</h1>
            <p>Análise com LLaMA 2 via Ollama - {datetime.now().strftime('%d de %B de %Y às %H:%M:%S')}</p>
        </header>
        
        <div class="content">
            <!-- Resumo Executivo -->
            <section class="section">
                <h2>📈 Resumo Executivo</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Total Analisados</h3>
                        <div class="stat-value">{total}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Bugs Confirmados</h3>
                        <div class="stat-value">{verified}</div>
                        <div class="stat-percent">{verified/total*100:.1f}% de confirmação</div>
                    </div>
                    <div class="stat-card">
                        <h3>Não Confirmados</h3>
                        <div class="stat-value">{not_verified}</div>
                        <div class="stat-percent">{not_verified/total*100:.1f}%</div>
                    </div>
                    <div class="stat-card">
                        <h3>Confiança Média</h3>
                        <div class="stat-value">{avg_confidence:.2%}</div>
                        <div class="stat-percent">dos resultados</div>
                    </div>
                </div>
            </section>
            
            <!-- Gráfico de Taxa de Confirmação por Padrão -->
            <section class="section">
                <h2>🎯 Taxa de Confirmação por Padrão</h2>
                <div class="chart-container">
                    <canvas id="patternChart"></canvas>
                </div>
                <table>
                    <tr>
                        <th>Padrão</th>
                        <th>Total</th>
                        <th>Confirmados</th>
                        <th>Taxa</th>
                        <th>Score Médio</th>
                    </tr>
"""
    
    for pattern in sorted(patterns_stats.keys()):
        stats = patterns_stats[pattern]
        total_p = stats['total']
        verified_p = stats['verified']
        taxa = verified_p / total_p * 100 if total_p > 0 else 0
        avg_score = stats['avg_score']
        
        html += f"""
                    <tr>
                        <td>{pattern}</td>
                        <td>{total_p}</td>
                        <td><span class="badge badge-success">{verified_p}</span></td>
                        <td>{taxa:.1f}%</td>
                        <td>{avg_score:.4f}</td>
                    </tr>
"""
    
    html += """
                </table>
            </section>
            
            <!-- Distribuição de Confiança -->
            <section class="section">
                <h2>📊 Distribuição de Confiança</h2>
                <div class="chart-container">
                    <canvas id="confidenceChart"></canvas>
                </div>
                <div style="margin-top: 30px;">
"""
    
    for bucket, count in confidence_buckets.items():
        percentage = count / total * 100 if total > 0 else 0
        html += f"""
                    <div style="margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span><strong>{bucket}</strong></span>
                            <span>{count} bugs ({percentage:.1f}%)</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {percentage}%">
                                {percentage:.0f}%
                            </div>
                        </div>
                    </div>
"""
    
    html += """
                </div>
            </section>
            
            <!-- Top 10 Bugs -->
            <section class="section">
                <h2>⭐ Top 10 Bugs Mais Confiáveis</h2>
                <table>
                    <tr>
                        <th>Padrão</th>
                        <th>Classe</th>
                        <th>Método</th>
                        <th>Confiança</th>
                        <th>Status</th>
                    </tr>
"""
    
    sorted_results = sorted(
        results,
        key=lambda x: x.get('llm_classification', {}).get('confianca', 0),
        reverse=True
    )
    
    for result in sorted_results[:10]:
        pattern = result.get('match', {}).get('pattern_name', '?')
        classname = result.get('class', '?')
        method = result.get('method', '?')
        conf = result.get('llm_classification', {}).get('confianca', 0)
        is_bug = _is_confirmed(result)
        badge_class = "badge-success" if is_bug else "badge-danger"
        status = "BUG" if is_bug else "NÃO É BUG"
        
        html += f"""
                    <tr>
                        <td>{pattern}</td>
                        <td>{classname}</td>
                        <td>{method}</td>
                        <td><strong>{conf:.2%}</strong></td>
                        <td><span class="badge {badge_class}">{status}</span></td>
                    </tr>
"""
    
    html += """
                </table>
            </section>
        </div>
        
        <footer>
            <p>Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>Análise de bugs em Java com LLaMA 2 e similaridade estrutural</p>
        </footer>
    </div>
    
    <script>
        // Gráfico de padrões
        const patternCtx = document.getElementById('patternChart').getContext('2d');
        const patternChart = new Chart(patternCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([p for p in sorted(patterns_stats.keys())])},
                datasets: [
                    {{
                        label: 'Confirmados',
                        data: {json.dumps([patterns_stats[p]['verified'] for p in sorted(patterns_stats.keys())])},
                        backgroundColor: '#667eea'
                    }},
                    {{
                        label: 'Não Confirmados',
                        data: {json.dumps([patterns_stats[p]['total'] - patterns_stats[p]['verified'] for p in sorted(patterns_stats.keys())])},
                        backgroundColor: '#e9ecef'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        
        // Gráfico de confiança
        const confidenceCtx = document.getElementById('confidenceChart').getContext('2d');
        const confidenceChart = new Chart(confidenceCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(list(confidence_buckets.keys()))},
                datasets: [{{
                    data: {json.dumps(list(confidence_buckets.values()))},
                    backgroundColor: [
                        '#ff6b6b',
                        '#ffd93d',
                        '#6bcf7f',
                        '#4ecdc4',
                        '#667eea'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    # Salvar arquivo
    with open('outputs/relatorio_visual.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("[OK] Relatório HTML gerado: outputs/relatorio_visual.html")

if __name__ == '__main__':
    generate_html_report()
