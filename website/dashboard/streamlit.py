import os
import pandas as pd 
import plotly.graph_objects as go 
import plotly.express as px 
import streamlit as st
from datetime import datetime


# Load and preprocess data
@st.cache_data  
def load_data():
    df = pd.read_csv('../../data/form990_embf.csv')
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

df = load_data()

# Define expense categories
def process_expenses(df):
    df_expenses = df[[
        'accntingfees', 'advrtpromo', 'benifitsmembrs', 'compnsatncurrofcr',
        'compnsatnandothr', 'converconventmtng', 'deprcatndepletn', 'grntstogovt',
        'grnsttoindiv', 'grntstofrgngovt', 'infotech', 'insurance',
        'feesforsrvcinvstmgmt', 'legalfees', 'feesforsrvclobby', 'feesforsrvcmgmt',
        'occupancy', 'officexpns', 'othremplyeebenef', 'othrexpnsa', 'othrexpnsb',
        'othrexpnsc', 'othrexpnsd', 'othrexpnse', 'othrexpnsf', 'feesforsrvcothr',
        'othrsalwages', 'pymtoaffiliates', 'payrolltx', 'pensionplancontrb',
        'profndraising', 'royaltsexpns', 'totfuncexpns', 'travel',
        'travelofpublicoffcl','lessdirfndrsng']]
    
    # Calculations for streamlit
    columns_to_sum = df_expenses.columns.drop(['totfuncexpns', 'lessdirfndrsng'])
    df_expenses['sum_expenses'] = df_expenses[columns_to_sum].sum(axis=1)

    # Categorical sums
    df_expenses['mission_related'] = df_expenses[['grntstogovt','grnsttoindiv','grntstofrgngovt','converconventmtng']].sum(axis=1)
    df_expenses['admin_general'] = df_expenses[['compnsatncurrofcr','officexpns','insurance','occupancy']].sum(axis=1)  # trimmed for brevity
    df_expenses['fundraising'] = df_expenses[['profndraising','advrtpromo','lessdirfndrsng']].sum(axis=1)
    df_expenses['other'] = df_expenses[['deprcatndepletn','travel']].sum(axis=1)  # trimmed for brevity

    return df_expenses

# Create df
df_expenses = process_expenses(df)

# Question 1
mean_expense = round(df_expenses.totfuncexpns.mean()) 
formatted_mean_expense = "{:,}".format(mean_expense)

# Question 2
def create_pie_chart(df_expenses, statistic='mean'):
    if statistic == 'mean':
        sizes = [df_expenses['mission_related'].mean(), df_expenses['admin_general'].mean(), 
                 df_expenses['fundraising'].mean(), df_expenses['other'].mean()]
    elif statistic == 'median':
        sizes = [df_expenses['mission_related'].median(), df_expenses['admin_general'].median(),
                 df_expenses['fundraising'].median(), df_expenses['other'].median()]

    labels = ['Mission Related', 'Admin General', 'Fundraising', 'Other']
    fig = px.pie(values=sizes, names=labels, title=f'Proportion of {statistic.capitalize()} Organization Expenses')
    return fig 


# Streamlit UI
st.title('Non-Profit Financial Dashboard')
st.write("This dashboard displays financial data extracted from Form 990 tax filings.")

# Display data head
if st.button('Show Data'):
    st.write(df.head()) 

st.write(f"Question 1: What is the mean expenses for tax exempt orgs over the last 3 years? ")
st.write(f"{formatted_mean_expense}")

st.write(f"Question 2: What is the mean/median percentage breakdown of expenses by category?  ")

# Buttons for different statistics
if st.button('Show Mean Expenses Pie Chart'):
    fig_mean = create_pie_chart(df_expenses, 'mean')
    st.plotly_chart(fig_mean)

if st.button('Show Median Expenses Pie Chart'):
    fig_median = create_pie_chart(df_expenses, 'median')
    st.plotly_chart(fig_median)
