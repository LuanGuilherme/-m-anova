import pandas as pd
from dfply import *
from statsmodels.multivariate.manova import MANOVA

#importa o dataset
data = pd.read_csv("dataset.csv")

# sumário das estatísticas para a variável dependente VelocidadeMaxima
print(data >> group_by(X.Horário) >> summarize(n=X['VelocidadeMaxima'].count(), mean=X['VelocidadeMaxima'].mean(), std=X['VelocidadeMaxima'].std()))
print()

#sumário das estatísticas para a variável dependente Idade
print(data >> group_by(X.Horário) >> summarize(n=X['Idade'].count(), mean=X['Idade'].mean(), std=X['Idade'].std()))
print()

#faz MANOVA
fit = MANOVA.from_formula('VelocidadeMaxima + Idade ~ Horário', data=data)
print(fit.mv_test())