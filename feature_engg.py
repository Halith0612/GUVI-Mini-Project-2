"""# **Feature Engineering**

**1. Illiteracy %** :
**Shows the percentage of the population that is illiterate**
"""

df_illiteracy

df_illiteracy["Illiteracy_Population"] = (df_illiteracy["Illiteracy_rate"] / 100 ) * df_illiteracy["Population"].astype(int)
df_illiteracy

print(df_illiteracy.isnull().sum())

"""**2. Literacy Gender Gap** :
**Highlights the disparity between male and female literacy rates.**
"""

df_literacy

# calculating literacy gap between gender and create column
df_literacy["Literacy_gap"] = df_literacy["Male"] - df_literacy["Female"]
df_literacy

"""**3. Youth Literacy Average : Provides a single indicator for overall youth literacy.**"""

df_literacy

# calculate the overall youth lliteracy avg and create column
df_literacy["Avg_Youth_Literacy"] = df_literacy[["Male", "Female"]].mean(axis = 1) # Calculates the average across columns (row-wise) ignores missing values by default.
df_literacy

print(df_literacy.isnull().sum())

"""**4. GDP per Schooling Year : Helps analyze economic output per year of education.**"""

df_gdp_schooling

# calculate gdp per schooling and create column
df_gdp_schooling["GDP_per_Schooling"] = df_gdp_schooling["GDP"] / df_gdp_schooling["Avg_yrs_schooling"]
df_gdp_schooling

"""**5. Education Index : Measures education quality by considering both access (literacy) and duration (schooling).**"""

df_gdp_schooling

# | EI Value    | Category  |
# | ----------- | --------- |
# | 0.900+      | Very High |
# | 0.700-0.899 | High      |
# | 0.500-0.699 | Medium    |
# | <0.500      | Low       |

df_gdp_schooling['Education_Index'] = (df_gdp_schooling['Literacy'] / 100) * (df_gdp_schooling['Avg_yrs_schooling'] / 15) / 2

df_gdp_schooling

"""**6. Literacy Growth Rate : Measures year-over-year improvement in literacy.**"""

df_gdp_schooling["Growth_Rate"] = (df_gdp_schooling["Literacy"].pct_change() * 100).fillna(0)

df_gdp_schooling

print(df_gdp_schooling.isnull().sum())

"""**Saving this DaraFrames as .csv file**

"""

df_literacy

df_illiteracy

df_gdp_schooling

df_literacy.to_csv("df_literacy.csv", index=False)
df_illiteracy.to_csv("df_illiteracy.csv", index=False)
df_gdp_schooling.to_csv("df_gdp_schooling.csv", index=False)
