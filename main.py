"""
main.py

Ponto de entrada do projeto. Interface de linha de comando (CLI) simples
para rodar o scraper e gerar os relatórios.

Uso:
    python main.py
    python main.py --max-pages 3
    python main.py --output-dir resultados
"""

import argparse
import logging
from pathlib import Path

from scraper import scrape_all_quotes, ScraperError
from report import save_csv, generate_summary

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Coleta citações de quotes.toscrape.com e gera relatórios."
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Número máximo de páginas a coletar (padrão: todas)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Pasta onde salvar os arquivos gerados (padrão: ./output)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        quotes = scrape_all_quotes(max_pages=args.max_pages)
    except ScraperError as exc:
        logger.error("Não foi possível coletar os dados: %s", exc)
        raise SystemExit(1)

    if not quotes:
        logger.warning("Nenhuma citação encontrada.")
        raise SystemExit(0)

    csv_path = output_dir / "quotes.csv"
    summary_path = output_dir / "summary.md"

    save_csv(quotes, str(csv_path))
    generate_summary(quotes, str(summary_path))

    logger.info("Concluído! %d citações salvas em:", len(quotes))
    logger.info("  - %s", csv_path)
    logger.info("  - %s", summary_path)


if __name__ == "__main__":
    main()
