"""#**Exploratory Data Analysis (EDA)**"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

"""***Literacy EDA***

**1. Adult & Youth Literacy Rate Over Years**
"""

df_literacy

adult_literacy = df_literacy.groupby("Year")["Adult"].mean()
youth_literacy = df_literacy.groupby("Year")[["Male", "Female"]].mean()

plt.figure(figsize=(15,8))
plt.plot(youth_literacy.index, youth_literacy.values)
plt.plot(adult_literacy.index, adult_literacy.values)
plt.title("Avg Literacy Rate Over Years of Adult & Youth")
plt.xlabel("Year")
plt.ylabel("Total_Youth & Adult")
plt.legend(["Female", "Male", "Adult"])
plt.grid(alpha=0.5)

plt.show()

"""**2. Region wise Male and Female Literacy Rate**"""

r_male_literacy = df_literacy.groupby("Region")["Male"].mean()
r_female_literacy = df_literacy.groupby("Region")["Female"].mean()

plt.figure(figsize=(15,8))
plt.plot(r_male_literacy.index, r_male_literacy.values, marker="o")
plt.plot(r_female_literacy.index, r_female_literacy.values, marker="o")
plt.title("Region Wise Trend")
plt.xlabel("Region")
plt.ylabel("Male vs Female")
plt.grid(alpha=0.5)
plt.legend(["Male", "Female"])

plt.show()

"""**3. Adult Literacy during covid (2020 to 2023)**"""

covid_year = df_literacy[(df_literacy["Year"] >= 2020) & (df_literacy["Year"] <= 2023)]
adult_literacy = covid_year.groupby("Year", as_index=False)["Adult"].mean().round()

plt.figure(figsize=(15,8))

sns.barplot(data=adult_literacy, x="Year", y="Adult", palette="dark", width=0.25, hue="Adult")

plt.title("Adult Literacy During COVID (2020 to 2023)")
plt.xlabel("Year")
plt.ylabel("Adult Literacy")
plt.legend(loc="upper center")

plt.grid(False)

plt.show()

fig = px.line(adult_literacy, x="Year", y="Adult", markers=True, title="Adult Literacy During COVID")

fig.show()

"""**4. Indain Adult Leteracy Rate Over Years**"""

india_literacy = df_literacy[df_literacy["Country"] == "India"]

plt.figure(figsize=(20,10))
plt.pie(india_literacy["Adult"], labels=india_literacy["Year"], autopct='%1.1f%%')
plt.title("Youth Leteracy Rate Over Years - Inida")
plt.legend(loc="upper right")

plt.show()

"""***Illiteracy EDA***

**5. Illiterates vs Literates trend over Years**
"""

illiteracy = df_illiteracy.groupby("Year")["Illiteracy_rate"].mean()
literacy = df_illiteracy.groupby("Year")["Literacy_rate"].mean()

plt.figure(figsize=(15,8))
plt.bar(illiteracy.index,illiteracy.values)
plt.bar(literacy.index, literacy.values, alpha=0.7)
plt.title("Illiterates and Literates trand over Years")
plt.xlabel("Year")
plt.ylabel("Trend")
plt.legend(["Illiterates", "Literates"])
plt.yticks(range(0, 101, 10))
plt.grid(alpha=0.5)

plt.show()

"""**6. Illiteracy Rate comparision betweeen selected countries over years**"""

countries = ["Bangladesh", "China", "India", "Nepal", "Pakistan"]

com_countries = df_illiteracy[df_illiteracy["Country"].isin(countries)]

plt.figure(figsize=(15,8))
sns.barplot(data=com_countries, x="Year", y="Illiteracy_rate", palette= "magma", width=1, hue="Country")

plt.title("Illiteracy Rate of Five Countries(random)")
plt.xlabel("Year")
plt.ylabel("Illiteracy Rate")
plt.legend(loc="upper right")

plt.grid(False)

plt.show()

"""***GDP and Schooling EDA***

**7. GPD per Avg Schooling**
"""

plt.figure(figsize=(15,6))

sns.scatterplot(data = df_gdp_schooling, x="Avg_yrs_schooling", y="GDP")

plt.title("GDP vs Schooling")
plt.xlabel("Schooling")
plt.ylabel("GDP")
plt.grid(True, alpha=0.5)


plt.show()

"""**8. Highest GDP countries literacy rate TOP 5 only**"""

top_gdp = df_gdp_schooling.groupby("Country")[["GDP", "Literacy"]] \
                          .mean() \
                          .sort_values(by="GDP", ascending=False) \
                          .head(5) #\ line continue

plt.figure(figsize=(15,8))

sns.barplot(x = top_gdp.index, y = top_gdp["Literacy"], palette = "viridis", hue = top_gdp["GDP"],
            width = 0.25)

plt.title("Literacy Rate of Highest GDP Countries")
plt.xlabel("Country")
plt.ylabel("Literacy Rate")
plt.grid(False)

plt.show()

"""**9. Literacy Growth Rate over year - India.**"""

ind = df_gdp_schooling[df_gdp_schooling["Country"] == "India"].copy()
growth = ind.groupby("Year")["Growth_Rate"].mean().reset_index()

fig = px.line(growth, x="Year", y="Growth_Rate", title="Literacy Growth Rate over year - India", markers=True, line_shape='spline')

fig.update_layout(width=1000, height=600, title_x=0.5)
fig.update_traces(line=dict(color='orange', width=4))

fig.show()

"""**10. Population Growth vs Literacy Growth - Covid**"""

covid = df_gdp_schooling[(df_gdp_schooling["Year"] >= 2020) & (df_gdp_schooling["Year"] <= 2023)]

population_literacy = covid.groupby("Year", as_index=False).agg ({"Population": "max", "Literacy": "mean"})

population_literacy["Year"] = population_literacy["Year"].astype(int)

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(x=population_literacy["Year"],y=population_literacy["Population"] / 1_000_000,name="Population (Million)"),secondary_y=False)

fig.add_trace(go.Scatter(x=population_literacy["Year"], y=population_literacy["Literacy"], mode="lines+markers", name="Literacy Rate (%)"), secondary_y=True)

fig.update_layout(title="Population Growth vs Literacy Growth - Covid",width=900, height=600, template="plotly_white")

fig.update_xaxes(title_text="Year")
fig.update_yaxes (title_text="Population (Millions)", secondary_y=False)
fig.update_yaxes(title_text="Literacy Rate (%)", secondary_y=True)

fig.show()

"""**11. GDP Distribution Boxplot**"""

plt.figure(figsize=(15,8))

sns.boxplot(
    data=df_gdp_schooling,
    x="Year",
    y="GDP",
    palette="viridis",
    hue = "Year"
)

plt.title("GDP Distribution Over Years")
plt.xlabel("Year")
plt.ylabel("GDP")

plt.xticks(rotation=45)

plt.grid(alpha=0.5)

plt.show()

"""**12. Correlation of Population and Literacy**"""

df_gdp_schooling = df_gdp_schooling.sort_values(["Year", "Population"])

population_literacy = df_gdp_schooling.groupby("Year", as_index=False).agg ({"Population": "max", "Literacy": "mean"})

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(x=population_literacy["Year"],y=population_literacy["Population"] / 1_000_000,name="Population (Million)"),secondary_y=False)
fig.add_trace(go.Scatter(x=population_literacy["Year"], y=population_literacy["Literacy"], mode="lines+markers", name="Literacy Rate (%)"), secondary_y=True)
fig.update_layout(title="Population vs Literacy Rate Over Years",width=1100, height=600, title_x=0.5, template="plotly_white")

fig.update_xaxes(title_text="Year")
fig.update_yaxes (title_text="Population (Millions)", secondary_y=False)
fig.update_yaxes(title_text="Literacy Rate (%)", secondary_y=True)

fig.show()
