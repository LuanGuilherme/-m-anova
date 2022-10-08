import pandas as pd
import scipy.stats as stats
from bioinfokit.analys import stat

#importa o dataset
data = pd.read_csv("dataset.csv")

#adequa o dataset para uso da biblioteca bioinfokit
data_mod = pd.melt(data.reset_index(), id_vars=['index'], value_vars=['Horário', 'VelocidadeMaxima', 'Idade', 'Ano'])

#muda os nomes das colunas no dataframe adequado anteriormente
data_mod.columns = ['index', 'variaveis', 'valores']

#calcula f-value e p-value
fvalue, pvalue = stats.f_oneway(data['Horário'], data['VelocidadeMaxima'], data['Idade'], data['Ano'])

print("F =", fvalue, "    P =", pvalue)

#faz anova
res = stat()
res.anova_stat(df=data_mod, res_var='valores', anova_model='valores ~ C(variaveis)')
print(res.anova_summary)

#algumas bibliotecas para gerar os gráficos das exigencias da anova
import statsmodels.api as sm
import matplotlib.pyplot as plt

# histograma
plt.hist(res.anova_model_out.resid, bins='auto', histtype='bar', ec='k') 
plt.xlabel("Resíduos")
plt.ylabel('Frequência')
plt.savefig("hist.png")

# gráfico q-q
sm.qqplot(res.anova_std_residuals, line='45')
plt.xlabel("Quantis")
plt.ylabel("Resíduos padronizados")
plt.savefig("qq.png")

#fonte: https://www.reneshbedre.com/blog/anova.html
