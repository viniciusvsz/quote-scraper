"""
scraper.py

Módulo responsável por buscar dados de um site paginado e retornar
os registros em uma estrutura limpa (lista de dicionários).

Site alvo: https://quotes.toscrape.com — um site público criado
especificamente para prática de web scraping (não tem restrição de uso).

Por que este design:
- Sessão HTTP reutilizada (mais rápido, menos overhead de conexão)
- Retry automático em caso de falha de rede (scraping real cai bastante)
- Logging estruturado em vez de print (facilita debug em produção)
- Separação entre "buscar dados" e "gerar relatório" (responsabilidade única)
"""

import logging
import time
from dataclasses import dataclass, asdict

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

BASE_URL = "https://quotes.toscrape.com"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


class ScraperError(Exception):
    """Erro customizado para falhas de scraping, mais fácil de tratar
    no código que chama esta função do que um requests.RequestException genérico."""


def _fetch_page(session: requests.Session, url: str) -> str:
    """Busca uma página HTML com retry automático."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            logger.warning("Tentativa %d/%d falhou para %s: %s", attempt, MAX_RETRIES, url, exc)
            if attempt == MAX_RETRIES:
                raise ScraperError(f"Falha ao buscar {url} após {MAX_RETRIES} tentativas") from exc
            time.sleep(RETRY_DELAY_SECONDS)
    raise ScraperError(f"Falha inesperada ao buscar {url}")


def _parse_quotes(html: str) -> list[Quote]:
    """Extrai as citações de uma página HTML."""
    soup = BeautifulSoup(html, "html.parser")
    quotes = []
    for block in soup.select(".quote"):
        text = block.select_one(".text").get_text(strip=True)
        author = block.select_one(".author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in block.select(".tags .tag")]
        quotes.append(Quote(text=text, author=author, tags=tags))
    return quotes


def _has_next_page(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")
    return soup.select_one(".next") is not None


def scrape_all_quotes(max_pages: int | None = None) -> list[dict]:
    """
    Percorre todas as páginas do site (ou até max_pages) e retorna
    todas as citações encontradas como lista de dicionários.
    """
    all_quotes: list[Quote] = []
    page = 1

    with requests.Session() as session:
        session.headers.update({"User-Agent": "quote-scraper-portfolio-project/1.0"})

        while True:
            url = f"{BASE_URL}/page/{page}/"
            logger.info("Buscando página %d...", page)
            html = _fetch_page(session, url)

            page_quotes = _parse_quotes(html)
            all_quotes.extend(page_quotes)
            logger.info("Página %d: %d citações encontradas", page, len(page_quotes))

            if not _has_next_page(html):
                logger.info("Última página alcançada.")
                break

            page += 1
            if max_pages and page > max_pages:
                logger.info("Limite de %d páginas atingido.", max_pages)
                break

            time.sleep(0.5)  # educado com o servidor, evita sobrecarregar

    return [asdict(q) for q in all_quotes]
