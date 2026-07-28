#importando arquivos panda
import pandas as pd

#lendo o arquivo csv
df = pd.read_csv('data/campeonato-brasileiro-full.csv') #pd é a biblioteca pandas, read_csv é o método para ler arquivos csv, e 'data/campeonato-brasileiro-full.csv' é o caminho do arquivo que queremos ler.
#df é o nome do DataFrame que criamos ao ler o arquivo CSV.
#pd é a biblioteca pandas que importamos no início do código.

# Imprimir as colunas
print("Colunas do DataFrame:")
print(df.columns) #df.columns é um atributo do DataFrame que retorna uma lista com os nomes das colunas do DataFrame.

# Imprimir as 5 primeiras linhas
print("\nPrimeiras 5 linhas:")
print(df.head()) #df.head() é um método do DataFrame que retorna as primeiras 5 linhas do DataFrame. Podemos passar um número como argumento para retornar mais ou menos linhas, por exemplo, df.head(10) retornaria as primeiras 10 linhas.

# Imprimir informações gerais
print("\nInformações gerais:")
print(df.info()) #df.info() é um método do DataFrame que retorna informações gerais sobre o DataFrame, como o número de linhas, o número de colunas, o tipo de dados de cada coluna, e a quantidade de valores não nulos em cada coluna.


#Convertendo a coluna data de texto para data de verdade
df["data"] = pd.to_datetime(df["data"]) #pd.to_datetime() é uma função do pandas que converte uma coluna de texto para o tipo datetime. Reatribuímos o resultado de volta para df["data"].

#Criando uma nova coluna ano, extraindo o ano da data
df["ano"] = df["data"].dt.year #df["data"].dt.year é um atributo do pandas que retorna o ano de uma coluna datetime. Criamos uma nova coluna "ano" e atribuímos o resultado de df["data"].dt.year a ela.

#Criando uma coluna resultado que diga se foi "Vitória mandante", "Vitória visitante" ou "Empate"
def resultado(row): #definimos uma função chamada resultado que recebe uma linha do DataFrame

    if row["mandante_Placar"] > row["visitante_Placar"]: #se o placar do mandante for maior que o placar do visitante
        return "Vitória mandante" #retorna "Vitória mandante"
    elif row["mandante_Placar"] < row["visitante_Placar"]: #se o placar do mandante for menor que o placar do visitante
        return "Vitória visitante" #retorna "Vitória visitante"
    else: #se não for nenhuma das duas condições acima, ou seja, se for empate
        return "Empate" #retorna "Empate"
#Criando coluna resultado
df["resultado"] = df.apply(resultado, axis=1) #aplicamos a função resultado a cada linha do DataFrame e atribuímos o resultado à nova coluna "resultado"

#Exibindo as colunas data, ano, mandante_Placar, visitante_Placar e resultado
print(df[
    [
        "data", 
        "ano",
        "mandante_Placar", 
        "visitante_Placar", 
        "resultado"
    ]
].head(10)
)