"""Automated HTML report generator.

Produces a styled HTML report combining KPIs, charts, and tables.
"""
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
from jinja2 import Template

from src.utils.config import REPORTS_DIR

TEMPLATE = Template("""<!doctype html>
<html><head><meta charset='utf-8'>
<title>Housing Analytics Report — {{ generated_at }}</title>
<style>
  body{font-family:'Segoe UI',Arial,sans-serif;margin:30px;color:#222;}
  h1{color:#1f4e79;border-bottom:3px solid #1f4e79;padding-bottom:8px;}
  h2{color:#1f4e79;margin-top:30px;}
  table{border-collapse:collapse;width:100%;margin:14px 0;}
  th,td{border:1px solid #ddd;padding:8px;text-align:right;}
  th{background:#1f4e79;color:#fff;text-align:center;}
  tr:nth-child(even){background:#f5f8fb;}
  .kpi{display:inline-block;background:#1f4e79;color:#fff;padding:14px 18px;
       margin:6px;border-radius:6px;min-width:170px;text-align:center;}
  .kpi span{display:block;font-size:22px;font-weight:bold;}
</style></head><body>
<h1>🏘️ Housing Price & Geographic Analytics</h1>
<p><i>Generated {{ generated_at }}</i></p>
<h2>Key Metrics</h2>
{% for k, val in kpis.items() %}
  <div class='kpi'>{{ k }}<span>{{ val }}</span></div>
{% endfor %}
<h2>Top States by Avg Price</h2>
{{ top_states_html | safe }}
<h2>Top Correlations with Sale Price</h2>
{{ top_corr_html | safe }}
<h2>Model Performance</h2>
<pre>{{ metrics_json }}</pre>
</body></html>""")


def build_report(top_states: pd.DataFrame, top_corr: pd.DataFrame,
                 kpis: dict, metrics: dict | None = None) -> Path:
    html = TEMPLATE.render(
        generated_at=datetime.now().strftime('%Y-%m-%d %H:%M'),
        kpis=kpis,
        top_states_html=top_states.to_html(index=False, float_format='%.2f'),
        top_corr_html=top_corr.to_html(index=False, float_format='%.3f'),
        metrics_json=json.dumps(metrics or {}, indent=2),
    )
    out = REPORTS_DIR / 'housing_analytics_report.html'
    out.write_text(html, encoding='utf-8')
    return out
