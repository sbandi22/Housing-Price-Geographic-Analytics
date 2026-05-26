"""Tableau-style interactive dashboard built with Plotly Dash.

Run:
    python dashboards/app.py
Then browse to http://localhost:8050
"""
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output

from src.utils.config import RAW_DIR

SAMPLE = RAW_DIR / 'sample_housing.csv'


def load_data() -> pd.DataFrame:
    if SAMPLE.exists():
        return pd.read_csv(SAMPLE)
    # Fallback synthetic data
    import numpy as np
    rng = np.random.default_rng(42)
    n = 500
    return pd.DataFrame({
        'state_code': rng.choice(['CA','TX','NY','FL','WA','IL','CO','GA','MA','AZ'], n),
        'sale_price': rng.lognormal(12.7, 0.4, n).round(),
        'sqft_living': rng.integers(700, 4500, n),
        'bedrooms':    rng.integers(1, 6, n),
        'year_built':  rng.integers(1950, 2024, n),
        'latitude':    rng.uniform(25, 49, n),
        'longitude':   rng.uniform(-124, -67, n),
    })


DF = load_data()
STATES = sorted(DF['state_code'].dropna().unique())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], title='Housing Analytics')

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2('🏘️  Housing Price & Geographic Analytics'),
                    width=12), class_name='my-3'),
    dbc.Row([
        dbc.Col([
            html.Label('State'),
            dcc.Dropdown(id='state', options=[{'label': s, 'value': s} for s in STATES],
                         multi=True, placeholder='All states'),
        ], md=4),
        dbc.Col([
            html.Label('Price range (USD)'),
            dcc.RangeSlider(id='price', min=int(DF['sale_price'].min()),
                            max=int(DF['sale_price'].max()),
                            value=[int(DF['sale_price'].min()), int(DF['sale_price'].max())],
                            tooltip={'placement': 'bottom'}),
        ], md=8),
    ], class_name='mb-3'),
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardHeader('Median Price'),
                          dbc.CardBody(id='kpi-median')]), md=3),
        dbc.Col(dbc.Card([dbc.CardHeader('Avg \u0024 / sqft'),
                          dbc.CardBody(id='kpi-ppsf')]), md=3),
        dbc.Col(dbc.Card([dbc.CardHeader('Listings'),
                          dbc.CardBody(id='kpi-count')]), md=3),
        dbc.Col(dbc.Card([dbc.CardHeader('States covered'),
                          dbc.CardBody(id='kpi-states')]), md=3),
    ], class_name='mb-3'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='choropleth'), md=6),
        dbc.Col(dcc.Graph(id='price-distribution'), md=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='price-vs-sqft'), md=6),
        dbc.Col(dcc.Graph(id='avg-by-state'),  md=6),
    ]),
], fluid=True)


@app.callback(
    Output('kpi-median', 'children'),
    Output('kpi-ppsf', 'children'),
    Output('kpi-count', 'children'),
    Output('kpi-states', 'children'),
    Output('choropleth', 'figure'),
    Output('price-distribution', 'figure'),
    Output('price-vs-sqft', 'figure'),
    Output('avg-by-state', 'figure'),
    Input('state', 'value'),
    Input('price', 'value'),
)
def update(states, price_range):
    df = DF.copy()
    if states:
        df = df[df['state_code'].isin(states)]
    if price_range:
        df = df[(df['sale_price'] >= price_range[0]) & (df['sale_price'] <= price_range[1])]

    if df.empty:
        empty = px.scatter(title='No data')
        return ('-', '-', '0', '0', empty, empty, empty, empty)

    median = f"\u0024{int(df['sale_price'].median()):,}"
    ppsf   = f"\u0024{(df['sale_price']/df['sqft_living']).mean():.0f}"
    count  = f"{len(df):,}"
    nstates = str(df['state_code'].nunique())

    state_agg = df.groupby('state_code', as_index=False)['sale_price'].mean()
    chor = px.choropleth(state_agg, locations='state_code', locationmode='USA-states',
                         color='sale_price', scope='usa',
                         color_continuous_scale='Viridis',
                         title='Average Sale Price by State')
    dist = px.histogram(df, x='sale_price', nbins=40, title='Price Distribution')
    scat = px.scatter(df, x='sqft_living', y='sale_price', color='state_code',
                      trendline='ols', title='Price vs. Living Sqft')
    bar  = px.bar(state_agg.sort_values('sale_price', ascending=False),
                  x='state_code', y='sale_price', title='Avg Price by State')
    return median, ppsf, count, nstates, chor, dist, scat, bar


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
