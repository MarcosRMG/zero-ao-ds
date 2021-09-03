import pandas as pd

data = pd.read_csv('data/kc_house_data.csv')
#print(data.head())

def pergunta_resposta(pergunta: str, resposta):
    '''
    --> Recebe a pergunta e a respectiva resposta

    :param pergunta: A questão a ser respondida
    :param resposta: A respectiva resposta
    :return: Imprime a pergunta seguida da resposta
    '''
    print(f'{pergunta} {resposta}')

# 1. Quantas casas estão disponíveis para compra?
#print(f'Quantas casas estão disponíveis para compra?: {data.shape[0]}')

#2. Quantos atributos as casa possuem? ( numero de quartos, garagens, m2, vista pro mar )
#print(f'Quantos atributos as casa possuem? {data.shape[1]}')

#3. Quais são os atributos?
#print(f'Quais são os atributos? {data.columns}')

#4. Qual a casa mais cara do portfólio ( casa com maior valor )?
#print(f'Qual a casa mais cara do portfólio? {data[["id", "price"]].sort_values("price", ascending=False).loc[0]}')

#5. Qual a casa com o maior número de quartos?
#print(f'Qual a casa com o maior número de quartos? {data[["id", "bedrooms"]].sort_values("bedrooms", ascending=False).loc[0]}')

#6. Qual a soma total de quartos do conjunto de dados?
#pergunta_resposta('Qual a soma total de quartos do conjunto de dados?', data['bedrooms'].sum())

#7. Quantas casas possuem 2 banheiros?
#pergunta_resposta('Quantas casas possuem 2 banheiros?', data.query('bathrooms == 2').shape[0])

#8. Qual o preço médio de todas as casas do conjunto de dados?
#pergunta_resposta('Qual o preço médio de todas as casas do conjunto de dados?', data['price'].mean())

#9. Qual o preço médio das casas com 2 banheiros?
#pergunta_resposta('Qual o preço médio das casas com 2 banheiros?', data.query('bathrooms == 2')['price'].mean())

#10. Qual o preço mínimo entre as casas com 3 quartos?
#pergunta_resposta('Qual o preço mínimo entre as casas com 3 quartos?', data.query('bedrooms == 3')['price'].min())

#11. Quantas casas possuem mais de 300 metros quadrados na sala de estar?
#pergunta_resposta('Quantas casas possuem mais de 300 metros quadrados na sala de estar?', data.query('sqft_living > 300').shape[0])

#12. Quantas casas tem mais de 2 andares?
#pergunta_resposta('Quantas casas tem mais de 2 andares?', data.query('floors > 2').shape[0])

#13. Quantas casas tem vista para o mar?
#pergunta_resposta('Quantas casas tem vista para o mar?', data.query('view != 0').shape[0])

#14. Das casas com vista para o mar, quantas tem 3 quartos?
#pergunta_resposta('Das casas com vista para o mar, quantas tem 3 quartos?', data.query('view == 1 and bedrooms == 3').shape[0])

#15. Das casas com mais de 300 metros quadrados de sala de estar tem quantos tem mais de 4 banheiros?
#pergunta_resposta('Das casas com mais de 300 metros quadrados de sala de estar quantas tem mais de 4 banheiros?', data.query('sqft_living > 300 and bathrooms > 4').shape[0])
