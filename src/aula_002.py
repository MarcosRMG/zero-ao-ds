import pandas as pd
from aula_001 import pergunta_resposta
import plotly.express as px

data = pd.read_csv('data/kc_house_data.csv')
data['date'] = pd.to_datetime(data['date'])
data['yr_built'] = pd.to_datetime(data['yr_built'])
#print(data.dtypes)

#1. Crie uma nova coluna chamada: “house_age” - Se o valor da coluna “date” for maior que 2014-01-01 =>
# ‘new_house’ - Se o valor da coluna “date” for menor que 2014-01-01 => ‘old_house’
data['house_age'] = 'new_house'
data.loc[data['date'] < '2014-01-01', 'house_age'] = 'old_house'
#print(data[['date', 'house_age']])

#2. Crie uma nova coluna chamada: “dormitory_type” - Se o valor da coluna “bedrooms” for igual à 1 =>
# ‘studio’ - Se o valor da coluna “bedrooms” for igual a 2 => ‘apartament’ - Se o valor da coluna
# “bedrooms” for maior que 2 => ‘house’
data['dormitory_type'] = 'house'
data.loc[data['bedrooms'] == 1, 'dormitory_type'] = 'studio'
data.loc[data['bedrooms'] == 2, 'dormitory_type'] = 'apartment'
#print(data[['bedrooms', 'dormitory_type']])

#3. Crie uma nova coluna chamada: “condition_type” - Se o valor da coluna “condition” for menor ou igual
# à 2 => ‘bad’ - Se o valor da coluna “condition” for igual à 3 ou 4 => ‘regular’ - Se o valor da coluna
# “condition” for igual à 5 => ‘good’
data['condition_type'] = 'bad'
data.loc[data['condition'] == 3, 'condition_type'] = 'regular'
data.loc[data['condition'] == 4, 'condition_type'] = 'regular'
data.loc[data['condition'] == 5, 'condition_type'] = 'good'
#print(data[['condition', 'condition_type']])

# 4. Modifique o TIPO a Coluna “condition” para STRING
data['condition'] = data['condition'].astype(str)
#print(data['condition'].dtypes)

#5. Delete as colunas: “sqft_living15” e “sqft_lot15”
data.drop(['sqft_living15', 'sqft_lot15'], axis=1, inplace=True)
#print(data.columns)

#6. Modifique o TIPO a Coluna “yr_build” para DATE
data['yr_built'] = pd.to_datetime(data['yr_built'])
#print(data['yr_built'].dtypes)

# 7. Modifique o TIPO a Coluna “yr_renovated” para DATE
data['yr_renovated'] = pd.to_datetime(data['yr_renovated'])
#print(data['yr_renovated'].dtypes)

#8. Qual a data mais antiga de construção de um imóvel?
#print(f'A data mais antiga é: {data["yr_built"].min()}')

# 9. Qual a data mais antiga de renovação de um imóvel?
#print(f'A data mais antiga de renovação do imóvel é: {data["yr_renovated"].min()}')

#10. Quantos imóveis tem 2 andares?
#pergunta_resposta('Quantos imóveis tem 2 andares?', data[data['floors'] == 2].shape[0])

#11. Quantos imóveis estão com a condição igual a “regular” ?
#pergunta_resposta('Quantos imóveis estão com a condição igual a regular?',
#                   data[data['condition_type'] == 'regular'].shape[0])

#12. Quantos imóveis estão com a condição igual a “bad”e possuem “vista para água” ?
#pergunta_resposta('Quantos imóveis estão com a condição igual a bad e possuem vista para água?',
#                  data.query('condition_type == "bad" and waterfront == 1').shape[0])

#13. Quantos imóveis estão com a condição igual a “good” e são “new_house”?
#pergunta_resposta('Quantos imóveis estão com a condição igual a “good” e são new_house?',
#                  data.query('condition_type == "good" and house_age == "new_house"').shape[0])

#14. Qual o valor do imóvel mais caro do tipo “studio” ?
#pergunta_resposta('Qual o valor do imóvel mais caro do tipo studio?',
#                  data[data['dormitory_type'] == 'studio']['price'].max())

#15. Quantos imóveis do tipo “apartment” foram reformados em 2015?
#pergunta_resposta('Quantos imóveis do tipo apartment foram reformados em 2015?',
#                  data.query('dormitory_type == "apartment" and yr_renovated == 2015').shape[0])

#16. Qual o maior número de quartos que um imóveis do tipo “house” possui?
#pergunta_resposta('Qual o maior número de quartos que um imóveis do tipo house possui?',
#                  data.query('dormitory_type == "house"')['bedrooms'].max())

#17. Quantos imóveis “new_house” foram reformados no ano de 2014?
#pergunta_resposta('Quantos imóveis new_house foram reformados no ano de 2014?',
#                  data.query('house_age == "new_house" and yr_renovated == "2014"').shape[0])

#18. Selecione as colunas: “id”, “date”, “price”, “floors”,“zipcode” pelo método:
# 10.1. Direto pelo nome das colunas.
#print(data[['id', 'date', 'price', 'floors', 'zipcode']])
# 10.2. Pelos Índices.
#print(data.iloc[:, [0, 1, 2, 7, 16]])
# 10.3. Pelos Índices das linhas e o nome das colunas
#print(data.loc[:, ['id', 'date', 'price', 'floors', 'zipcode']])
# 10.4. Índices Booleanos
#print(data.loc[:, [True, True, True, False, False, False, False, True, False, False, False, False, False,
#            False, False, False, True, False, False, False, False, False]])

#19. Salve um arquivo .csv com somente as colunas do item 10 ao 17.
#data.iloc[:, 10:17].to_csv('data/report.csv', index=False)

#20. Modifique a cor dos pontos no mapa de “pink” para “verde-escuro”
fig = px.scatter_mapbox(data, 'lat', 'long', hover_name='id', hover_data=['price'], color='price',
                  color_discrete_sequence=['darkgreen'], zoom=7, height=600, size='price')
fig.update_layout(mapbox_style='open-street-map', margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
#fig.show()
#fig.write_html('data/map.html')