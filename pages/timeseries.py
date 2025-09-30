#!/usr/bin/env python
# coding: utf-8

# Import libraries/packages

# In[1]:


import numpy as np
import pandas as pd
import dash
from dash import Dash, dcc, html, callback, Input, Output 
import plotly.express as px
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# Import data and create page layout

# In[2]:

df_disease_prev_heart = pd.read_csv('https://raw.githubusercontent.com/healthbiodatascientist/heart_health/refs/heads/main/heart_prev_timeseries.csv')
df_disease_prev_heart = df_disease_prev_heart.drop(columns='Unnamed: 0')


layout = dbc.Container([
    html.H1("Prevalence of Heart Disease Related factors in Scottish Health Boards 2022-2025", className='mb-2', style={'textAlign':'center'}),
    html.Summary("The graph and grid below display publicly available data from Public Health Scotland (PHS), National Records of Scotland and the Scottish Government on the prevalence of heart disease related factors plus other factors which may be of importance from 2022-2025. It has been recorded by GP Practices in Scotland for each of their Regional NHS Health Boards. Choose a health board and the heart disease related factors that you are interested in from the lists below:", className='mb-2', style={'textAlign':'center', 'list-style': 'none', 'margin-top': '1em', 'padding': '10px 10px'}),
    dbc.Row([dbc.Col([dcc.Dropdown(id='healthboard', value='Ayrshire and Arran', clearable=False, options=np.unique(df_disease_prev_heart['Health Boards'].values)) ], style={'margin-top': '1em', 'padding': '10px 10px'}),
             dbc.Col([dcc.Dropdown(id='category', multi=True, clearable=False, options=df_disease_prev_heart.columns[2:14])])]),
    dbc.Row([dbc.Col([dcc.Graph(id='line-graph-plotly', figure={} ,style={'width': '120vh', 'height': '90vh', 'textAlign':'center'})]),
    html.H4("Potential Data Patterns", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Most Scottish Health Board Regions have seen a small rise in the prevalence rate of Atrial Fibrillation since 2021/22. The small population of the Western Isles recorded the highest rates in 2024/25"),
    html.Summary("There is no clear pattern of increases or decreases across Scotland in the prevalence of Chronic Kidney Disease. The Western Isles has the highest prevalence rate of this condition, although it has decreased sice 2022. Orkney and Lothian both saw rises in prevalence over 2022-25"),
    html.Summary("Most Scottish Health Board Regions have seen either a small decrease or a stabilisation in the prevalence rate of Coronary Heart Disease since 2021/22, with the exception of the small population on Shetland. The Western Isles recorded the highest prevalence of this condition in Scotland in 2024/25"),
    html.Summary("All Scottish Health Board Regions have seen a rise in the prevalence of Diabetes since 2021/22. The regions with the highest prevalence in 2024/25 are Ayrshire and Arran, Dumfries and Galloway and the Western Isles"),
    html.Summary("Most Scottish Health Board Regions have seen either a small increase or a stabilisation in the prevalence rate of Heart Failure. The region with the highest prevalence in 2024/25 is the Western Isles"),
    html.Summary("All Scottish Health Board Regions have seen a small rise in the prevalence of Hypertension or high blood pressure since 2021/22. The Western Isles recorded the highest prevalence of this condition in 2024/25"),
    html.Summary("Most Scottish Health Board Regions have seen either a small decrease or a stabilisation in the prevalence rate of Peripheral Arterial Disease since 2021/22. The region with the highest prevalence rate in 2024/25 was the Western Isles"),
    html.Summary("The only publicly available Scottish Health Board Regional data related to obesity is for primary 1s and is based on Body Mass Index (BMI). This data shows that there is no clear pattern of increases or decreases across Scotland for the percentage of children who have been classed as epidemiologically overweight or obese. The highest percentage of children in this category were found in Orkney in the 2023/24 school year and they along with Fife seem to have an increasing percentage of children in this category recently"),
    html.Summary("The levels of deprivation in the Scottish Health Board regions as whole are relatively stable over time, although each region will have specific areas with either lower or higher deprivation than the average. Ayrshire and Arran is the Scottish Health Board Region with the highest level of deprivation on average"),
    html.Summary("The median age of the residents in the Scottish Health Board regions are relatively stable over time, with the average age of residents showing a very slight increase. The regions with the highest median age of resident are the Western Isles and Dumfries and Galloway"),
    html.Figcaption("Table 1: Prevalence of Heart Disease related factors data for the Scottish Health Board Regions 2022-2025", className='mb-2', style={'margin-bottom': '1em', 'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col([dag.AgGrid(id='grid', rowData=df_disease_prev_heart.to_dict("records"), columnDefs=[{"field": i} for i in df_disease_prev_heart.columns], columnSize="autoSize")])]),
             ], className='mt-4'),
    html.H4("Open Data References", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Public Health Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://publichealthscotland.scot/publications/general-practice-disease-prevalence-data-visualisation/general-practice-disease-prevalence-visualisation-8-july-2025/")),
    html.Li(html.Cite("https://publichealthscotland.scot/media/34174/diseaseprevalence_methodology_and_metadata_2025-for-publication.pdf")),
    html.Li(html.Cite("https://www.opendata.nhs.scot/dataset/01fe4008-23f8-4b34-b8f6-c38699a2f00d/resource/2cb9d907-7149-4bbd-904a-174f15344585/download/od_p1bmi_hb_epi.csv")),
    html.Summary("National Records of Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.nrscotland.gov.uk/publications/population-estimates-time-series-data/")),
    html.Summary("Scottish Government", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.gov.scot/publications/scottish-surveys-core-questions-2023/")),
    html.Li(html.Cite("https://www.gov.scot/publications/scottish-surveys-core-questions-2022/"))
])

@callback(
    Output('line-graph-plotly', 'figure'),
    Output('grid', 'defaultColDef'),
    Input('healthboard', 'value'),
    Input('category', 'value'),
    prevent_initial_call=True    
)

def plot_data(healthboard, selected_yaxis):

    # Build the matplotlib figure
    df_disease_prev_heart = pd.read_csv('https://raw.githubusercontent.com/healthbiodatascientist/heart_health/refs/heads/main/heart_prev_timeseries.csv')
    df_disease_prev_heart = df_disease_prev_heart.loc[df_disease_prev_heart['Health Boards'] == healthboard] # filter for healthboard

    # Build the Plotly figure
    fig_line_plotly = px.line(df_disease_prev_heart, x='Year', y=selected_yaxis, markers=True, title="Figure 1: Prevalence of Heart Disease related factors in "+healthboard+" 2022-2025").update_xaxes(tickangle=330, automargin=True)
    fig_line_plotly.update_layout(yaxis_range=[0, None], legend=dict(yanchor='middle', y=0.5))

    my_cellStyle = {
        "styleConditions": [
            {
                "condition": f"params.colDef.field == '{selected_yaxis}'",
                "style": {"backgroundColor": "#d3d3d3"},
            },
            {   "condition": f"params.colDef.field != '{selected_yaxis}'",
                "style": {"color": "black"}
            },
        ]
    }

    return fig_line_plotly, {'cellStyle': my_cellStyle} 
