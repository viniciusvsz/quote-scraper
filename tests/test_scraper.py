"""
test_scraper.py

Testes unitários básicos. Mostram no portfólio que você se preocupa
com qualidade, não só "fazer funcionar uma vez".

Rodar com: pytest tests/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scraper import _parse_quotes, _has_next_page

SAMPLE_HTML_WITH_QUOTE = """
<div class="quote">
    <span class="text">"A vida é o que acontece enquanto você faz outros planos."</span>
    <small class="author">John Lennon</small>
    <div class="tags">
        <a class="tag">vida</a>
        <a class="tag">planos</a>
    </div>
</div>
<nav>
    <ul>
        <li class="next"><a href="/page/2/">Next</a></li>
    </ul>
</nav>
"""

SAMPLE_HTML_LAST_PAGE = """
<div class="quote">
    <span class="text">"Última citação."</span>
    <small class="author">Autor Final</small>
    <div class="tags"></div>
</div>
"""


def test_parse_quotes_extracts_text_author_and_tags():
    quotes = _parse_quotes(SAMPLE_HTML_WITH_QUOTE)

    assert len(quotes) == 1
    assert quotes[0].author == "John Lennon"
    assert "vida" in quotes[0].tags
    assert "planos" in quotes[0].tags


def test_parse_quotes_handles_no_tags():
    quotes = _parse_quotes(SAMPLE_HTML_LAST_PAGE)

    assert len(quotes) == 1
    assert quotes[0].tags == []


def test_has_next_page_true_when_next_link_present():
    assert _has_next_page(SAMPLE_HTML_WITH_QUOTE) is True


def test_has_next_page_false_on_last_page():
    assert _has_next_page(SAMPLE_HTML_LAST_PAGE) is False
