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

# Sidebar
with st.sidebar:
    page = st.radio(
        "Explore",
        ("Home", "Teoria", "Simulações")
    )

if (page == "Home"):
    st.title('Marcação a mercado no Tesouro Direto')
    st.subheader('Títulos disponíveis* para simulação**')
    st.write('Escolha uma opção ao lado (Teoria ou Simulações) para mais informações.')
    st.dataframe(df.set_index('TÍTULO'))
    st.write('''<p1 style="font-size: small" style="text-align: left;">
                *Foram listados acima apenas os títulos vendidos direto pelo portal do tesouro direto e com rendimento atrelado ao IPCA ou prefixados.</p1>''',unsafe_allow_html=True)
    st.write('''<p1 style="font-size: small" style="text-align: left;">
                **Não é recomendação de investimento. A ferramenta deve ser utilizada apenas para cálculos sem compromisso.</p1>''',unsafe_allow_html=True)

elif (page == "Teoria"):
    st.title('O que é marcação a mercado?')
    st.write('Ainda que os títulos públicos, "prometam" uma taxa de rentabilidade na hora da compra, essas taxas flutuam e, com elas, o valor dos investimentos. Marcação a mercado é a atualização dos valores de um investimento com base nas flutuações das taxas. Em outras palavras, é o valor de resgate do investimento, caso esse seja feito antes do seu vencimento.')
    st.write('Essa variação, por si só, não é necessariamente algo positivo ou negativo. Depende do investidor entender como e porquê essas flutuações ocorrem e agir de acordo com o que faz mais sentido.')
    st.write('É principalmente por isso que os títulos públicos, ainda que possibilitando o resgate diário, não são recomendados de forma uniforme ao público. Um resgate antecipado por necessidade por trazer grandes perdas ao investidor, bem como um resgate planejado pode assimilar ganhos extraordinários.')
    st.subheader('Aprenda mais nos vídeos abaixo:')
    container1 = st.container()
    col1, col2 = container1.columns(2)
    with col1:
        st.video('https://www.youtube.com/watch?v=BUnpkmVIwgo')
        st.video('https://www.youtube.com/watch?v=WTKueE2P_Vk')
    with col2:
        st.video('https://www.youtube.com/watch?v=ll7EB32XM_g')
        st.video('https://www.youtube.com/watch?v=wQqFypK4o4A')

else: 
    st.title('Simulação')
    st.subheader('Título escolhido:')

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

    df_show = df[df['TÍTULO'] == titulo].set_index('TÍTULO')
    st.dataframe(df_show)
    data_vencimento = df[df['TÍTULO'] == titulo]['VENCIMENTO'].tolist()[0]
    valor_titulo = float(df[df['TÍTULO'] == titulo]['VALOR TÍTULO'].tolist()[0].split(' ')[1].replace('.', '').replace(',','.'))
    numero_de_titulos = valor_investido / valor_titulo
    

    if (data_resgate > format_date(data_vencimento)):
        st.error("Escolha uma data menor que a data de vencimento do título.")
    else:

        today = datetime.date.today()
        periodo = pd.date_range(today, data_resgate, freq='D').strftime("%Y-%m-%d").tolist()
        rendimentos = pd.DataFrame({'Data':periodo})

        
        rendimentos['Intervalo de tempo'] = rendimentos['Data'].apply(lambda x: len(pd.date_range(today, x, freq = 'D').tolist())/365)
        rendimentos['Poupança'] = rendimentos['Intervalo de tempo'].apply(lambda x: valor_investido * ((1.005 ** 12 + 0.00048) ** x) if selic >= 8.5    else valor_investido * ((selic * 0.7) / 100 + 1 + 0.00048) ** x)
        rendimentos['SELIC'] = rendimentos['Intervalo de tempo'].apply(lambda x: valor_investido * calculo_de_rendimento(selic, x))
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

        container1 = st.container()
        col1, col2 = container1.columns([1, 3])
        container2 = col2.container()
        container3 = col2.container()
        tab1, tab2 = container3.tabs(["📈 Gráfico", "🗃 Dados"])

        data_resgate = datetime.datetime.strftime(data_resgate, '%Y-%m-%d')
        df_barplot = rendimentos[rendimentos['Data'] == data_resgate][['Poupança', 'SELIC', 'Inflação (IPCA)', 'Tesouro direto (teórico)', 'Tesouro direto (real)']].astype(str).T.reset_index()
        df_barplot.columns = ['Comparação','valor']
        df_barplot['valor'] = df_barplot['valor'].apply(lambda x: ((float(x) / valor_investido) - 1 ) * 100)
        df_barplot['valor_str'] = df_barplot['valor'].map('{:,.2f}%'.format)

        with col1:
            data_resgate = data_resgate.split('-')[2] + '/' + data_resgate.split('-')[1] + '/' + data_resgate.split('-')[0]
            st.markdown("<h3 style='text-align: center;'>""</h3>", unsafe_allow_html=True) #Empty line
            st.markdown("<h3 style='text-align: center;'>""</h3>", unsafe_allow_html=True) #Empty line
            st.markdown("<h3 style='text-align: center;'>Dados da simulação:</h3>", unsafe_allow_html=True)
            st.text("") #Empty line
            st.write(
                    """
                    -   Título selecionado: {}
                    -   Valor investido: R$ {:.2f}
                    -   Data de resgate: {}
                    -   Taxa SELIC escolhida: {}%
                    -   Taxa IPCA escolhida: {}%
                    -   Taxa prefixada escolhida: {}%
                    """.format(titulo.capitalize(), valor_investido, data_resgate, str(selic), str(ipca), str(taxa_resgate)))
            st.text("") #Empty line
            st.text("") #Empty line
            st.markdown("<h3 style='text-align: center;'>Interpretação dos resultados**</h3>", unsafe_allow_html=True)
            st.text("") #Empty line
            st.write('<p style="text-align: left;">Os valores calculados devem ser lidos como resposta às perguntas:</p>', unsafe_allow_html=True)
            st.write('''
                    -   Qual seria o total resgatado se R$ {} fossem deixados nesse investimento até {}?
                    -   Qual a variação da inflação e da SELIC durante esse período?"
                    '''.format(int(valor_investido), data_resgate))
            st.write('<p style="text-align: left;">Assim, a simulação indica que, na poupança, o dinheiro renderia {}. Já no tesouro direto, o rendimento seria de {} por conta da marcação a mercado e do resgate antecipado. Caso fosse deixado até o vencimento, pode-se considerar um rendimento téorico no tesouro direto de {} em {}.</p>'
                    .format(df_barplot[df_barplot['Comparação'] == 'Poupança']['valor_str'].tolist()[0],
                    df_barplot[df_barplot['Comparação'] == 'Tesouro direto (real)']['valor_str'].tolist()[0], 
                    df_barplot[df_barplot['Comparação'] == 'Tesouro direto (teórico)']['valor_str'].tolist()[0], 
                    data_resgate), 
                    unsafe_allow_html=True)
            st.write('<p style="text-align: left;">Ademais, durante esse período, a inflação avançará {} e a SELIC {}.</p>'
                    .format(df_barplot[df_barplot['Comparação'] == 'Inflação (IPCA)']['valor_str'].tolist()[0],
                    df_barplot[df_barplot['Comparação'] == 'SELIC']['valor_str'].tolist()[0]), 
                    unsafe_allow_html=True)

        fig = px.line(rendimentos, x='Data', y=['Poupança', 'SELIC', 'Inflação (IPCA)', 'Tesouro direto (teórico)', 'Tesouro direto (real)'], labels = {'Data' : 'Data de resgate', 'value' : 'Valor de resgate  /  Variação (R$)', 'variable' : 'Variável'}, hover_data={'Data' : False})
        fig.update_layout(hovermode="x unified", title = {'text' : 'Variação do retorno com o tempo','xanchor': 'left'})
        container2.plotly_chart(fig, use_container_width=True)

        fig = px.bar(df_barplot, x='Comparação', y = 'valor', text = 'valor_str', labels = {'valor' : 'Rendimento  /  Variação (%)'},hover_data= {'Comparação': False, 'valor' : False, 'valor_str' : False})
        fig.update_layout(title = {'text' : 'Expectativa percentual do retorno','xanchor': 'left'})
        tab1.plotly_chart(fig, use_container_width=True)
        df_show = df_barplot[['Comparação', 'valor_str']].set_index('Comparação')
        df_show.columns = ['Valor']
        tab2.dataframe(df_show)
        
        st.text("") #Empty line
        st.write('''<p1 style="font-size: small" style="text-align: left;">
                *Não é recomendação de investimento. A ferramenta deve ser utilizada apenas para cálculos sem compromisso.</p1>''',unsafe_allow_html=True)
        st.write('''<p1 style="font-size: small" style="text-align: left;">
                **Os resultados mostrados são brutos de imposto de renda e aproximados por conta do cálculo de dias úteis. Além disso, não consideram a taxa de custódia da B3 ou taxas das corretoras.</p1>''',unsafe_allow_html=True)
        
    
# ---- HIDE STREAMLIT STYLE
hide_st_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>    
                ''' 
st.markdown(hide_st_style, unsafe_allow_html=True)                