import os
import pandas as pd 
import plotly.graph_objects as go 
import plotly.express as px 
import streamlit as st
from datetime import datetime
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt


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

# Question 3: What subsection of Admin is so costly? 
# Column renaming
column_names = {
    'compnsatncurrofcr': 'Compensation of Officers',
    'officexpns': 'Office Expenses',
    'insurance': 'Insurance',
    'occupancy': 'Occupancy',
    'accntingfees': 'Accounting Fees',
    'legalfees': 'Legal Fees',
    'feesforsrvcmgmt': 'Management Service Fees',
    'feesforsrvcinvstmgmt': 'Investment Management Fees',
    'othrsalwages': 'Other Salaries and Wages',
    'payrolltx': 'Payroll Taxes',
    'pensionplancontrb': 'Pension Plan Contributions',
    'othremplyeebenef': 'Other Employee Benefits',
    'infotech': 'Information Technology',
    'compnsatnandothr': 'Compensation and Other Benefits',
    'travelofpublicoffcl': 'Travel and Entertainment for Public Officials',
    'benifitsmembrs': 'Benefits to Members'
}
df_expenses.rename(columns=column_names, inplace=True)
mean_admin_exp = df_expenses[list(column_names.values())].mean()
med_admin_exp = df_expenses[list(column_names.values())].median()
def millions_formatter(x, pos):
    if x >= 1e9:  # For billions
        return f'{x * 1e-9:.1f}B'
    elif x >= 1e6:  # For millions
        return f'{x * 1e-6:.1f}M'
    else:
        return int(x)

def create_bar_chart(df_expenses, statistic='mean'):
    if statistic == 'mean':
        data = df_expenses[list(column_names.values())].mean().sort_values()
        title = "Mean Admin General Expenses by Category"
    elif statistic == 'median':
        data = df_expenses[list(column_names.values())].median().sort_values()
        title = "Median Admin General Expenses by Category"

    fig = px.bar(data, orientation='h', title=title, labels={'index': 'Admin Category', 'value': statistic.capitalize() + ' Expenses'})
    fig.update_layout(xaxis_tickformat='s')
    return fig  


# Streamlit UI
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: rgb(0, 102, 0);
        color: white;
        border: 2px solid white;
    }
    div.stButton > button:first-child:hover {
        background-color: rgb(0, 153, 0);
        color: white;
        border: 2px solid white;
    }
    div.stRadio > div:checked {
        background-color: rgb(0, 102, 0);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title('Non-Profit Financial Dashboard')
st.write("This dashboard displays financial data extracted from Form 990 tax filings.")

# Display data head
if st.button('Show Data'):
    st.write(df.head()) 

st.write(f"Question 1: What is the mean expenses for tax exempt orgs over the last 3 years? ")
st.write(f"{formatted_mean_expense}")

st.write(f"Question 2: What is the mean/median percentage breakdown of expenses by category?  ")
statistic2 = st.radio('Select Statistic', ['mean', 'median'], key=['radio1'])
fig = create_pie_chart(df_expenses, statistic2)
st.plotly_chart(fig)

st.write(f"Question 3: What subsection of Admin is so costly? ")
statistic3 = st.radio('Select Statistic', ['mean', 'median'], key=['radio2'])
fig = create_bar_chart(df_expenses, statistic3)
st.plotly_chart(fig)
