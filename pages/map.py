#!/usr/bin/env python
# coding: utf-8

# Import libraries/packages

# In[1]:


import pandas as pd
import dash
from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# Import data and create tables

# In[2]:


def no_geometry():
    df_heart_prev_mapped = pd.read_csv('https://raw.githubusercontent.com/healthbiodatascientist/heart_health/refs/heads/main/heart_prev_mapped.csv')
    df_heart_prev_mapped = df_heart_prev_mapped.set_index('HBCode')
    df_no_geometry = df_heart_prev_mapped.drop('geometry', axis=1)
    return df_no_geometry
df_hb_beds_table = no_geometry()
df_numeric_columns = df_no_geometry.select_dtypes('number')


# Create page layout

# In[3]:
    
layout = dbc.Container([
    html.H1("Heart Disease Related Prevalence in Scotland's Regional Health Boards 2021/22 to 2024/25", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(html.Summary("The map below displays open source heart disease related data from Public Health Scotland (PHS), National Records of Scotland (NRS) and the Scottish Government for each of the Scottish Health Board Regions. Hover over your Health Board for an insight into the factors affecting heart disease in your area:", className='mb-2', style={'padding': '10px 10px', 'list-style': 'none'}))]),
    dbc.Row([dbc.Col(html.Iframe(id='my_output', height=600, width=1000, srcDoc=open('heartprevmap.html', 'r').read()))], style={'text-align':'center'}),
    html.Figcaption("Figure 1: Map of the latest heart-related disease open health data for the Scottish Health Board Regions", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    html.H4("Potential Data Relationships", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Prevalence is how common a disease is in a population. If in a GP practice with 10,000 patients 1,000 meet the conditions for the cancer indicator, then this practice has a cancer prevalence of 10 per 100. In other words, prevalence rates represent how many people out of every 100 are recorded as having a particular disease.", className='mb-2'),
    html.Summary("Atrial fibrillation (AF) is an irregular and often rapid heart rhythm that can be a symptom or complication of underlying heart disease, increasing the risk of stroke, heart failure, and other serious conditions", className='mb-2'),
    html.Summary("Risk factors for coronary heart disease (CHD) include modifiable lifestyle choices like smoking, unhealthy diet, lack of physical activity, and excessive alcohol intake, as well as health conditions such as high blood pressure, high cholesterol, and diabetes", className='mb-2'),
    html.Summary("Chronic kidney disease (CKD) and heart disease are strongly linked in a vicious cycle where one condition worsens the other, with heart disease being the leading cause of death in people with CKD", className='mb-2'),
    html.Summary("Diabetes significantly increases the risk of heart disease and stroke by damaging blood vessels and nerves", className='mb-2'),
    html.Summary("Heart failure risk factors include high blood pressure, coronary artery disease (often caused by high cholesterol and smoking), diabetes, obesity, physical inactivity, excessive alcohol use, and certain existing conditions like cardiomyopathy, sleep apnea, chronic kidney disease, and atrial fibrillation", className='mb-2'),
    html.Summary("Hypertension, or high blood pressure, significantly increases the risk of heart disease by straining and damaging blood vessels and the heart muscle, leading to conditions like coronary artery disease, heart attacks, heart failure, and enlarged heart chambers", className='mb-2'),
    html.Summary("Peripheral arterial disease (PAD) and heart disease, particularly coronary heart disease, are closely related because both are caused by the same underlying condition, atherosclerosis (fatty plaque buildup in arteries)", className='mb-2'),
    html.Summary("Childhood obesity is a significant risk factor for developing serious health issues, including heart disease, high blood pressure, and type 2 diabetes", className='mb-2'),
    html.Summary("The Scottish Index of Multiple Deprivation (SIMD) is a tool to measure geographic inequality in Scotland, with studies showing a link between high levels of deprivation (high SIMD scores) and increased risks or worse outcomes for heart and circulatory diseases", className='mb-2'),
    html.Summary("Coronary heart disease (CHD) risk significantly increases with age, becoming more prevalent after age 35 for both men and women, with men generally having a higher risk starting around age 45 and women's risk accelerating around age 55 after menopause", className='mb-2'),
    html.Figcaption("Table 1: Latest open heart disease related data for the Scottish Health Board Regions with the highest 50% of column values highlighted in dark pink", className='mb-2', style={'margin-bottom': '1em', 'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(dash_table.DataTable(
    data=df_hb_beds_table.to_dict('records'),
    sort_action='native',
    columns=[{'name': i, 'id': i} for i in df_hb_beds_table.columns],
    style_cell={'textAlign': 'center'},
    fixed_columns={'headers': True, 'data': 1},
    style_table={'minWidth': '100%'},
    style_data_conditional=
    [
            {
                'if': {
                    'filter_query': '{{{}}} > {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#AA336A',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.1).items()
        ] +       
        [
            {
                'if': {
                    'filter_query': '{{{}}} <= {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#FFC0CB',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.5).items()
        ]
    ))
    ]),
    html.H4("Open Data Links", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Public Health Scotland"),
    html.Li(html.Cite("https://publichealthscotland.scot/publications/general-practice-disease-prevalence-data-visualisation/general-practice-disease-prevalence-visualisation-8-july-2025/")),
    html.Li(html.Cite("https://publichealthscotland.scot/media/34174/diseaseprevalence_methodology_and_metadata_2025-for-publication.pdf")),
    html.Li(html.Cite("https://www.opendata.nhs.scot/dataset/01fe4008-23f8-4b34-b8f6-c38699a2f00d/resource/2cb9d907-7149-4bbd-904a-174f15344585/download/od_p1bmi_hb_epi.csv")),
    html.Summary("National Records of Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.nrscotland.gov.uk/publications/population-estimates-time-series-data/")),
    html.Summary("Scottish Government", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.gov.scot/publications/scottish-surveys-core-questions-2023/"))
    ])

