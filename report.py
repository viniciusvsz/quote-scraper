"""
report.py

Transforma os dados brutos coletados pelo scraper em relatórios úteis:
- CSV com todos os registros (pra abrir em Excel/Sheets)
- Resumo em Markdown com estatísticas (autores mais citados, tags mais comuns)

Separar isso do scraper.py é proposital: em um projeto real, você pode
querer trocar a fonte de dados (outro site, uma API, um banco) sem
tocar na lógica de relatório.
"""

import csv
from collections import Counter
from pathlib import Path


def save_csv(quotes: list[dict], output_path: str) -> None:
    """Salva os dados brutos em CSV."""
    if not quotes:
        raise ValueError("Lista de citações vazia, nada para salvar.")

    fieldnames = ["text", "author", "tags"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for quote in quotes:
            writer.writerow({
                "text": quote["text"],
                "author": quote["author"],
                "tags": ", ".join(quote["tags"]),
            })


def generate_summary(quotes: list[dict], output_path: str) -> None:
    """Gera um resumo em Markdown com as estatísticas mais relevantes."""
    author_counts = Counter(q["author"] for q in quotes)
    tag_counts = Counter(tag for q in quotes for tag in q["tags"])

    lines = [
        "# Relatório de citações\n",
        f"Total de citações coletadas: **{len(quotes)}**\n",
        "## Top 5 autores mais citados\n",
    ]
    for author, count in author_counts.most_common(5):
        lines.append(f"- {author}: {count} citações")

    lines.append("\n## Top 10 tags mais comuns\n")
    for tag, count in tag_counts.most_common(10):
        lines.append(f"- {tag}: {count} ocorrências")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
