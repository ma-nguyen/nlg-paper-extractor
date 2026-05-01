from typing import List
from pathlib import Path

def export_to_html(all_extracted_papers: List, output_path: Path) -> None:
    import markdown as md
    import html

    response_keys = []
    for entry in all_extracted_papers:
        for result in entry["results"]:
            for key in result["response"].keys():
                if key not in response_keys:
                    response_keys.append(key)

    toc_items = []
    papers_html = []

    for i, entry in enumerate(all_extracted_papers, 1):
        title = html.escape(entry["paper"])

        toc_items.append(
            f'<li><a href="#paper-{i}">{i}. {title}</a></li>'
        )

        model_blocks = []

        for result in entry["results"]:
            fields = []

            for key in response_keys:
                value = result["response"].get(key, "")
                rendered = md.markdown(value)

                fields.append(f"""
                    <div class="field">
                        <span class="field-name">{html.escape(key)}</span>
                        {rendered}
                    </div>
                """)

            model_blocks.append(f"""
                <details class="model-block">
                    <summary>{html.escape(result["model"])}</summary>
                    {''.join(fields)}
                </details>
            """)

        papers_html.append(f"""
            <section class="paper print-page" id="paper-{i}">
                <details>
                    <summary>
                        <h2>{i}. {title}</h2>
                    </summary>

                    {''.join(model_blocks)}

                    <div class="back-top">
                        <a href="#top">↑ Back to top</a>
                    </div>
                </details>
            </section>
        """)

    html_doc = f"""<!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <title>Papers Export</title>

                    <style>
                        body {{
                            margin: 0;
                            font-family: Arial, sans-serif;
                            display: flex;
                            line-height: 1.6;
                            color: #222;
                        }}

                        #sidebar {{
                            position: sticky;
                            top: 0;
                            height: 100vh;
                            width: 320px;
                            overflow-y: auto;
                            background: #f8f9fa;
                            border-right: 1px solid #ddd;
                            padding: 20px;
                            box-sizing: border-box;
                        }}

                        #content {{
                            flex: 1;
                            padding: 40px;
                            overflow-x: auto;
                        }}

                        input {{
                            width: 100%;
                            padding: 10px;
                            margin-bottom: 16px;
                            box-sizing: border-box;
                            font-size: 14px;
                        }}

                        .toggle-controls {{
                            display: flex;
                            gap: 8px;
                            margin-bottom: 16px;
                        }}

                        .toggle-controls button {{
                            flex: 1;
                            padding: 10px;
                            cursor: pointer;
                            border: 1px solid #ccc;
                            background: white;
                            border-radius: 4px;
                        }}

                        ul {{
                            list-style: none;
                            padding: 0;
                            margin: 0;
                        }}

                        li {{
                            margin-bottom: 8px;
                        }}

                        a {{
                            text-decoration: none;
                            color: #007bff;
                        }}

                        a:hover {{
                            text-decoration: underline;
                        }}

                        .paper {{
                            margin-bottom: 48px;
                            border-bottom: 2px solid #eee;
                            padding-bottom: 24px;
                        }}

                        .model-block {{
                            margin: 16px 0;
                            padding: 16px;
                            background: #f9f9f9;
                            border-left: 4px solid #007bff;
                            border-radius: 4px;
                        }}

                        .field {{
                            margin-bottom: 18px;
                        }}

                        .field-name {{
                            display: block;
                            font-weight: bold;
                            margin-bottom: 6px;
                            color: #444;
                            text-transform: capitalize;
                        }}

                        summary {{
                            cursor: pointer;
                            font-weight: bold;
                            padding: 10px 0;
                        }}

                        .back-top {{
                            margin-top: 20px;
                        }}

                        h2 {{
                            display: inline;
                            margin: 0;
                        }}

                        @media print {{
                            #sidebar {{
                                display: none;
                            }}

                            body {{
                                display: block;
                                margin: 0;
                            }}

                            #content {{
                                padding: 0;
                            }}

                            details {{
                                display: block;
                            }}

                            details > * {{
                                display: block;
                            }}

                            summary {{
                                display: block;
                            }}

                            .paper {{
                                page-break-before: always;
                                break-before: page;
                                page-break-inside: avoid;
                                border: none;
                            }}

                            .paper:first-child {{
                                page-break-before: auto;
                                break-before: auto;
                            }}

                            .model-block {{
                                page-break-inside: avoid;
                                break-inside: avoid;
                            }}

                            .back-top {{
                                display: none;
                            }}
                        }}
                    </style>

                    <script>
                    function filterTOC() {{
                        const input = document.getElementById("search").value.toLowerCase();
                        const items = document.querySelectorAll("#toc li");

                        items.forEach(item => {{
                            item.style.display = item.textContent.toLowerCase().includes(input)
                                ? ""
                                : "none";
                        }});
                    }}

                    function toggleAll(open) {{
                        document.querySelectorAll("details").forEach(d => {{
                            d.open = open;
                        }});
                    }}

                    window.onbeforeprint = function() {{
                        toggleAll(true);
                    }};
                    </script>

                    </head>

                    <body id="top">

                    <div id="sidebar">
                        <h2>{len(all_extracted_papers)} Papers</h2>

                        <input
                            id="search"
                            type="text"
                            placeholder="Search papers..."
                            onkeyup="filterTOC()"
                        >

                        <div class="toggle-controls">
                            <button onclick="toggleAll(true)">Expand All</button>
                            <button onclick="toggleAll(false)">Collapse All</button>
                        </div>

                        <ul id="toc">
                            {''.join(toc_items)}
                        </ul>
                    </div>

                    <div id="content">
                        {''.join(papers_html)}
                    </div>

                    </body>
                    </html>
                    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
