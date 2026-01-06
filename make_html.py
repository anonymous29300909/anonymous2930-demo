import csv

# Path to your CSV file
csv_file = "demo.csv"

# Path to output HTML
html_file = "index.html"

# Start the HTML template
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Speech Language Model Demo</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
    h1, h2 {{ text-align: center; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 30px; }}
    th, td {{ border: 1px solid #ccc; padding: 12px; text-align: center; }}
    th {{ background-color: #f5f5f5; }}
    audio {{ width: 220px; }}
    .caption {{ text-align: center; font-size: 0.95em; color: #555; margin-top: 10px; }}
  </style>
</head>
<body>

<h1>Speech Language Model Demo</h1>
<p style="text-align:center;">
  Audio samples for zero-shot TTS and STT evaluation.
</p>

<h2>Zero-shot TTS Samples</h2>

<table>
  <tr>
    <th>Text</th>
    <th>Reference</th>
    <th>Ground Truth</th>
    <th>Codec-SLM</th>
    <th>DLMel-SLM</th>
    <th>DLMel-SML (joint)</th>
  </tr>
  {rows}
</table>

</body>
</html>
'''

# Read CSV and generate table rows
rows_html = ""
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows_html += f'''
  <tr>
    <td><em>"{row['text']}"</em></td>
    <td><audio controls><source src="{row['Reference']}" type="audio/flac"></audio></td>
    <td><audio controls><source src="{row['GT']}" type="audio/flac"></audio></td>
    <td><audio controls><source src="{row['f768407035']}" type="audio/flac"></audio></td>
    <td><audio controls><source src="{row['f821282878']}" type="audio/flac"></audio></td>
    <td><audio controls><source src="{row['f831930970']}" type="audio/flac"></audio></td>
  </tr>
'''

# Write the HTML file
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_template.format(rows=rows_html))

print(f"index.html generated with all samples from {csv_file}")
