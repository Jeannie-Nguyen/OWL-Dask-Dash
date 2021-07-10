import os
import dask
import dask.dataframe as dd
import modin.pandas as pd
import numpy as np
import datetime as dt
from glob import glob

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


dataset=dd.read_csv(os.path.join("Overwatch", "phs_*.csv"), parse_dates=["start_time"]).sort_values("start_time").reset_index(drop=True)
df=dataset[(dataset.stage!="OWL APAC All-Stars") & (dataset.stage!="OWL North America All-Stars") & (dataset.hero!="All Heroes")]
df_sub=df[df.stat_name=="Time Played"]

hero_maptime=df_sub.groupby([df_sub.map_type, df_sub.start_time.dt.to_period("Y"), df_sub.hero]).stat_amount.sum().compute().reset_index()
tank=["D.Va", "Orisa", "Reinhardt", "Roadhog", "Sigma", "Winston", "Wrecking Ball", "Zarya"]
dps=["Ashe", "Bastion", "Doomfist", "Echo", "Genji", "Hanzo", "Junkrat", "McCree", "Mei", "Pharah", "Reaper", "Soldier: 76", "Sombra", "Symmetra", "Torbjörn", "Tracer", "Widowmaker"]
healer=["Ana", "Baptiste", "Brigitte", "Lúcio", "Mercy"," Moira", "Zenyatta"]

fig=go.Figure()
for year in hero_maptime.start_time.unique():
    frame=hero_maptime[hero_maptime.start_time==year]
    for i in [tank, dps, healer]:
        # f=frame[frame.hero.isin(i)]
#         f["percentage"]=0
#          for j in hero_maptime.map_type.unique():
#             f.percentage[f.map_type==j]=f[f.map_type==j].stat_amount/f.groupby("map_type").stat_amount.sum()[j]
    # fig=px.bar(frame, x="map_type", y="stat_amount", color="hero")
    # return fig
		fig.add_trace(go.bar(frame[frame.hero.isin(i)], x="map_type", y="stat_amount", color="hero")
	fig.show()

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])
# def display_graph(year):
#     fig = go.Figure(
#         data=go.Bar(y=[2, 3, 1], marker_color=color))
#     return fig

if __name__ == '__main__':
    app.run_server(debug=True)