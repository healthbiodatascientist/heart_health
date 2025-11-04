#!/usr/bin/env python
# coding: utf-8

# Import packages/libraries

# In[1]:


import numpy as np
import pandas as pd
import dash
from dash import Dash, dcc, html, callback, Input, Output 
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# Import data

# In[2]:


df_disease_prev_heart_time = pd.read_csv('heart_prev_timeseries.csv')


# Create layout

# In[3]:

layout = dbc.Container([
    html.H1("Prevalence of Heart Disease Related factors in Scottish Health Boards 2022-2025", className='mb-2', style={'textAlign':'center'}),
    html.Summary("The trendline and heat maps below display the correlations between the heart disease related factors found in the data from Public Health Scotland (PHS), National Records of Scotland and the Scottish Government on the prevalence of heart disease related factors from 2022-2025. Choose the heart disease related factors that you are interested in from the lists below:", className='mb-2', style={'textAlign':'center', 'list-style': 'none', 'margin-top': '1em', 'padding': '10px 10px'}),
    dbc.Row([dbc.Col([dcc.Dropdown(id='category1', value='Rate_Hypertension', clearable=False, options=df_disease_prev_heart_time.columns[3:15])]),
             dbc.Col([dcc.Dropdown(id='category2', value='Rate_Heart Failure', clearable=False, options=df_disease_prev_heart_time.columns[3:15])])]),
    html.H4("Potential Data Patterns", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Lighter colours in the heatmap display higher prevalence values and it appears that in most cases higher rates of factors such as atrial fibrillation, hypertension and diabetes in a health board region do tend to correlate with higher rates of coronary heart disease and heart failure. Unfortunately the age and SIMD data for the population in each health board region has not been updated in 2025 as yet.", className='mb-2', style={'textAlign':'center', 'list-style': 'none', 'margin-top': '1em', 'padding': '10px 10px'}),
    dbc.Row([dbc.Col([dcc.Graph(id='heatmap-plotly-hb', figure={} ,style={'width': '120vh', 'height': '90vh', 'textAlign':'center'})])]),
    html.Summary("Choose a healthboard below to check if there is a correlation in your chosen heart disease related factors within the healthboard across 2022-2025", className='mb-2', style={'textAlign':'center', 'list-style': 'none', 'margin-top': '1em', 'padding': '10px 10px'}),
    html.H4("Potential Data Patterns", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("The correlation of the heart disease related factors over time in individual health board regions can be viewed via trendlines with higher R squared values (viewed via hovering over the Ordinary Least Squares generated trendline) showing a higher likelihood of a correlation between the two selected factors. However, since there are only a few data points, the heatmap should provide a clearer and more accurate picture of any potential data relationships.", className='mb-2', style={'textAlign':'center', 'list-style': 'none', 'margin-top': '1em', 'padding': '10px 10px'}),
    dbc.Row([dbc.Col([dcc.Dropdown(id='healthboard', value='Ayrshire and Arran', clearable=False, options=np.unique(df_disease_prev_heart_time['Health Boards'].values))], style={'margin-top': '1em', 'padding': '10px 10px'})]),
    dbc.Row([dbc.Col([dcc.Graph(id='trendline-graph-plotly', figure={} ,style={'width': '120vh', 'height': '90vh', 'textAlign':'center'})])]),
    dbc.Row([dbc.Col([dcc.Graph(id='heatmap-plotly-time', figure={} ,style={'width': '120vh', 'height': '90vh', 'textAlign':'center'})])]),
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
    Output('heatmap-plotly-hb', 'figure'),
    Output('trendline-graph-plotly', 'figure'),
    Output('heatmap-plotly-time', 'figure'),
    Input('healthboard', 'value'),
    Input('category1', 'value'),
    Input('category2', 'value'),
    
)

def plot_data(healthboard, selected_xaxis, selected_yaxis):

    # Build the matplotlib figure
    df_disease_prev_heart_time = pd.read_csv('heart_prev_timeseries.csv')
    df_disease_prev_heart_time = df_disease_prev_heart_time.round(2)
    df_disease_prev_heart_time_hb = df_disease_prev_heart_time.loc[df_disease_prev_heart_time['Health Boards'] == healthboard] # filter for healthboard
    df_disease_prev_heart_hb_heat = df_disease_prev_heart_time.loc[df_disease_prev_heart_time['Year'] == 2025]
    df_disease_prev_heart_hb_heat = df_disease_prev_heart_hb_heat.filter(items=['Health Boards', selected_xaxis, selected_yaxis])
    df_disease_prev_heart_hb_heat = df_disease_prev_heart_hb_heat.pivot_table(columns='Health Boards')
    df_disease_prev_heart_time_heat = df_disease_prev_heart_time_hb.filter(items=['Year', selected_xaxis, selected_yaxis])
    df_disease_prev_heart_time_heat = df_disease_prev_heart_time_heat.pivot_table(columns='Year')
    
    # Build the Plotly figure
    fig_heatmap_hb = px.imshow(df_disease_prev_heart_hb_heat, title="Figure 1: Heatmap of Heart Disease related factors in Scottish Health Boards in 2025").update_xaxes(tickangle=330, automargin=True)
    fig_heatmap_hb = fig_heatmap_hb.update_traces(text=df_disease_prev_heart_hb_heat.values, texttemplate="%{text}")
    fig_trendline_plotly = px.scatter(df_disease_prev_heart_time_hb, x=selected_xaxis, y=selected_yaxis, trendline='ols', title="Figure 2: Correlation of Heart Disease related factors in "+healthboard+" 2022-2025").update_xaxes(tickangle=330, automargin=True)
    fig_heatmap_time = px.imshow(df_disease_prev_heart_time_heat, title="Figure 3: Heatmap of Heart Disease related factors in "+healthboard+" 2022-2025").update_xaxes(tickangle=330, automargin=True)
    fig_heatmap_time = fig_heatmap_time.update_traces(text=df_disease_prev_heart_time_heat.values, texttemplate="%{text}")
    
    return fig_heatmap_hb, fig_trendline_plotly, fig_heatmap_time
