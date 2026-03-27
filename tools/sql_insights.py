#!/usr/bin/env python3
"""
SQL to Insights Generator
Usage: python3 sql_insights.py <database_url> --table <table_name>
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text
import sys
from datetime import datetime
import json

def analyze_table(engine, table_name):
    """Generate insights from SQL table"""
    
    # Get row count
    count_result = engine.execute(text(f"SELECT COUNT(*) FROM {table_name}")).fetchone()
    row_count = count_result[0]
    
    # Get sample data
    sample_df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 1000", engine)
    
    # Generate insights
    insights = {
        'table': table_name,
        'total_rows': row_count,
        'columns': len(sample_df.columns),
        'column_info': []
    }
    
    for col in sample_df.columns:
        col_data = {
            'name': col,
            'dtype': str(sample_df[col].dtype),
            'null_count': int(sample_df[col].isnull().sum()),
            'null_pct': float(sample_df[col].isnull().mean() * 100)
        }
        
        # Add stats for numeric columns
        if pd.api.types.is_numeric_dtype(sample_df[col]):
            col_data.update({
                'min': float(sample_df[col].min()),
                'max': float(sample_df[col].max()),
                'mean': float(sample_df[col].mean()),
                'median': float(sample_df[col].median())
            })
        
        # Add top values for categorical
        if sample_df[col].dtype == 'object':
            top_values = sample_df[col].value_counts().head(5).to_dict()
            col_data['top_values'] = {str(k): int(v) for k, v in top_values.items()}
        
        insights['column_info'].append(col_data)
    
    return insights, sample_df

def generate_report(insights, df, output_dir='./insights'):
    """Generate HTML report with tables"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save summary JSON
    json_file = f"{output_dir}/{insights['table']}_insights_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(insights, f, indent=2, default=str)
    
    # Save sample data as CSV
    csv_file = f"{output_dir}/{insights['table']}_sample_{timestamp}.csv"
    df.head(100).to_csv(csv_file, index=False)
    
    # Generate HTML report
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Insights: {insights['table']}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 1000px; margin: 40px auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .stats {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #007AFF; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .numeric {{ text-align: right; }}
    </style>
</head>
<body>
    <h1>📊 Data Insights: {insights['table']}</h1>
    <div class="stats">
        <strong>Total Rows:</strong> {insights['total_rows']:,}<br>
        <strong>Columns:</strong> {insights['columns']}<br>
        <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    
    <h2>Column Analysis</h2>
    <table>
        <tr>
            <th>Column</th>
            <th>Type</th>
            <th>Null %</th>
            <th>Stats</th>
        </tr>
"""
    
    for col in insights['column_info']:
        stats = []
        if 'mean' in col:
            stats.append(f"Mean: {col['mean']:.2f}")
            stats.append(f"Range: {col['min']:.0f} - {col['max']:.0f}")
        if 'top_values' in col:
            top = ', '.join([f"{k[:20]} ({v})" for k, v in list(col['top_values'].items())[:3]])
            stats.append(f"Top: {top}")
        
        html += f"""
        <tr>
            <td><strong>{col['name']}</strong></td>
            <td>{col['dtype']}</td>
            <td>{col['null_pct']:.1f}%</td>
            <td>{'<br>'.join(stats)}</td>
        </tr>
"""
    
    html += """
    </table>
    
    <h2>Sample Data (First 10 Rows)</h2>
    <table>
"""
    
    # Sample data preview
    preview_df = df.head(10)
    html += "<tr>" + "".join(f"<th>{col}</th>" for col in preview_df.columns) + "</tr>"
    
    for _, row in preview_df.iterrows():
        html += "<tr>" + "".join(f"<td>{str(val)[:50]}</td>" for val in row) + "</tr>"
    
    html += f"""
    </table>
    
    <hr>
    <p><em>Files saved: {json_file}, {csv_file}</em></p>
</body>
</html>"""
    
    html_file = f"{output_dir}/{insights['table']}_report_{timestamp}.html"
    with open(html_file, 'w') as f:
        f.write(html)
    
    return html_file, csv_file, json_file

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 sql_insights.py <database_url> --table <table_name>")
        print("Example: python3 sql_insights.py 'sqlite:///data.db' --table users")
        sys.exit(1)
    
    db_url = sys.argv[1]
    table_name = sys.argv[3] if '--table' in sys.argv else sys.argv[2]
    
    try:
        engine = create_engine(db_url)
        print(f"Analyzing table: {table_name}")
        
        insights, df = analyze_table(engine, table_name)
        html_file, csv_file, json_file = generate_report(insights, df)
        
        print(f"\n✓ Analysis complete!")
        print(f"  HTML Report: {html_file}")
        print(f"  CSV Sample: {csv_file}")
        print(f"  JSON Data: {json_file}")
        print(f"\n  Open report: open {html_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
