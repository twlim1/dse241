import pandas as pd

# Read json file into pandas data frame
n = 15
df = pd.read_csv(r'..\data\olympics.csv')

# Filter the list by top N countries by medal won
df_men = df[df.Gender == 'M']
df_top_n = df_men.groupby('Country').count().sort_values(['Medal'], ascending=False).head(n)
country_list = df_top_n.index.values
df_men = df_men[df_men.Country.isin(country_list)]

# Create new csv format for easier processing in vis
df_men = df_men[['Year', 'Country']]
df_men = df_men.groupby(df_men.columns.tolist(), as_index=False).size()
# print(df_new)

# Filter the list by top N countries by medal won
df_women = df[df.Gender == 'W']
df_top_n = df_women.groupby('Country').count().sort_values(['Medal'], ascending=False).head(n)
country_list = df_top_n.index.values
df_women = df_women[df_women.Country.isin(country_list)]

# Create new csv format for easier processing in vis
df_women = df_women[['Year', 'Country']]
df_women = df_women.groupby(df_women.columns.tolist(), as_index=False).size()
# print(df_new)

df_men.to_csv(r'..\data\olympics_men_top_{}.csv'.format(n), index=False)
df_women.to_csv(r'..\data\olympics_women_top_{}.csv'.format(n), index=False)
