
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
