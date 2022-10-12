import scipy.stats as stats
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import random
import statsmodels.api as sm
import matplotlib.pyplot as plt
import researchpy as rp
import warnings # Só pra tirar os warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('dataset.csv')
inner = []
major= []
outer =[]
remote = []
veryRemote = []
male = []
female = []
for index, row in df.iterrows():
    if (len(major) < 100 and row['Região'] == 'Major Cities of Australia'):
        major.append(row['HorarioH'])
    if (len(inner) < 100 and row['Região'] == 'Inner Regional Australia'): 
        inner.append(row['HorarioH'])
    if (len(outer) < 100 and row['Região'] == 'Outer Regional Australia'): 
        outer.append(row['HorarioH'])
    if (len(veryRemote) < 100 and row['Região'] == 'Very Remote Australia'): 
        veryRemote.append(row['HorarioH'])
    if (len(veryRemote) < 100 and row['Região'] == 'Remote Australia'): 
        remote.append(row['HorarioH'])
    if (len(male) < 100 and row['Gênero'] == 'Male'):
        male.append(row['HorarioH'])
    if (len(female) < 100 and row['Gênero'] == 'Female'):
        female.append(row['HorarioH'])
    
newData = pd.DataFrame(list(zip(major, inner ,outer, remote, veryRemote, male, female)), columns=['Região metropolitana', 'Interior', 'Outros','Remota','Muito remota', 'Homens', 'Mulheres'])

df_melt = pd.melt(newData.reset_index(), id_vars=['index'], value_vars=['Região metropolitana', 'Interior','Outros','Remota','Muito remota', 'Homens', 'Mulheres'])
df_melt.columns = ['index', 'RegiãoSexo', 'HorarioH']
print(df_melt)
print()

print(rp.summary_cont(df_melt['HorarioH']))
print()
print(rp.summary_cont(df_melt['HorarioH'].groupby(df_melt['RegiãoSexo'])))
print()
#print(rp.summary_cont(df_melt['HorarioH'].groupby(df_melt['Gênero'])))

import matplotlib.pyplot as plt
import seaborn as sns
'''plt.figure(figsize=(12,5))
ax = sns.boxplot(x='RegiãoSexo', y='HorarioH', data=df_melt, color='#99c2a2')
plt.xlabel('Regiões e sexo')
plt.ylabel('Horário (h)')
plt.savefig("boxplot.png")'''

# Ordinary Least Squares (OLS) model
# output (ANOVA F and p value)
model = ols('HorarioH ~ C(RegiãoSexo)', data=df_melt).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

from bioinfokit.analys import stat
res = stat()
res.tukey_hsd(df=df_melt, res_var='HorarioH', xfac_var='RegiãoSexo', anova_model='HorarioH ~ C(RegiãoSexo)')
print(res.anova_summary)
print()

#print(res.anova_model_out.resid)
# histogram
plt.hist(res.anova_model_out.resid, bins='auto', histtype='bar', ec='k') 
plt.xlabel("Resíduos")
plt.ylabel('Frequência')
#plt.xticks([])
plt.savefig("histograma-residuos-2.png")

# res.anova_std_residuals are standardized residuals obtained from ANOVA (check above)
sm.qqplot(res.anova_std_residuals, line='45')
plt.xlabel("Quantis")
plt.ylabel("Resíduos padronizados")
plt.savefig("qq-plot.png")

import scipy.stats as stats
w, pvalue = stats.shapiro(model.resid)
print('Shapiro: ', w, pvalue)
print()

from bioinfokit.analys import stat 
res = stat()
res.levene(df=df_melt, res_var='HorarioH', xfac_var='RegiãoSexo')
print(res.levene_summary)
