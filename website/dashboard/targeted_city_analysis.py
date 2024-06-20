# Load in libraries
import pandas as pd
import plotly.express as px
import streamlit as st
import os
from tabulate import tabulate


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
data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_org_locals.csv')
df_org_locals = pd.read_csv(data_path)
#df_org_locals = pd.read_csv('../../data/df_org_locals.csv')

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'melted_city_funds.csv')
melted_city_funds = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'hypothesis_testing_results.csv')
hypothesis_testing_results = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_combined.csv')
df_combined = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_filing_percentage.csv')
df_filing_percentage = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_city_rulingyear.csv')
df_city_rulingyear = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_city_decade.csv')
df_city_decade = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_nteename_groupby.csv')
df_nteename_groupby = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_nteename_city_groupby.csv')
df_nteename_city_groupby = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_city_rulingname_all.csv')
df_city_rulingname_all = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_city_rulingname_grouped.csv')
df_city_rulingname_grouped = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_city_rulingname_env.csv')
df_city_rulingname_env = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_city_nteena_cluster.csv')
df_city_nteena_cluster = pd.read_csv(data_path)

data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'df_env_city_cluster.csv')
df_env_city_cluster = pd.read_csv(data_path)


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
fig_map.update_layout(height=700)
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
    height=500,
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
    ),
    height=500,
)
st.plotly_chart(fig_box, use_container_width=True)


##################################################
# Section 2: Financial Transparency and Accountability
st.header("Financial Transparency and Accountability")
st.subheader("How transparent are the financial activities or organizations in these cities?")
st.markdown("""
Understanding these ratios helps identify where the gaps in nonprofit reporting and formalization exist.""")

fig = px.bar(df_filing_percentage, x='CITY', y='Percentage_Not_Required_to_File', title='Percentage of Total EINs Not Required to File by City')
fig.update_layout(
    yaxis=dict(
        title='Percentage of Total EINs Not Required to File'
    ),
    xaxis=dict(
        title='City'
    ),
    height=500,
)
st.plotly_chart(fig, use_container_width=True)

##################################################
# Section 3: Trends over Time
st.header("Trends over Time")
st.subheader("How has the growth of nonprofit organizations evolved over time in these cities?")
st.markdown("""
Peaks in nonprofit creations during certain years - see below for analysis""")

view_option = st.selectbox("Select View:", ["Year", "Decade"])

if view_option == "Year":
    # Plot ruling year
    fig = px.line(df_city_rulingyear, x='RULING_YEAR', y='EIN')
    fig.update_layout(
        title='Number of Nonprofits in Targeted Cities by Ruling Year',
        xaxis=dict(title='Ruling Year'),
        yaxis=dict(title='Number of Nonprofits'),
        height=500,
    )
else:
    # Plot ruling decade
    fig = px.line(df_city_decade, x='RULING', y='EIN')
    fig.update_layout(
        title='Number of Nonprofits in Targeted Cities by Ruling Decade',
        xaxis=dict(title='Ruling Decade'),
        yaxis=dict(title='Number of Nonprofits'),
        height=500,
    )

# Display the plot
st.plotly_chart(fig, use_container_width=True)

st.subheader("Can we deduce historical events or trends in these cities by looking at the ruling date of organizations?")

st.markdown("""
### 1940s
- **World War II Era:** war relief, support for soldiers and their families.
- **Post-War Reconstruction:** rebuilding and providing aid.
### 1950s
- **Cold War** : emphasis on education, particularly in science and technology, National Defense Education Act (1958).
- **Desegregation:** Brown v. Board of Education - promote equal access to quality education for all students
### 1960s
- **Civil Rights Movement and War on Poverty:** creation of numerous organizations focused on civil rights, social justice, and economic equality.
- **Social Upheaval:** assassinations of Martin Luther King Jr. and Robert Kennedy, the escalation of the Vietnam War, and widespread protests, leading to the rise of nonprofits focused on social change, peace, and justice.
### 1970s
- **Environmental Movement:** first Earth Day in 1970 and the etablishment of the EPA.
- **Women’s Rights:** passage of Title IX.
### 1980s
- **Reagan Era:** welfare/housing budget cuts, Reaganomics, 1986 Immigration Reform and Control Act.
- **Public Health:** HIV/AIDS Crisis.
### Early 2000s
- **Post-Recession Recovery and Social Media Boom:** nonprofits focusing on economic recovery, digital advocacy.
- **Climate Change Awareness:** Al Gore's "An Inconvienient Truth," Kyoto Protocol (2005), use of solar tech, Hurricane Katrina (2005) ** 
### 2010s
- **Social Upheaval:** acquittal of Trayvon Martin's shooter, deaths of Michael Brown, Eric Garner, and George Floyd among others.
- **COVID-19 Pandemic:** non profits providing healthcare, economic relief.
""")
st.subheader("How have policy changes specific to these cities impacted the establishment of nonprofit organizations?")

st.subheader("Can we use the nonprofit categories (NTEE Codes) to help explain this futher?")
# plot group by name and count
fig = px.bar(df_nteename_groupby, x='EIN',y='NTEE_NAME')
fig.update_layout(
    title='NTEE Name Distribution',
    xaxis=dict(title='Number of Nonprofits'),
    yaxis=dict(title='NTEE Name'),
    width=1000,
    height=600,)
st.plotly_chart(fig, use_container_width=True)

# plot by city and name
fig = px.bar(df_nteename_city_groupby, x='CITY',y='EIN', color='NTEE_NAME',barmode='group')
fig.update_layout(
    title='NTEE Name Distribution by City',
    xaxis=dict(title='City'),
    yaxis=dict(title='Number of Nonprofits'),
    width=1000,
    height=500,)
st.plotly_chart(fig, use_container_width=True)


# NTEE Name Distribution by Ruling Years of Interest
view_option = st.selectbox("Select View:", ["Top 5 Nonprofits", "Environment & Civil Rights Focused"])

if view_option == "Top 5 Nonprofits":
    fig = px.line(df_city_rulingname_all, x='RULING_YEAR',y='EIN', color='NTEE_NAME')
    fig.update_layout(
        title='Top 5 NTEE Distribution by Ruling Years',
        xaxis=dict(title='Ruling Year'),
        yaxis=dict(title='Number of Nonprofits'),
        width=1000,
        height=600,)
    st.plotly_chart(fig, use_container_width=True)

# Targeted NTEE Name Distribution by Ruling Year
else:
    fig = px.line(df_city_rulingname_grouped, x='RULING_YEAR',y='EIN', color='NTEE_NAME')
    fig.update_layout(
        title='Environmental & Civil Rights NTEE Distribution by Ruling Year',
        xaxis=dict(title='Ruling Year'),
        yaxis=dict(title='Number of Nonprofits'),
        width=1000,
        height=600,)
    st.plotly_chart(fig, use_container_width=True)

##################################################
# Section 4: ML Trends
st.header("Machine Learning Focus")
st.subheader("Can we segment organizations into distinct clusters based on their financial health indicators (assets, income, revenue)?")
st.markdown("""
XXXX""")
df_city_nteena_cluster["CLUSTER_KMEANS"] = df_city_nteena_cluster["CLUSTER_KMEANS"].astype(str)
df_env_city_cluster["CLUSTER_KMEANS"] = df_env_city_cluster["CLUSTER_KMEANS"].astype(str)

view_option = st.selectbox("Select View:", ["All nonprofits", "Environmental and civil rights nonprofits"])

if view_option == "All nonprofits":
    fig = px.scatter_3d(df_city_nteena_cluster, 
                    x='ASSET_AMT', 
                    y='INCOME_AMT', 
                    z='REVENUE_AMT', 
                    color='CLUSTER_KMEANS',
                    color_discrete_sequence=px.colors.qualitative.G10,
                    hover_data={'NTEE_NAME': True, 'NAME': True})
    fig.update_layout(
        title='3D Clusters of All Organizations by Financial Health',
        scene = dict(
                        xaxis_title='Asset Amount',
                        yaxis_title='Income Amount',
                        zaxis_title='Revenue Amount',
                    ),
        width=700,
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

if view_option == "Environmental and civil rights nonprofits":
    fig = px.scatter_3d(df_env_city_cluster, 
                    x='ASSET_AMT', 
                    y='INCOME_AMT', 
                    z='REVENUE_AMT', 
                    color='CLUSTER_KMEANS',
                    color_discrete_sequence=px.colors.qualitative.G10,
                    hover_data={'NTEE_NAME': True, 'NAME': True})
    fig.update_layout(
        title='3D Clusters of Environmental and Civil Rights Organizations by Financial Health',
        scene = dict(
                        xaxis_title='Asset Amount',
                        yaxis_title='Income Amount',
                        zaxis_title='Revenue Amount',
                    ),
        width=700,
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("What is the distribution of environmental and civil rights nonprofits across the clusters?")
ntee_distribution = df_env_city_cluster.groupby(['CLUSTER_KMEANS', 'NTEE_NAME']).size().unstack().fillna(0).reset_index()
ntee_distribution_melt = ntee_distribution.melt(id_vars=['CLUSTER_KMEANS'], value_vars=['Civil Rights, Social Action & Advocacy','Environment'], var_name='NTEE',value_name='Number of Nonprofits')
fig= px.bar(ntee_distribution_melt, x='CLUSTER_KMEANS', y='Number of Nonprofits', color='NTEE', barmode='group')
fig.update_layout(title='Number of Environmental and Civil Rights Nonprofits by Cluster (Log Transformed)',
                  xaxis=dict(title='Cluster'),
                  yaxis=dict( type='log'),
                  width=800,    
                  height=500,)
st.plotly_chart(fig, use_container_width=True)



st.subheader("Which clusters of organizations have the highest potential financial impact?")
view_option = st.selectbox("Select View:", ["Among all nonprofits", "Among environmental and civil rights nonprofits"])

if view_option == "Among all nonprofits":
    cluster_analysis = df_city_nteena_cluster.groupby('CLUSTER_KMEANS')[['ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT']].median().reset_index()
    cluster_analysis_melt = cluster_analysis.melt(id_vars=['CLUSTER_KMEANS'], value_vars=['INCOME_AMT', 'ASSET_AMT', 'REVENUE_AMT'], var_name='FUND_TYPE', value_name='AMOUNT')
    fig= px.bar(cluster_analysis_melt, x='CLUSTER_KMEANS', y='AMOUNT', color='FUND_TYPE', barmode='group')
    fig.update_layout(title='KMeans Clusters by Median Funding Amount',
                    xaxis=dict(title='Cluster'),
        yaxis=dict(title='Amount (Log Transformed)', type='log'),  # Log transformation 
        width=1000,
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)

if view_option == "Among environmental and civil rights nonprofits":
    cluster_analysis = df_env_city_cluster.groupby('CLUSTER_KMEANS')[['ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT']].median().reset_index()
    cluster_analysis_melt = cluster_analysis.melt(id_vars=['CLUSTER_KMEANS'], value_vars=['INCOME_AMT', 'ASSET_AMT', 'REVENUE_AMT'], var_name='FUND_TYPE', value_name='AMOUNT')
    fig= px.bar(cluster_analysis_melt, x='CLUSTER_KMEANS', y='AMOUNT', color='FUND_TYPE', barmode='group')
    fig.update_layout(title='KMeans Clusters by Median Funding Amount',
                    xaxis=dict(title='Cluster'),
        yaxis=dict(title='Amount (Log Transformed)', type='log'),  # Log transformation 
        width=1000,
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)


st.subheader("What nonprofits fall into clusters identified as having highest potential financial impact?")
df_names_highfinance = df_env_city_cluster[(df_env_city_cluster['CLUSTER_KMEANS']=='1') | (df_env_city_cluster['CLUSTER_KMEANS']=='2')]
df_names_highfinance = df_names_highfinance[['NAME', 'CITY', 'NTEE_NAME','CLUSTER_KMEANS']]
markdown_table = tabulate(df_names_highfinance, headers='keys', tablefmt='pipe', showindex=False)
st.markdown(markdown_table)