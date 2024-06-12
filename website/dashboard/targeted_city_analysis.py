# Load in libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN, KMeans
import optuna

# Streamlit layout
st.set_page_config(page_title="Philanthropic Fund Analysis", layout="wide")

# Set title and description
st.title("Philanthropic Analysis in Cities of Interest")
st.markdown("""
This dashboard provides an overview of philanthropic funds in various cities that are US based, contain a presence of Environmental Justice (EJ) communities,
            and individuals who engage with digital divide and climate change. 
The following analysis includes a density map of EINs, a breakdown of philanthropic fund types by city, and the results of hypothesis testing on fund amounts.
""")

# Load in data
df_org_locals = pd.read_csv('../../data/df_org_locals.csv')
melted_city_funds = pd.read_csv('../../data/melted_city_funds.csv')
hypothesis_testing_results = pd.read_csv('../../data/hypothesis_testing_results.csv')
df_combined = pd.read_csv('../../data/df_combined.csv')

# Create the scatter plot of EINs and cities
fig_map = px.scatter_mapbox(
    df_org_locals,
    lat='Latitude',
    lon='Longitude',
    size='COUNT',
    hover_name='CITY',
    hover_data={'COUNT': True, 'Latitude': False, 'Longitude': False},
    size_max=15,
    zoom=3,
    mapbox_style='carto-positron',
    title='Density Map of EINs in Selected Cities'
)

# Display the map in a wide column
st.plotly_chart(fig_map, use_container_width=True)

##################################################
# Section 1: Distribution and Allocation of Funds
st.header("Distribution and Allocation of Funds")


###########
# Section 1: Distribution of finances by city 
st.subheader("How are philanthropic finances distributed across these cities?")
st.markdown("""
Despite Chicago and Washington having the highest number of nonprofits, 
            the chart below shows that Washington and Seattle have the 
            largest income, asset and revenue amounts on a median scale.
""")
fig_bar = px.bar(melted_city_funds, x='CITY', y='AMOUNT', color='FUND_TYPE', barmode='group')
fig_bar.update_layout(title='Median Nonprofit Financial Breakdown By City',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='USD (billions)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
        title='City'
    ),
    legend=dict(
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1  # gap between bars of the same location coordinate.
)

# Display the bar plot in a wide column
st.plotly_chart(fig_bar, use_container_width=True)

###########
# Section 1: Fund hypothesis testing
st.subheader("Are there significant differences in the allocation of funds between these cities engaged in addressing the digital divide and climate change compared to those that are not?")
st.markdown("""
The hypothesis testing results in the table below indicate high T-stats and below 0.5 P-stats. This confirms that there are statistically significant differences in income, asset, and revenue amounts between cities engaged in addressing the digital divide and climate change and those that are not.
""")
st.table(hypothesis_testing_results)

###########
# Section 1: Comparison of Funding Types bt target and non target cities
st.subheader("How does income compare between targeted and non-targeted cities?")
st.markdown("""
Cities of interest/target evaluation are labeled with the number 1. The boxplot below shows cities of interest generally have higher and more consistent levels of income.
""")
fig_box = px.box(
    df_combined[df_combined['FUND_TYPE'] == 'INCOME_AMT'],
    x='CITY_TARGET',
    y='AMOUNT',
    title='Comparison of Income between Targeted and Non-Targeted Cities'
)

fig_box.update_layout(
    yaxis=dict(type='log', title='Amount (log scale)'),
    xaxis=dict(title='City Target (1 = Yes, 0 = No)'),
    title=dict(
        text='Comparison of Income between Targeted and Non-Targeted Cities',
        x=0.5,
        xanchor='center'
    )
)
st.plotly_chart(fig_box, use_container_width=True)
