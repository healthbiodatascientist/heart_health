#!/usr/bin/env python
# coding: utf-8

# Import libraries/packages

# In[1]:


import pandas as pd
from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc


# Import data and create tables

# In[2]:


def no_geometry():
    df_heart_prev_mapped = pd.read_csv('https://raw.githubusercontent.com/healthbiodatascientist/heart_health/refs/heads/main/heart_prev_mapped.csv')
    df_heart_prev_mapped = df_heart_prev_mapped.set_index('HBCode')
    df_no_geometry = df_heart_prev_mapped.drop('geometry', axis=1)
    return df_no_geometry
df_no_geometry = no_geometry()
df_numeric_columns = df_no_geometry.select_dtypes('number')


# Create app layout

# In[3]:


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
app.layout = dbc.Container([
    html.H1("Heart Disease Related Prevalence in Scotland's General Practices by Regional Health Board 2024/25", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(html.Summary("The map below displays open source heart disease related data from Public Health Scotland (PHS) for each of the Scottish Health Board Regions. Click on or hover over over your Health Board for an insight into the factors affecting heart disease prevalence in your area:", className='mb-2', style={'padding': '10px 10px', 'list-style': 'none'}))]),
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
    html.Summary("Coronary heart disease (CHD) risk significantly increases with age, becoming more prevalent after age 35 for both men and women, with men generally having a higher risk starting around age 45 and women's risk accelerating around age 55 after menopause", className='mb-2'),
    html.Figcaption("Table 1: Latest open heart disease related data for the Scottish Health Board Regions with the highest 50% of column values highlighted in dark pink", className='mb-2', style={'margin-bottom': '1em', 'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(dash_table.DataTable(
    data=df_no_geometry.to_dict('records'),
    sort_action='native',
    columns=[{'name': i, 'id': i} for i in df_no_geometry.columns],
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
    html.Summary("Scotland's Census 2022 - National Records of Scotland"),
    html.Li(html.Cite("https://www.scotlandscensus.gov.uk/webapi/jsf/tableView/tableView.xhtml")),
    ])


# Run app

# In[4]:


if __name__ == "__main__":
    app.run()

