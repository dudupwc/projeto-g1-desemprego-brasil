# Projeto G1 — Análise e Visualização do Desemprego no Brasil

## Tema
**Desemprego no Brasil — 2015 a 2024**

## Objetivo
Analisar uma base simulada de dados de desemprego, identificando evolução temporal, diferenças regionais e relações entre taxa de desemprego, renda média, vagas formais e inflação.

> **Importante:** a base é simulada. Os resultados deste projeto não representam estatísticas oficiais.

## Tecnologias
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- SQLAlchemy
- SQLite
- GitHub / GitHub Pages

## Funcionalidades intermediárias atendidas
1. Filtros múltiplos no Streamlit.
2. KPIs dinâmicos.
3. Análise temporal.
4. Visualizações comparativas.
5. Tabelas interativas.

## Funcionalidades avançadas atendidas
1. **Persistência em banco:** SQLite + SQLAlchemy.
2. **Mapas interativos:** Plotly com visualização geográfica por UF.
3. **Séries temporais:** análise trimestral de 2015 a 2024.
4. **Correlação estatística:** matriz de correlação entre indicadores numéricos.

## Estrutura
```text
projeto-g1/
├── app.py
├── requirements.txt
├── README.md
├── index.html
├── dados/
│   └── simulacao_desemprego_brasil.csv
├── database/
│   └── desemprego.db
├── notebooks/
│   └── analise_desemprego_brasil.ipynb
└── imagens/
```

## Como executar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

O banco SQLite é criado/atualizado automaticamente a partir do CSV caso seja necessário.

## Publicação

### GitHub
Crie um repositório e envie todos os arquivos do projeto.

### GitHub Pages
No GitHub, acesse **Settings → Pages**, selecione a branch principal e a pasta `/root`. O arquivo `index.html` será usado como página inicial.

### Streamlit Community Cloud
Crie um novo app apontando para o repositório, selecione `app.py` como arquivo principal e aguarde o deploy.

## Entregas
- Repositório GitHub: preencher com o link do repositório criado.
- GitHub Pages: preencher com o link gerado pelo GitHub.
- Dashboard Streamlit: preencher com o link gerado pelo Streamlit Community Cloud.
- Notebook: `notebooks/analise_desemprego_brasil.ipynb`
- Código do dashboard: `app.py`

## Critérios de avaliação contemplados
- Organização do projeto: estrutura solicitada e README.
- Tratamento dos dados: validação de nulos, duplicados, tipos e consistência.
- Análise exploratória: temporal, regional, UF e setor.
- Qualidade dos gráficos: Matplotlib, Seaborn e Plotly.
- Streamlit: dashboard com filtros, KPIs, tabelas e interpretações.
- Funcionalidades avançadas: SQLite/SQLAlchemy, mapa, séries temporais e correlação.
- Interatividade: filtros e gráficos interativos.
- Interpretação e conclusão: seção específica no notebook e no dashboard.
