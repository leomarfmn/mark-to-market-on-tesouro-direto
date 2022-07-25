'''
1. Add footer:  st.footer('Esse app atualiza os títulos e informações disponíveis uma vez por dia, regularmente.')
2. Edit information on page 'Teoria'.
2.1 Add tl;dr section
2.2 Add one more video
3. Taxa referencial
4. Inverter a ordem dos dados na data
5. Adicionar uma nota de rodapé: Disclaimer: esse não é um site oficial do TD, não tem relação com os vídeos e não deve ser considerado recomendação de investimento. As informações obtidas aqui, devem apenas ser utilizadas como apoio na tomada autônoma de decisão.
6. Inserir nota de rodapé na página de simulação: os valores calculados não levam em consideração as taxas de custódia cobradas pelo Banco Central, nem as taxas de corretagem possivelmente cobradas pelas corretoras. 
7. Ajustar largura das dataframes na página
8. Format page
9. 10 feriados por ano
'''

from turtle import width
from unittest import skip
import pandas as pd
import numpy as np
import streamlit as st
import datetime
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache
def get_data():
    df = pd.read_csv('df.csv', usecols= ['TÍTULO', 'TAXA', 'VALOR MÍNIMO', 'VALOR TÍTULO', 'VENCIMENTO'])
    df['VENCIMENTO'] = df['VENCIMENTO'].apply(lambda x: x.split('-')[2] + '/' + x.split('-')[1] + '/' + x.split('-')[0] )
    df['TÍTULO'] = df['TÍTULO'].apply(lambda x: 'flag' if 'selic' in str.lower(x) else (x if 'juros' not in str.lower(x) else 'flag'))
    df = df[df['TÍTULO'] != 'flag']
    return df

def calculo_de_rendimento(taxa, x):
    return (((taxa / 100) + 1) ** x)

def format_date(data):
    return datetime.datetime.strptime(data, '%d/%m/%Y').date()

def date_diff(a, b):
    return np.busday_count(a, b)

TR = 0.00048
df = get_data()
#df = df[~df['TÍTULO'].str.contains('juros')]

# Sidebar
with st.sidebar:
    page = st.radio(
        "Explore",
        ("Home", "Teoria", "Simulações")
    )

if (page == "Home"):
    st.title('Marcação a mercado no Tesouro Direto')
    st.subheader('Títulos disponíveis para simulação*')
    st.write('Escolha uma opção ao lado (Teoria ou Simulações) para mais informações.')
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),line_color='darkslategray',
    fill_color='royalblue',
    align='center',
    height = 45),
    cells=dict(values=[df['TÍTULO'],df['TAXA'],df['VALOR MÍNIMO'],df['VALOR TÍTULO'],df['VENCIMENTO']],
    line_color='darkslategray',
    fill_color='green',
    align='center',
    height = 45))])
    fig.update_layout(
    height = 1500,
    margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig)

elif (page == "Teoria"):
    st.title('O que é marcação a mercado?')
    st.subheader('Aprenda mais nos vídeos abaixo:')
    st.video('https://www.youtube.com/watch?v=BUnpkmVIwgo')

else: 
    st.title('Simulação')

    with st.sidebar:
        titulo = st.selectbox('Selecione o título',(df['TÍTULO']))

        valor_investido = st.number_input('Insira o valor em reais para a simulação', min_value=0, value=1000)

        data_resgate = st.date_input(
        "Selecione a data de resgate antecipada (ano/mês/dia)",datetime.datetime.today() + datetime.timedelta(365), max_value = datetime.date(2100,12,1))

        selic = st.slider('Escolha a taxa SELIC para o período (%)', 2.0, 18.0, 7.5, step = 0.25)
        ipca = st.slider('Escolha o IPCA médio para o período (%)', 0.0, 15.0, 6.0, step = 0.25)
        if 'PREFIXADO' in titulo: 
            taxa_resgate = st.slider('Escolha a taxa prefixada no momento do resgate', 6.0, 20.0, 11.0, step = 0.25)
        else:
            taxa_resgate = st.slider('Escolha a taxa prefixada no momento do resgate', 2.0, 9.0, 5.0, step = 0.25)
        st.info('Para mais informações sobre a taxa SELIC, visite: https://www.bcb.gov.br/controleinflacao/taxaselic')
        st.info('Para mais informações sobre o IPCA, visite: https://www.bcb.gov.br/controleinflacao/indicepreco')

    
    st.write(df[df['TÍTULO'] == titulo])
    data_vencimento = df[df['TÍTULO'] == titulo]['VENCIMENTO'].tolist()[0]
    valor_titulo = float(df[df['TÍTULO'] == titulo]['VALOR TÍTULO'].tolist()[0].split(' ')[1].replace('.', '').replace(',','.'))
    numero_de_titulos = valor_investido / valor_titulo
    

    if (data_resgate > format_date(data_vencimento)):
        st.error("Escolha uma data menor que a data de vencimento do título.")
    else:
        st.write('Valor investido R$ {:.2f}'.format(valor_investido))
        st.write("Data selecionada: " + data_resgate.strftime('%d-%b-%Y'))
        st.write("Taxa SELIC escolhida: " + str(selic) + '%')
        st.write("Taxa IPCA escolhida: " + str(ipca) + '%')
        st.write("Taxa prefixada escolhida: " + str(taxa_resgate) + '%')

        today = datetime.date.today()
        periodo = pd.date_range(today, data_resgate, freq='D').strftime("%Y-%m-%d").tolist()
        rendimentos = pd.DataFrame({'Data':periodo})

        
        rendimentos['Intervalo de tempo'] = rendimentos['Data'].apply(lambda x: len(pd.date_range(today, x, freq = 'D').tolist())/365)
        rendimentos['Poupança'] = rendimentos['Intervalo de tempo'].apply(lambda x: valor_investido * ((1.005 ** 12 + 0.00048) ** x) if selic >= 8.5    else valor_investido * ((selic * 0.7) / 100 + 1 + 0.00048) ** x)
        rendimentos['Selic'] = rendimentos['Intervalo de tempo'].apply(lambda x: valor_investido * calculo_de_rendimento(selic, x))
        rendimentos['Inflação (IPCA)'] = rendimentos['Intervalo de tempo'].apply(lambda x: valor_investido * calculo_de_rendimento(ipca, x))
        
        if ('PREFIXADO' in titulo):
            taxa_contratada = float(df[df['TÍTULO'] == titulo]['TAXA'].tolist()[0].replace(',','.').replace('%', ''))
            rendimentos['Tesouro direto (teórico)'] = rendimentos['Intervalo de tempo'].apply(lambda x: valor_investido * calculo_de_rendimento(taxa_contratada, x))
            rendimentos['Tesouro direto (real)'] = rendimentos['Data'].apply(lambda x: numero_de_titulos * (1000 / ( 1 + taxa_resgate / 100) ** (date_diff(x, format_date(data_vencimento)) / 252)))
        else:
            taxa_contratada = float(df[df['TÍTULO'] == titulo]['TAXA'].tolist()[0].split(' ')[2].replace(',','.').replace('%', ''))
            dias_da_compra_ate_vencimento = date_diff(today, format_date(data_vencimento))
            dias_do_resgate_ate_vencimento = date_diff(data_resgate, format_date(data_vencimento))
            percentual_do_vna_inicial = 100 / ((1 + taxa_contratada / 100) ** (dias_da_compra_ate_vencimento / 252)) / 100
            percentual_do_vna_final = 100 / ((1 + taxa_resgate / 100) ** (dias_do_resgate_ate_vencimento / 252)) / 100
            vna_inicial = valor_titulo / percentual_do_vna_inicial
            rendimentos['Tesouro direto (teórico)'] = rendimentos['Intervalo de tempo'].apply(lambda x: valor_investido * (((ipca / 100 + 1) * (taxa_contratada / 100 + 1)) ** x))
            rendimentos['Tesouro direto (real)'] = rendimentos['Intervalo de tempo'].apply(lambda x: numero_de_titulos * percentual_do_vna_final * vna_inicial * (1 + ipca / 100) ** x)
            
    

        rendimentos.drop(['Intervalo de tempo'], axis = 1 , inplace=True)
        st.dataframe(rendimentos)
        data_resgate = datetime.datetime.strftime(data_resgate, '%Y-%m-%d')
        df_barplot = rendimentos[rendimentos['Data'] == data_resgate][['Poupança', 'Selic', 'Inflação (IPCA)', 'Tesouro direto (teórico)', 'Tesouro direto (real)']].astype(str).T.reset_index()
        df_barplot.columns = ['Comparação','valor']
        df_barplot['valor'] = df_barplot['valor'].apply(lambda x: ((float(x) / valor_investido) - 1 ) * 100)
        df_barplot['valor_str'] = df_barplot['valor'].map('{:,.2f}%'.format)
        st.write(df_barplot)

        fig = px.bar(df_barplot, x='Comparação', y = 'valor', text = 'valor_str')
        st.plotly_chart(fig, use_container_width=True)

        fig = px.line(rendimentos, x='Data', y=['Poupança', 'Selic', 'Inflação (IPCA)', 'Tesouro direto (teórico)', 'Tesouro direto (real)'])
        st.plotly_chart(fig, use_container_width=True)

        
    
        