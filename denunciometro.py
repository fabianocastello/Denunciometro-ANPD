import pandas as pd
import numpy as np
pd.options.display.max_columns = None
import warnings
warnings.simplefilter(action='ignore')
import socket
import time
from PIL import Image
from datetime import datetime
runningOn =  socket.gethostname()
import requests
from random import randrange

######################### TEMP
######################### TEMP

    
def run():
    global inicio, final, ped
    
    # https://www.markdownguide.org/basic-syntax/
    with st.beta_expander('Leia-Me!', expanded=False):
        st.write('✅ Denunciómetro foi criado para publicar dados referentes à denúncias feitas a Agência Nacional de Proteção de Dados (ANPD), no contexto da Lei Geral de Proteção de dados (LGPD). **O conteúdo das denúncias não é disponibilizado**.')
        st.write('✅ as informações e gráficos são compiladas a partir de dados públicos da CGU, que estão disponíveis em https://falabr.cgu.gov.br/publico/DownloadDados/DownloadDadosLai.aspx. Para opções use a barra lateral (clique ">" no topo esquerdo da página).')
        st.write('✅ Denunciómetro é uma inciativa da DPO3, startup com foco na aderência à LGPD com planos a partir de R$19/mês. Conheça e experimente gratuitamente por 14 dias em http://www.dpo3.com.br.')
        
    ################################## Opções
    st.sidebar.write('Opções de seleção. Para reset geral pressione F5.')

    from datetime import time
    from datetime import date
    inicio,final = st.sidebar.slider(
        "Período para considerar:",
        value=(inicio, final))
    ped = ped[(ped.Data != 'ND') & (ped.Data>=inicio) & (ped.Data<=final)]
    
    opts    = []
    choices = []
    for index, value in enumerate(ped['AssuntoPedido'].unique()):
        if value=='ND':continue
        opts.append(value)
        choices.append(True)
    st.sidebar.write('Assuntos:')
    for i in range(len(opts)):
        choices[i] = st.sidebar.checkbox(opts[i], value=choices[i])
    choosen = []    
    for i in range(len(opts)):
        if choices[i]: choosen.append(opts[i])
    ped = ped[ped['AssuntoPedido'].isin(choosen)].reset_index(drop=True)
    
        
    ################################## Highligths
    st.markdown(f'''<body><p style="font-size:18px;line-height: 25px;color:DeepSkyBlue  ">
    <i><b>Destaques e informações:</b></i></p></body>''', unsafe_allow_html=True)
    hl = []
    search = ['incidente', 'vazamentos']
    cont = 0
    for index, row in ped.iterrows():
        present = False
        for i in search:
            if i.lower() in row['AssuntoPedido'].lower(): present = True
            if i.lower() in row['SubAssuntoPedido'].lower(): present = True
        if present: cont += 1
    #incidentes de segurança
    hl.append(f"""🔥 Existem {cont} entradas que mencionam "{' e/ou '.join(search)}".""")
    for i in hl:
        st.write(i)
    st.write("📅 As informações são referentes ao período de "+\
                 datetime.strftime(inicio, '%d/%m/%Y')+" até "+\
                 datetime.strftime(final, '%d/%m/%Y')+".")

    ################################## GERAL
    st.markdown(f'''<body><p style="font-size:18px;line-height: 25px;color:DeepSkyBlue  ">
    <i><b>Distribuição dos {ped.shape[0]:,} pedidos e denúncias ao longo do tempo:</b></i></p></body>''', unsafe_allow_html=True)
    st.bar_chart(ped.groupby('Periodo').size(),
                          use_container_width=True)
                          
    ################################## ASSUNTOS
    tmp = ped
    if tmp[tmp.AssuntoPedido=='ND'].shape[0] == 0:
        head_gráfico = f'Distribuição dos {tmp.shape[0]:,} pedidos e denúncias de acordo com assunto:'
    else:
        count  = tmp[tmp.AssuntoPedido=='ND'].shape[0]
        remain = tmp.shape[0] - count
        head_gráfico = f'Sobre os assuntos, existem {count:,} assunto(s) não especificado(s). Os demais {remain:,} tem a seguinte distribuição:'
        tmp = tmp[tmp.AssuntoPedido!='ND']
        tmp.reset_index(drop=True, inplace=True)

    st.markdown(f'''<body><p style="font-size:18px;line-height: 25px;color:DeepSkyBlue  ">{head_gráfico}</b></i></p></body>''', unsafe_allow_html=True)
    st.bar_chart(tmp.groupby('AssuntoPedido').size(),
                          use_container_width=True)

    ################################## SUB-ASSUNTOS
    tmp = ped
    if tmp[tmp.SubAssuntoPedido=='ND'].shape[0] == 0:
        head_gráfico = f'Distribuição dos {tmp.shape[0]:,} pedidos e denúncias de acordo com detalhamento do assunto (subassunto):'
    else:
        count  = tmp[tmp.SubAssuntoPedido=='ND'].shape[0]
        remain = tmp.shape[0] - count
        head_gráfico = f'Sobre o detalhamento dos assuntos (subassuntos), existem {count:,} entrada(s) não especificada(s). As demais {remain:,} tem a seguinte distribuição:'
        tmp = tmp[tmp.SubAssuntoPedido!='ND']
        tmp.reset_index(drop=True, inplace=True)

    st.markdown(f'''<body><p style="font-size:18px;line-height: 25px;color:DeepSkyBlue  ">{head_gráfico}</b></i></p></body>''', unsafe_allow_html=True)
    st.bar_chart(tmp.groupby('SubAssuntoPedido').size(),
                          use_container_width=True)

    ################################## Municipios
    tmp = ped
    if tmp[tmp.s_Municipio=='ND'].shape[0] == 0:
        head_gráfico = f'Distribuição dos {tmp.shape[0]:,} pedidos e denúncias de acordo o estado do solicitante:'
    else:
        count  = tmp[tmp.s_Municipio=='ND'].shape[0]
        remain = tmp.shape[0] - count
        head_gráfico = f'Sobre o estado dos solicitantes, existem {count:,} entrada(s) não especificada(s). As demais {remain:,} tem a seguinte distribuição:'
        tmp = tmp[tmp.s_Municipio!='ND']
        tmp.reset_index(drop=True, inplace=True)

    st.markdown(f'''<body><p style="font-size:18px;line-height: 25px;color:DeepSkyBlue  ">{head_gráfico}</b></i></p></body>''', unsafe_allow_html=True)
    st.bar_chart(tmp.groupby('s_Municipio').size(),
                          use_container_width=True)

    st.map(tmp[['lat','lon']],use_container_width=True)
    
       
    with st.beta_expander('Veja a tabela completa', expanded=False):
        show = ped[['Periodo','DataRegistro', 'DataResposta', 'Esfera',
                    'ProtocoloPedido', 'Situacao', 'Decisao', 'EspecificacaoDecisao', 
                    'AssuntoPedido', 'SubAssuntoPedido', 's_Genero', 's_Idade',  'UF_loc', 'Cidade']]
        show.rename({'s_Genero': 'Gênero',
                     's_Idade' : 'Idade',
                     'UF_loc'  : 'UF'}, axis=1,inplace=True)
        show['Idade'] = show['Idade'].astype(str)
        st.dataframe(show.fillna('ND'))
        

    return()
def registro(remarks=None):
    form_data = { 'entry.2093722949'  : 'Denunciómetro',
                  'entry.442023490' : 'IP',
                  'entry.225285568'   : runningOn,
                  'entry.1052496244'   : remarks}
    ret = requests.post(url_post+'/formResponse', data=form_data, headers=
             {'Referer':url_post+'/viewform',
              'User-Agent': UserAgents[randrange(len(UserAgents))]})
    return(True)
    
import streamlit as st 
try: st.set_page_config(
        page_title="Validação de Hashs de Laudos",
        initial_sidebar_state="collapsed")
except: pass
from streamlit import caching
hide_streamlit_style = """<style>#MainMenu {visibility: hidden;}
                          footer {visibility: hidden;}
                          </style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#### CONFIG
with open("./UserAgents.cfg",encoding='utf-8') as f:
     UserAgents = f.readlines(); f.close()
UserAgents = [c.replace('\n','').strip() for c in UserAgents]
if not runningOn == 'localhost':
    import configparser
    config_parser = configparser.RawConfigParser()
    config_parser.read('./Denunciometro.ini')
    url_post  = config_parser.get('RUN', 'url_post')
else:
    url_post = st.secrets["url_post"]
    
global inicio, final
with open('00LastUpdate.txt', 'r', encoding='utf-8') as base:
    content = base.read().split('\n') 
    last   = content[0]
    inicio = datetime.strptime(content[1], '%Y-%m-%d %H:%M:%S')
    final  = datetime.strptime(content[2], '%Y-%m-%d %H:%M:%S')

def load_data():
    with st.spinner('Carregando dados'):
        ped      = pd.read_pickle('00Ped.pkl')
        rec      = pd.read_pickle('00Recl.pkl')
    return(ped, rec)
ped, rec = load_data()

#### CABEC
from pathlib import Path
import base64

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    img_to_bytes("BannerDPO3.png")
)
st.markdown(
    header_html, unsafe_allow_html=True
)
    
st.markdown(f'''<body>
<p style="font-size:30px;line-height: 25px"><b><br>Denunciómetro LGPD</b><br><span style="font-size: 12pt;"><i>denuncias realizadas junto à ANPD no contexto da LGPD</i></span>
<span style="font-size: 8pt;"><br><i>atualizado até {last}</i></span>
    </p></body>''', unsafe_allow_html=True)

run()


#HTML Colors: https://www.w3schools.com/colors/colors_groups.asp






