# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel(r'C:\Users\imran\Downloads\Hospice data from Board Charts 1.1.2016_6.30.2020.xlsx')
long_df = pd.melt(df, id_vars=['Months', 'Year'], value_vars=['#Pts Served', 'PCF(ADC)', 'ALOS', 'Admissions'])
long_df_served = long_df.loc[long_df['variable'] == '#Pts Served']
long_df_pcf = long_df.loc[long_df['variable'] == 'PCF(ADC)']
long_df_alos = long_df.loc[long_df['variable'] == 'ALOS']
long_df_admissions = long_df.loc[long_df['variable'] == 'Admissions']

year_indicators = long_df['Year'].unique()
variable_indicators = long_df['variable'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': i, 'value': i} for i in year_indicators],
                value='Select Year'
            )],
            style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='variable-column',
                options=[{'label': i, 'value': i} for i in variable_indicators],
                value='Select Metric'
            )],
            style = {'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='hospicare-graphic')])])

@app.callback(
    Output('hospicare-graphic', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('variable-column', 'value')])
def update_graph(year_value, metric_name):
    dff = long_df[long_df['Year'] == year_value]
    #fig = px.scatter(x=list(dff.Months),
                     #y=list(dff[dff['variable'] == metric_name]['value']))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(dff.Months), y=list(dff[dff['variable'] == metric_name]['value']), mode='lines+markers', line=dict(color = '#57664b')))
    fig.update_layout(
        plot_bgcolor='#e2dbda',
        xaxis_title = "Month",
        yaxis_title = "Results",
        font=dict(size = 18, color = '#684e3f', family = 'Times New Roman'),
        title={'text':'Hospicare Metrics','y':0.9, 'x':0.5},
        xaxis_showgrid=False, yaxis_showgrid=True

    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

