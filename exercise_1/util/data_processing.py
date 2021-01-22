import pandas as pd

# Read json file into pandas data frame
n = 15
df = pd.read_csv(r'..\data\olympics.csv')

# Filter the list by top N countries by Men medal won
df_men = df[df.Gender == 'M']
df_top_n = df_men.groupby('Country').count().sort_values(['Medal'], ascending=False).head(n)
country_list = df_top_n.index.values
df_men = df_men[df_men.Country.isin(country_list)]

# Create men's Year-over-year dataframe
df_men_yoy = df_men[['Year', 'Country']]
df_men_yoy = df_men_yoy.groupby(df_men_yoy.columns.tolist(), as_index=False).size()
df_men_yoy.rename(columns={'size': 'Total'}, inplace=True)

# Create men by medal dataframe
df_men_gold = df_men[df_men.Medal == 'Gold'][['Country']]
df_men_gold = df_men_gold.groupby(df_men_gold.columns.tolist(), as_index=False).size()
df_men_gold.rename(columns={'size': 'Gold'}, inplace=True)
df_men_silver = df_men[df_men.Medal == 'Silver'][['Country']]
df_men_silver = df_men_silver.groupby(df_men_silver.columns.tolist(), as_index=False).size()
df_men_silver.rename(columns={'size': 'Silver'}, inplace=True)
df_men_bronze = df_men[df_men.Medal == 'Bronze'][['Country']]
df_men_bronze = df_men_bronze.groupby(df_men_bronze.columns.tolist(), as_index=False).size()
df_men_bronze.rename(columns={'size': 'Bronze'}, inplace=True)
df_men_medal = pd.concat([df_men_gold, df_men_silver['Silver'], df_men_bronze['Bronze']], axis=1)

# Filter the list by top N countries by women medal won
df_women = df[df.Gender == 'W']
df_top_n = df_women.groupby('Country').count().sort_values(['Medal'], ascending=False).head(n)
country_list = df_top_n.index.values
df_women = df_women[df_women.Country.isin(country_list)]

# Create women's Year-over-year dataframe
df_women_yoy = df_women[['Year', 'Country']]
df_women_yoy = df_women_yoy.groupby(df_women_yoy.columns.tolist(), as_index=False).size()
df_women_yoy.rename(columns={'size': 'Total'}, inplace=True)

# Create women by medal dataframe
df_women_gold = df_women[df_women.Medal == 'Gold'][['Country']]
df_women_gold = df_women_gold.groupby(df_women_gold.columns.tolist(), as_index=False).size()
df_women_gold.rename(columns={'size': 'Gold'}, inplace=True)
df_women_silver = df_women[df_women.Medal == 'Silver'][['Country']]
df_women_silver = df_women_silver.groupby(df_women_silver.columns.tolist(), as_index=False).size()
df_women_silver.rename(columns={'size': 'Silver'}, inplace=True)
df_women_bronze = df_women[df_women.Medal == 'Bronze'][['Country']]
df_women_bronze = df_women_bronze.groupby(df_women_bronze.columns.tolist(), as_index=False).size()
df_women_bronze.rename(columns={'size': 'Bronze'}, inplace=True)
df_women_medal = pd.concat([df_women_gold, df_women_silver['Silver'], df_women_bronze['Bronze']], axis=1)

# Filter the list by top N countries by pairs medal won
df_pairs = df[df.Gender == 'X']
df_top_n = df_pairs.groupby('Country').count().sort_values(['Medal'], ascending=False).head(n)
country_list = df_top_n.index.values
df_pairs = df_pairs[df_pairs.Country.isin(country_list)]

# Create pairs' Year-over-year dataframe
df_pairs_yoy = df_pairs[['Year', 'Country']]
df_pairs_yoy = df_pairs_yoy.groupby(df_pairs_yoy.columns.tolist(), as_index=False).size()
df_pairs_yoy.rename(columns={'size': 'Total'}, inplace=True)

# Create pairs by medal dataframe
df_pairs_gold = df_pairs[df_pairs.Medal == 'Gold'][['Country']]
df_pairs_gold = df_pairs_gold.groupby(df_pairs_gold.columns.tolist(), as_index=False).size()
df_pairs_gold.rename(columns={'size': 'Gold'}, inplace=True)
print(df_pairs_gold)
df_pairs_silver = df_pairs[df_pairs.Medal == 'Silver'][['Country']]
df_pairs_silver = df_pairs_silver.groupby(df_pairs_silver.columns.tolist(), as_index=False).size()
df_pairs_silver.rename(columns={'size': 'Silver'}, inplace=True)
print(df_pairs_silver)
df_pairs_bronze = df_pairs[df_pairs.Medal == 'Bronze'][['Country']]
df_pairs_bronze = df_pairs_bronze.groupby(df_pairs_bronze.columns.tolist(), as_index=False).size()
df_pairs_bronze.rename(columns={'size': 'Bronze'}, inplace=True)
print(df_pairs_bronze)
df_pairs_medal = pd.concat([df_pairs_gold, df_pairs_silver['Silver'], df_pairs_bronze['Bronze']], axis=1)
print(df_pairs_medal)

df_men_yoy.to_csv(r'..\data\olympics_top_{}_men_yoy.csv'.format(n), index=False)
df_men_medal.to_csv(r'..\data\olympics_top_{}_men_medal.csv'.format(n), index=False)
df_women_yoy.to_csv(r'..\data\olympics_top_{}_women_yoy.csv'.format(n), index=False)
df_women_medal.to_csv(r'..\data\olympics_top_{}_women_medal.csv'.format(n), index=False)
df_pairs_yoy.to_csv(r'..\data\olympics_top_{}_pairs_yoy.csv'.format(n), index=False)
# df_pairs_medal.to_csv(r'..\data\olympics_top_{}_pairs_medal.csv'.format(n), index=False)
