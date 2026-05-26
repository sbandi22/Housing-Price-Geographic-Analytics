"""Choropleth and Folium heatmap utilities."""
from pathlib import Path

import folium
import pandas as pd
import plotly.express as px
from folium.plugins import HeatMap

from src.utils.config import REPORTS_DIR


def plotly_state_choropleth(df: pd.DataFrame,
                            value_col: str = 'avg_sale_price',
                            state_col: str = 'state_code',
                            title: str = 'Average Housing Price by State') -> Path:
    fig = px.choropleth(
        df,
        locations=state_col,
        locationmode='USA-states',
        color=value_col,
        color_continuous_scale='Viridis',
        scope='usa',
        title=title,
        labels={value_col: 'USD'},
    )
    fig.update_layout(margin=dict(l=0, r=0, t=60, b=0))
    out = REPORTS_DIR / 'choropleth_state.html'
    fig.write_html(out)
    return out


def folium_point_heatmap(df: pd.DataFrame,
                         lat_col: str = 'latitude',
                         lon_col: str = 'longitude',
                         weight_col: str | None = 'sale_price',
                         zoom: int = 5) -> Path:
    center = [df[lat_col].mean(), df[lon_col].mean()]
    m = folium.Map(location=center, zoom_start=zoom, tiles='cartodbpositron')
    if weight_col and weight_col in df.columns:
        data = df[[lat_col, lon_col, weight_col]].dropna().values.tolist()
    else:
        data = df[[lat_col, lon_col]].dropna().values.tolist()
    HeatMap(data, radius=12, blur=18, max_zoom=12).add_to(m)
    out = REPORTS_DIR / 'point_heatmap.html'
    m.save(str(out))
    return out
