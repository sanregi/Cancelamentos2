
# Configuração da página
st.set_page_config(
    page_title="Projeto | Análise de dados com Python",
    layout="wide",
    initial_sidebar_state="auto",
)

# Etapa 1:
st.markdown('''
## Case - Cancelamento de Clientes <a name="1"></a>
''', unsafe_allow_html=True)

st.markdown('''
Você foi contratado por uma empresa com mais de 800 mil clientes para um projeto de Dados. Recentemente a empresa percebeu que da sua base total de clientes, a maioria são clientes inativos, ou seja, que já cancelaram o serviço.
Precisando melhorar seus resultados ela quer conseguir entender os principais motivos desses cancelamentos e quais as ações mais eficientes para reduzir esse número.
''')

import pandas as pd
import streamlit as st
import plotly.express as px
import sklearn

# Carrega os dados
@st.cache_data
def load_data():
    tabela = pd.read_csv("cancelamentos.csv")
    return tabela

tabela = load_data()

# Remove a coluna CustomerID
tabela = tabela.drop("CustomerID", axis=1)

# Mostra a tabela
st.write("### Tabela de Dados")
st.write(tabela)

# Informações da tabela
st.write("### Informações da Tabela")
st.write(tabela.info())

# Remove linhas com valores ausentes
tabela = tabela.dropna()

# Mostra as informações após a remoção de valores ausentes
st.write("### Informações da Tabela Após Remoção de Valores Ausentes")
st.write(tabela.info())

# Contagem de cancelamentos
st.write("### Contagem de Cancelamentos")
st.write(tabela["cancelou"].value_counts())

# Porcentagem de cancelamentos
st.write("### Porcentagem de Cancelamentos")
st.write(tabela["cancelou"].value_counts(normalize=True).map("{:.1%}".format))

# Contagem de duração do contrato
st.write("### Contagem de Duração do Contrato")
st.write(tabela["duracao_contrato"].value_counts(normalize=True))
st.write(tabela["duracao_contrato"].value_counts())

# Média por duração do contrato
st.write("### Média por Duração do Contrato")
st.write(tabela.groupby("duracao_contrato").mean(numeric_only=True))

# Remove entradas de contrato mensal
tabela = tabela[tabela["duracao_contrato"] != "Monthly"]

# Mostra a tabela após remoção de contratos mensais
st.write("### Tabela após Remoção de Contratos Mensais")
st.write(tabela)

# Contagem de cancelamentos após remoção de contratos mensais
st.write("### Contagem de Cancelamentos após Remoção de Contratos Mensais")
st.write(tabela["cancelou"].value_counts())
st.write(tabela["cancelou"].value_counts(normalize=True).map("{:.1%}".format))

# Contagem de assinaturas
st.write("### Contagem de Assinaturas")
st.write(tabela["assinatura"].value_counts(normalize=True))

# Média por tipo de assinatura
st.write("### Média por Tipo de Assinatura")
st.write(tabela.groupby("assinatura").mean(numeric_only=True))

# Cria histogramas interativos
for coluna in tabela.columns:
    grafico = px.histogram(tabela, x=coluna, color="cancelou")
    st.plotly_chart(grafico)

# Filtra linhas com menos de 5 ligações ao call center e menos de 20 dias de atraso
tabela = tabela[(tabela["ligacoes_callcenter"] < 5) & (tabela["dias_atraso"] <= 20)]

# Mostra a tabela após a filtragem
st.write("### Tabela após Filtragem")
st.write(tabela)

# Contagem de cancelamentos após a filtragem
st.write("### Contagem de Cancelamentos após Filtragem")
st.write(tabela["cancelou"].value_counts())
st.write(tabela["cancelou"].value_counts(normalize=True).map("{:.1%}".format))


"""# INSIGHTS

Taxa atual de 56% de cancelamentos.

# 3 principais causas de cancelamento:
    atraso no pagamento
    Necessidade de ligações para o call center
    forma de contrato


# Atraso no pagamento;
    Os graficos sugerem que clientes com 20 dias ou mais de atraso estão mais propensos ao cancelamento.

# Necessidade de ligações para o call center
    Clientes que ligam para o call center acima de 5x tendem mais ao cancelamento do plano.

# forma de contrato
    Clientes que possuem planos mensais tendem a cancelar mais do que os que possuem planos trimestrais e anuais.




## Implementações para resolução na taxa atual de cancelamentos.

# 1 -  Criar nova politica de cobrança
    Sms lembrete de pagamento de contas
    ligações após XX dias de atraso
    incentivos ao pagamento de faturas em atraso.

# 2 - Traçar plano com o call center
    Cliente com problema é cliente insatisfeito.
    Apartir de data xx/xx , todos os problemas de clientes que ligam no call center, devem ser resolvidos em até no maximo 3 ligações do mesmo.

# 3 - Descontos em assinaturas
    Desconto em assinaturas trimestrais e anuais.
    incentivos a contratações de planos maiores.


Segundo as previsões, a taxa de cancelamento com essas implementações poderão cair de 56% para 18%.

"""
