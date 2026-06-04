queries = {
      "Literacy Rates and Trends":{
          "Top 5 Countries with Highest Adult Literacy in 2020":{
              "query":
              """SELECT Country AS top_5_countries, MAX(Adult) AS adult_literacy_rate FROM literacy_rates WHERE Year = 2020
              AND Adult IS NOT NULL GROUP BY Country ORDER BY adult_literacy_rate DESC LIMIT 5;""",

              "chart": "bar",
              "x": "top_5_countries",
              "y": "adult_literacy_rate"
              },

          "Countries where Female Youth Literacy were < 80pct":{
              "query":
              """SELECT Country, Female FROM literacy_rates WHERE Female < 80;""",

              "chart": "bar",
              "x": "Country",
              "y": "Female"
              },

          "Average Adult Literacy per Continent":{
              "query":
              """SELECT Region, AVG(Adult) AS Avg_Adult_Literacy FROM literacy_rates GROUP BY Region;""",
              "chart": "pie",
              "x": "Region",
              "y": "Avg_Adult_Literacy"
              }
          },

      "Illiteracy Population Analysis": {
          "Countries with illiteracy rate > 20pct in 2000":{
              "query":
              """SELECT Country, Year, Illiteracy_rate FROM illiteracy_population
              WHERE Year = 2000 AND Illiteracy_rate > 20 ORDER BY Illiteracy_rate ASC;""",

              "chart": "bar",
              "x": "Country",
              "y": "Illiteracy_rate"
              },

          "Trend of illiteracy rate for India (2000 to 2020)": {
              "query":
              """SELECT Year, Illiteracy_rate FROM illiteracy_population WHERE Country = 'India' AND Year BETWEEN 2000 AND 2020;""",
              "chart": "line",
              "x": "Year",
              "y": "Illiteracy_rate"
              },
          "Top 10 countries with largest illiterate population in the last year": {
              "query":
              """SELECT Country, MAX(Illiteracy_Population) AS Illiterate FROM illiteracy_population WHERE Year = 2023
              AND Illiteracy_Population IS NOT NULL GROUP BY Country ORDER BY Illiterate DESC LIMIT 10;""",

              "chart": "bar",
              "x": "Country",
              "y": "Illiterate"
              }
          },

      "GDP and Schooling Analysis": {
          "Countries with avg_years_schooling > 7 and gdp_per_capita < 5000":{
              "query":
              """SELECT Country, Avg_yrs_schooling, GDP FROM gdp_schooling
              WHERE Avg_yrs_schooling > 7 AND GDP < 5000 AND Avg_yrs_schooling is NOT NULL AND GDP is NOT NULL;""",

              "chart": "scatter",
              "x": "Avg_yrs_schooling",
              "y": "GDP"
              },

          "Ranking countries by GDP per schooling for the year 2020":{
              "query": """SELECT Country, GDP_per_Schooling FROM gdp_schooling
              WHERE Year = 2020 AND GDP_per_Schooling IS NOT NULL ORDER BY GDP_per_Schooling DESC;""",

              "chart": "scatter",
              "x": "Country",
              "y": "GDP_per_Schooling"
              },

          "Find global average schooling years per year":{
              "query": """SELECT Year, AVG(Avg_yrs_schooling) AS Avg_Schooling FROM gdp_schooling
              WHERE Avg_yrs_schooling IS NOT NULL GROUP BY Year ORDER BY Year ASC;""",

              "chart": "line",
              "x": "Year",
              "y": "Avg_Schooling"
              }
      },

      "Additional Queries": {
          "Top 10 countries in 2020 with highest GDP per capita but lowest average years of schooling(less than 6)" : {
              "query": """SELECT Country, GDP_per_Schooling, Avg_yrs_schooling FROM gdp_schooling WHERE Year = 2020
              AND Avg_yrs_schooling < 6 AND GDP_per_Schooling IS NOT NULL ORDER BY GDP_per_Schooling DESC LIMIT 11;""",

              "chart": "bar",
              "x": "Country",
              "y": "GDP_per_Schooling"
              },

          "Countries where the illiterate population is high despite having more than 10 average years of schooling" :{
              "query": """SELECT i.Country, i.Illiteracy_Population, g.Avg_yrs_schooling, i.Year FROM illiteracy_population i
              JOIN gdp_schooling g ON i.Country = g.Country WHERE g.Avg_yrs_schooling > 10 AND i.Illiteracy_Population IS NOT NULL
              ORDER BY i.Illiteracy_Population DESC;""",

              "chart": "scatter",
              "x": "Avg_yrs_schooling",
              "y": "Illiteracy_Population"
              },

          "Compare literacy rates and GDP per capita growth for India" :{
              "query": """SELECT l.Country, l.Year, l.Avg_Youth_Literacy, g.Growth_Rate FROM literacy_rates l JOIN gdp_schooling g ON l.Country = g.Country
              AND l.Year = g.Year WHERE l.Country = 'India' AND l.year BETWEEN 2000 AND 2023 AND l.Avg_Youth_Literacy IS NOT NULL
              AND g.GDP_per_Schooling IS NOT NULL ORDER BY l.Year ASC;""",

              "chart": "line",
              "x": "Year",
              "y": "Growth_Rate"
              },
          "Countries with high GDP and Difference in Literacy(Male, Female)" : {
              "query": """SELECT l.Country, l.Year, l.Male, l.Female, g.GDP FROM literacy_rates l JOIN gdp_schooling g ON l.Country = g.Country
              AND l.Year = g.Year WHERE g.Year = 2020 AND g.GDP > 30000 AND l.Male IS NOT NULL AND l.Female IS NOT NULL
              AND g.GDP IS NOT NULL ORDER BY g.GDP DESC;""",
              "chart": "grouped_bar",
              "x": "Country",
              "y1": "Male",
              "y2": "Female"
              }
          }
      }