# Quote Scraper & Report Generator

Projeto de portfólio: coleta dados de um site paginado, trata erros de rede
e gera relatórios automáticos (CSV + resumo em Markdown).

Construído para demonstrar boas práticas comuns em pedidos reais de
automação/scraping freelance: sessão HTTP reutilizável, retry automático,
logging estruturado, separação de responsabilidades e testes unitários.

## O que ele faz

1. Percorre todas as páginas de [quotes.toscrape.com](https://quotes.toscrape.com)
   (site público feito para prática de scraping)
2. Extrai texto, autor e tags de cada citação
3. Gera:
   - `output/quotes.csv` — todos os dados brutos
   - `output/summary.md` — estatísticas (autores mais citados, tags mais comuns)

## Como rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar o scraper completo
python main.py

# Ou limitar a algumas páginas (mais rápido para testar)
python main.py --max-pages 2

# Escolher pasta de saída
python main.py --output-dir meus_resultados
```

## Rodar os testes

```bash
pytest tests/
```

## Estrutura do projeto

```
quote-scraper/
├── main.py           # CLI, ponto de entrada
├── scraper.py         # Lógica de coleta de dados (requisições + parsing)
├── report.py           # Geração de CSV e resumo estatístico
├── tests/
│   └── test_scraper.py  # Testes unitários do parsing
├── requirements.txt
└── README.md
```

## Decisões de design (e por quê)

- **Sessão HTTP reutilizada**: evita reabrir conexão TCP a cada página, mais rápido em sites com muitas páginas.
- **Retry automático com backoff**: scraping real cai por instabilidade de rede o tempo todo; isso evita que o script quebre na primeira falha.
- **Dataclass `Quote`**: estrutura tipada em vez de dicionários soltos, deixa o código mais legível e evita erros de digitação em chaves.
- **Separação scraper / report**: se amanhã a fonte de dados mudar (outro site, uma API), só `scraper.py` muda — `report.py` continua funcionando igual.
- **Logging em vez de print**: em um projeto real (ou rodando agendado via cron), você precisa de logs com timestamp, não só texto solto no terminal.

## Possíveis extensões (bom mostrar que você pensou além do básico)

- Adaptar `scraper.py` para outro site trocando os seletores CSS
- Adicionar agendamento automático (ex: rodar todo dia às 8h com `cron` ou `schedule`)
- Salvar histórico em SQLite em vez de sobrescrever o CSV a cada execução
- Adicionar envio de e-mail/Telegram com o resumo gerado
