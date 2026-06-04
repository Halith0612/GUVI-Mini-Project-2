

# importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import mysql.connector
from sqlalchemy import create_engine
import time

# connecting with sql
mydb = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="3fXqCw6nxxduoS8.root",
    password="u2dctQHUVuOXcZhS",
    database="Global_Literacy"
)


# load data
@st.cache_data
def load_data():
    literacy = pd.read_sql("SELECT * FROM literacy_rates", mydb)
    illiteracy = pd.read_sql("SELECT * FROM illiteracy_population", mydb)
    gdp_schooling = pd.read_sql("SELECT * FROM gdp_schooling", mydb)
    return literacy, illiteracy, gdp_schooling

literacy, illiteracy, gdp_schooling = load_data()

st.set_page_config(page_title="Global Literacy and GDP ", layout="wide")

# side bar
st.sidebar.title("Menu")
page = st.sidebar.selectbox(
    "Options",
    [ "Project Overview", "SQL Query Executor", "EDA Visualizations", "Country Profile Page"])

if page == "Project Overview": # main page setup
  st.title("🧠💰Global Literacy and GDP Dashboard")
  st.subheader("Welcome to the Global Literacy Dashboard!👋")
  st.markdown("""This project is a data analysis and visualization dashboard that explores global literacy rates, illiteracy rates, and GDP trends across different countries over the years. The project was developed using SQL, Python, Pandas, and Streamlit to perform data analysis, execute SQL queries, and create interactive visualizations.
  The main objective of this project is to understand how literacy and education levels relate to economic growth and development in different regions of the world.

  ## Features
  * Analyze adult and youth literacy rates across countries
  * Compare male and female literacy rates by region
  * Track illiteracy trends over multiple years
  * Explore GDP and average years of schooling
  * Perform SQL-based analytical queries dynamically
  * Interactive visualizations using Plotly, Matplotlib, and Seaborn
  * Streamlit dashboard with multiple analysis pages
  ---
  ## Technologies Used
  * Python
  * Pandas
  * SQL / SQLite
  * Streamlit
  * Plotly Express
  * Matplotlib
  * Seaborn
  ---
  ## Key Analyses Performed

  ### Literacy Analysis
  * Top countries with highest literacy rates
  * Female literacy analysis
  * Region-wise literacy comparison
  * Literacy trends over years

  ### Illiteracy Analysis
  * Countries with high illiteracy rates
  * Illiteracy trend analysis
  * Country-wise comparison

  ### GDP and Education Analysis
  * Relationship between GDP and schooling
  * GDP per schooling analysis
  * Global schooling trends
---
  ## Project Outcome
  This project helps understand:
  * Global education development trends
  * Literacy growth across regions
  * Gender-based literacy differences
  * The relationship between education and economic growth
  ---
  ## Author
  Mohamed Halith M K
  """)

#page 1: sql query page
elif page == "SQL Query Executor":
  st.title("⚡💾 SQL Query Executor")
  st.markdown("""Dive into data exploration using SQL queries that reveal literacy patterns, economic growth, and educational progress worldwide.
  Also, Analyze global education and economic indicators with ready-to-use SQL queries, interactive tables, and insightful visualizations.""")

  from utils.sql import queries
  
  category = st.selectbox("Select Category", list(queries.keys()))
  query_name = st.selectbox("Select Query", list(queries[category].keys()))

  if st.button("Run Query"):
    with st.spinner("Running query..."):
      time.sleep(2)
    query_info = queries[category][query_name]
    query = query_info["query"]

    result = pd.read_sql(query, mydb)

    st.dataframe(result)

    st.subheader("📊 Query Visualization")
    chart_type = query_info["chart"]
    x_col = query_info["x"]
    y_col = query_info.get("y")

    # BAR
    if chart_type == "bar":
      fig = px.bar(result,
                   x=x_col,
                   y=y_col,
                   text_auto=True,
                   color=y_col
                   )

    elif chart_type == "line":
      fig = px.line(result,
                    x=x_col,
                    y=y_col,
                    markers=True)

    elif chart_type == "pie":
      fig = px.pie(result,
                   names=x_col,
                   values=y_col)

    elif chart_type == "scatter":
      fig = px.scatter(result,
                       x=x_col,
                       y=y_col)

    elif chart_type == "grouped_bar":
      fig = px.bar(result,
                   x=x_col,
                   y=[query_info["y1"], query_info["y2"]],
                   barmode="group"
                   )

    st.plotly_chart(fig, use_container_width=True)


# page 2:
elif page == "EDA Visualizations":

    st.title("📊 EDA Visualizations")
    st.markdown("Gain deeper understanding of global education data through exploratory charts, trends, and comparative visualizations.")

    eda_options = [
        "Adult & Youth Literacy Rate Over Years",

        "Region wise Male and Female Literacy Rate",

        "Adult Literacy during covid (2020 to 2023)",

        "Illiteracy Rate comparision betweeen selected countries over years",

        "Illiterates vs Literates trend over Years",

        "GDP per Avg Schooling",

        "Highest GDP countries literacy rate TOP 5 only",

        "Literacy Growth Rate over year - India.",

        "GDP Distribution Boxplot",

        "Correlation of Population and Literacy"
    ]

    eda_name = st.selectbox("Select Category",eda_options)

    def show_chart(fig):

        st.plotly_chart( fig, use_container_width=True)

    # 1
    if eda_name == "Adult & Youth Literacy Rate Over Years":
      adult_literacy = literacy.groupby("Year")["Adult"].mean()
      male_literacy = literacy.groupby("Year")["Male"].mean()
      female_literacy = literacy.groupby("Year")["Female"].mean()


      fig, ax = plt.subplots(figsize=(15, 8))

      ax.plot(male_literacy.index, male_literacy.values, label="Male")
      ax.plot(female_literacy.index, female_literacy.values, label="Female")
      ax.plot(adult_literacy.index, adult_literacy.values, label="Adult")

      ax.set_title("Avg Literacy Rate Over Years of Adult & Youth")
      ax.set_xlabel("Year")
      ax.set_ylabel("Literacy Rate")

      ax.legend()
      ax.grid(alpha=0.5)

      show_chart(fig)

    # 2
    elif eda_name == "Region wise Male and Female Literacy Rate":
      r_male_literacy = literacy.groupby("Region")["Male"].mean()
      r_female_literacy = literacy.groupby("Region")["Female"].mean()

      fig, ax = plt.subplots(figsize=(15,8))
      ax.plot(r_male_literacy.index, r_male_literacy.values, marker="o")
      ax.plot(r_female_literacy.index, r_female_literacy.values, marker="o")
      ax.set_title("Region Wise Trend")
      ax.set_xlabel("Region")
      ax.set_ylabel("Total_Youth")
      ax.grid(alpha=0.5)
      ax.legend(["Male", "Female"])

      st.pyplot(fig)

    # 3
    elif eda_name == "Adult Literacy during covid (2020 to 2023)":
      covid_year = literacy[(literacy["Year"] >= 2020) & (literacy["Year"] <= 2023)]
      adult_literacy = covid_year.groupby("Year", as_index=False)["Adult"].mean().round()

      fig, ax = plt.subplots(figsize=(15,8))

      sns.barplot(data=adult_literacy, x="Year", y="Adult", palette="dark", ax=ax)

      ax.set_title("Adult Literacy During COVID (2020 to 2023)")
      ax.set_xlabel("Year")
      ax.set_ylabel("Adult Literacy")
      ax.legend(loc="upper center")

      st.pyplot(fig)

    # 4
    elif eda_name == "Illiteracy Rate comparision betweeen selected countries over years":
      countries = ["Bangladesh", "China", "India", "Nepal", "Pakistan"]

      com_countries = illiteracy[illiteracy["Country"].isin(countries)]

      fig, ax = plt.subplots(figsize=(15, 8))

      sns.barplot(data=com_countries, x="Year", y="Illiteracy_rate", hue="Country", palette="magma", ax=ax)

      ax.set_title("Illiteracy Rate of Five Countries")
      ax.set_xlabel("Year")
      ax.set_ylabel("Illiteracy Rate")

      ax.legend(loc="upper right")
      ax.grid(False)

      st.pyplot(fig)

    # 5
    elif eda_name == "Illiterates vs Literates trend over Years":

      data = illiteracy.groupby("Year", as_index=False)[["Illiteracy_rate", "Literacy_rate"]].mean()

      fig = px.line(data, x="Year", y=["Illiteracy_rate", "Literacy_rate"], markers=True)

      show_chart(fig)

    # 6
    elif eda_name == "GDP per Avg Schooling":

      fig = px.scatter(gdp_schooling, x="Avg_yrs_schooling", y="GDP", color="Region")

      show_chart(fig)

    # 7
    elif eda_name == "GDP Distribution Boxplot":

      fig = px.box(gdp_schooling, x="Year", y="GDP")

      show_chart(fig)

    # 8
    elif eda_name == "Correlation of Population and Literacy":
      data = gdp_schooling[(gdp_schooling["Year"] >= 2020) & (gdp_schooling["Year"] <= 2023)]
      df = data.groupby("Year", as_index=False).agg({"Population": "mean", "Literacy": "mean"})
      df["Population_Million"] = df["Population"] / 1_000_000

      fig = make_subplots(specs=[[{"secondary_y": True}]])

      # Population bar
      fig.add_trace(go.Bar(x=df["Year"],y=df["Population_Million"],name="Population (Million)"),secondary_y=False)

      # Literacy line (IMPORTANT FIX HERE)
      fig.add_trace(go.Scatter(x=df["Year"],y=df["Literacy"],mode="lines+markers",name="Literacy Rate (%)"),secondary_y=True)

      fig.update_layout(title="Population Growth vs Literacy Growth (2020–2023)", width=900, height=600, template="plotly_white")

      fig.update_xaxes(title_text="Year")

      fig.update_yaxes(title_text="Population (Millions)", secondary_y=False)

      fig.update_yaxes(title_text="Literacy Rate (%)", secondary_y=True, range=[0, 100])

      show_chart(fig)

    # 9
    elif eda_name == "Highest GDP countries literacy rate TOP 5 only":
      data = gdp_schooling.groupby( "Country", as_index=False )[["GDP", "Literacy"]].mean()

      #top 5
      data = data.sort_values( by="GDP", ascending=False ).head(5)

      fig = px.bar(data, x="Country", y=["GDP", "Literacy"], barmode="group")

      show_chart(fig)

    # 10
    elif eda_name == "Literacy Growth Rate over year - India.":

      data = literacy[literacy["Country"] == "India"][["Year", "Adult", "Avg_Youth_Literacy"]]

      fig = px.line(data, x="Year", y=["Adult", "Avg_Youth_Literacy"], markers=True)

      show_chart(fig)

# page 3
elif page == "Country Profile Page":

    st.title("🌍 Country Profile Page")
    st.markdown("Discover country-level trends and insights in literacy, education quality, schooling, and development indicators.")
    country = st.selectbox("Select Country", sorted(literacy["Country"].unique()))
    row1_col1, row1_col2 = st.columns(2)
    row3_col1, row3_col2 = st.columns(2)

    # filter data
    literacy_data = literacy[literacy["Country"] == country]

    illiteracy_data = illiteracy[illiteracy["Country"] == country]

    gdp_data = gdp_schooling[gdp_schooling["Country"] == country]

    # literacy trend
    with row1_col1:
      st.subheader("📘 Literacy Trends")
      fig1 = px.line( literacy_data, x="Year", y=["Adult", "Avg_Youth_Literacy"], markers=True, title=f"{country} Literacy Trends")

      st.plotly_chart( fig1, use_container_width=True )

    # illiteracy trend
    with row1_col2:
      st.subheader("📉 Illiteracy Trend")

      fig5 = px.line(illiteracy_data, x="Year", y="Illiteracy_rate", markers=True, title=f"{country} Illiteracy Trend")

      st.plotly_chart(fig5,use_container_width=True)

    # schooling trend
    st.subheader("🎓 Average Schooling Years")

    fig3 = px.line(gdp_data, x="Year", y="Avg_yrs_schooling", markers=True, title=f"{country} Schooling Trend")

    st.plotly_chart(fig3,use_container_width=True)

    # population trend
    with row3_col1:
      st.subheader("👨‍👩‍👧 Population Trend")

      fig4 = px.bar(gdp_data, x="Year", y="Population", title=f"{country} Population")

      st.plotly_chart(fig4, use_container_width=True)

    # gdp trend
    with row3_col2:
      st.subheader("💰 GDP Trend")
      fig2 = px.line(gdp_data, x="Year", y="GDP", markers=True, title=f"{country} GDP Over Years")

      st.plotly_chart(fig2, use_container_width=True)