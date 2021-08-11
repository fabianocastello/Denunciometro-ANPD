import pandas as pd
import numpy as np
pd.options.display.max_columns = None
import warnings
warnings.simplefilter(action='ignore')
import socket
import os
import time
from PIL import Image
from datetime import datetime
runningOn =  socket.gethostname()
import requests
from random import randrange
from glob import glob
import zipfile
from unidecode import unidecode
 
global running_date
running_date = datetime.now().strftime("%d-%m-%Y %Hh%Mm")


######################### TEMP
######################### TEMP

    
def run():
    global inicio, final, ped
    registro()
    
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
        page_title="DPO3 - Denunciómetro LGPD",
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

def update():
    try:
        from lxml import etree
        with st.spinner('Atualizando dados. Aguarde ~2 minutos'):
            ############################################## UPDATE
            ############################################## UPDATE
            ############################################## UPDATE
            with st.spinner('Baixando dados de CGU.gov.br'):
                try: os.mkdir('TEMP')
                except: pass
                files = glob('./TEMP/*')
                for f in files:
                    os.remove(f)
                url = r'https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR/Pedidos_xml_2021.zip'
                output = r'./TEMP/pedidos2021.zip'
                try:
                    r = requests.get(url)
                except:
                    return(False)
                with open(output, 'wb') as f:
                    f.write(r.content) 
                with zipfile.ZipFile(r'./TEMP/pedidos2021.zip', 'r') as zip_ref:
                    zip_ref.extractall(r'./TEMP')
        
                url = r'https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR/Recursos_Reclamacoes_xml_2021.zip'
                output = r'./TEMP/reclamações2021.zip'
                try:
                    r = requests.get(url)
                except:
                    return(False)
                with open(output, 'wb') as f:
                    f.write(r.content)
                    
                with zipfile.ZipFile(r'./TEMP/reclamações2021.zip', 'r') as zip_ref:
                    zip_ref.extractall(r'./TEMP')
            with st.spinner('Processando Pedidos'):
                files = glob('./TEMP/*.xml')
                for f in files:
                    if '_pedidos_' in f.lower():
                        file = f
                        break
                df = pd.DataFrame()
                tree = etree.parse(f)
                root = tree.getroot()
                elementos = root.xpath(".//Pedido")
                for each in elementos:
                    if not 'ANPD' in each.get('OrgaoDestinatario',None): continue
                    rec = dict()
                    rec['IdPedido']              = each.get('IdPedido',None)
                    rec['ProtocoloPedido']       = each.get('ProtocoloPedido',None)
                    rec['Esfera']                = each.get('Esfera',None)
                    rec['UF']                    = each.get('UF',None)
                    rec['OrgaoDestinatario']     = each.get('OrgaoDestinatario',None)
                    rec['Situacao']              = each.get('Situacao',None)
                    rec['DataRegistro']          = each.get('DataRegistro',None)
                    rec['FoiProrrogado']         = each.get('FoiProrrogado',None)
                    rec['FoiReencaminhado']      = each.get('FoiReencaminhado',None)
                    rec['FormaResposta']         = each.get('FormaResposta',None)
                    rec['OrigemSolicitacao']     = each.get('OrigemSolicitacao',None)
                    rec['IdSolicitante']         = each.get('IdSolicitante',None)
                    rec['AssuntoPedido']         = each.get('AssuntoPedido',None)
                    rec['SubAssuntoPedido']      = each.get('SubAssuntoPedido',None)
                    rec['DataResposta']          = each.get('DataResposta',None)
                    rec['Decisao']               = each.get('Decisao',None)
                    rec['EspecificacaoDecisao']  = each.get('EspecificacaoDecisao',None)
                    df = df.append(rec, ignore_index=True)
                df['UF'] = df['UF'].apply(lambda x: None if pd.isna(x) else x.replace('DISTRITO FEDERAL','DF') )
                ped = df
            with st.spinner('Processando Solicitantes de Pedidos'):
                solANPD = list(set(list(ped['IdSolicitante'].unique())))
                files = glob('./TEMP/*.xml')
                for f in files:
                    if '_solicitantespedidos_' in f.lower():  
                        file = f
                        break
                df = pd.DataFrame()
                tree = etree.parse(f)
                root = tree.getroot()
                elementos = root.xpath(".//Solicitante")
                for each in elementos:
                    if not each.get('IdSolicitante',None) in solANPD: continue
                    rec = dict()
                    rec['IdSolicitante']    = each.get('IdSolicitante',None)
                    rec['TipoDemandante']   = each.get('TipoDemandante',None)
                    rec['DataNascimento']   = each.get('DataNascimento',None)
                    rec['Genero']           = each.get('Genero',None)
                    rec['Pais']             = each.get('Pais',None)
                    rec['UFs']              = each.get('UF',None)
                    rec['Municipio_s']      = each.get('Municipio',None)
                    df = df.append(rec, ignore_index=True)
                df['UFs'] = df['UFs'].apply(lambda x: None if pd.isna(x) else x.replace('DISTRITO FEDERAL','DF') )
                sol = df
            with st.spinner('Processando Recursos e Reclamações'):
                files = glob('./TEMP/*.xml')
                for f in files:
                    if '_recursos_reclamacoes_' in f.lower():  
                        file = f
                        break
                df = pd.DataFrame()
                from lxml import etree
                tree = etree.parse(f)
                root = tree.getroot()
                elementos = root.xpath(".//Recurso")
                for each in elementos:
                    if not 'ANPD' in each.get('OrgaoDestinatario',None): continue
                    rec = dict()
                    rec['IdRecurso']          = each.get('IdRecurso',None)
                    rec['IdPedido']           = each.get('IdPedido',None)
                    rec['IdSolicitante']      = each.get('IdSolicitante',None)
                    rec['ProtocoloPedido']    = each.get('ProtocoloPedido',None)
                    rec['Esfera']             = each.get('Esfera',None)
                    rec['UF']                 = each.get('UF',None)
                    rec['Municipio']          = each.get('Municipio',None)
                    rec['OrgaoDestinatario']  = each.get('OrgaoDestinatario',None)
                    rec['Instancia']          = each.get('Instancia',None)
                    rec['Situacao']           = each.get('Situacao',None)
                    rec['DataRegistro']       = each.get('DataRegistro',None)
                    rec['PrazoAtendimento']   = each.get('PrazoAtendimento',None)
                    rec['OrigemSolicitacao']  = each.get('OrigemSolicitacao',None)
                    rec['TipoRecurso']        = each.get('TipoRecurso',None)
                    rec['DataResposta']       = each.get('DataResposta',None)
                    rec['TipoResposta']       = each.get('TipoResposta',None)
                    df = df.append(rec, ignore_index=True)
                df['UF'] = df['UF'].apply(lambda x: None if pd.isna(x) else x.replace('DISTRITO FEDERAL','DF') )
                recl = df              
            
            with st.spinner('Processando Solicitantes de Recursos e Reclamações'):
                solANPD = list(set(list(recl['IdSolicitante'].unique())))
                files = glob('./TEMP/*.xml')
                for f in files:
                    if '_solicitantesrecursos_' in f.lower():  
                        file = f
                        break
                df = pd.DataFrame()
                from lxml import etree
                tree = etree.parse(f)
                root = tree.getroot()
                elementos = root.xpath(".//Solicitante")
                for each in elementos:
                    if not each.get('IdSolicitante',None) in solANPD: continue
                    rec = dict()
                    rec['IdSolicitante']    = each.get('IdSolicitante',None)
                    rec['TipoDemandante']   = each.get('TipoDemandante',None)
                    rec['DataNascimento']   = each.get('DataNascimento',None)
                    rec['Genero']           = each.get('Genero',None)
                    rec['Pais']             = each.get('Pais',None)
                    rec['UF']               = each.get('UF',None)
                    rec['Municipio_s']      = each.get('Municipio',None)
                    df = df.append(rec, ignore_index=True)
                try: df['UF'] = df['UF'].apply(lambda x: None if pd.isna(x) else x.replace('DISTRITO FEDERAL','DF') )
                except: pass
                solr = df
            with st.spinner('Wraping-up. Falta pouco!'):
                ped = ped[ped['OrgaoDestinatario'].str.contains('ANPD')]
                ped['IdSolicitante'] = ped['IdSolicitante'].apply(lambda x: 'ND' if x=='0' else x)
                ped.drop('OrgaoDestinatario',axis=1,inplace=True)
                ped.reset_index(drop=True, inplace=True)
                recl['IdSolicitante'] = recl['IdSolicitante'].apply(lambda x: 'ND' if x=='0' else x)
                recl = recl[recl['OrgaoDestinatario'].str.contains('ANPD')]
                recl.reset_index(drop=True, inplace=True)
                recl.drop('OrgaoDestinatario',axis=1,inplace=True)
                r1 = sol
                r1['Origem'] = 'Ped'
                r2 = solr
                r2['Origem'] = 'Rec'

                df = pd.DataFrame()
                df = df.append(r1, ignore_index=False)
                df = df.append(r2, ignore_index=False)
                df.sort_values(by=['IdSolicitante','Origem'], ascending=True, inplace = True)
                df.drop_duplicates(subset=['IdSolicitante'], keep='first', inplace=True)
                df.reset_index(drop=True, inplace=True)
                for c in df.columns:
                    if c.startswith('Unnamed'): df.drop(c, axis=1, inplace=True)
                df.rename({'UFs':'UF'               }, axis=1, inplace=True)
                df.rename({'Municipio_s':'Municipio'}, axis=1, inplace=True)
                for c in df.columns:
                    if not c == 'IdSolicitante':
                        df.rename({c:'s_'+c}, axis=1, inplace=True)
                df = df[['IdSolicitante','s_DataNascimento', 's_Genero',  
                         's_Pais', 's_UF', 's_Municipio', 's_TipoDemandante']]
                solF = df   
                     
                solANPD = list(set(list(recl['IdSolicitante'].unique()) + list(ped['IdSolicitante'].unique())))
                solANPD = ['ND' if x=='0' else x for x in solANPD]
                solF = solF[solF['IdSolicitante'].isin(solANPD)]
                solF.reset_index(drop=True, inplace=True)
                solF = solF.fillna('ND')
                for c in solF.columns:
                    #solF.rename({c:c.replace('s_','')}, axis=1, inplace=True)
                    solF[c] = solF[c].apply(lambda x: 'ND' if x=='' else x)
                from datetime import date
                def idade(born):
                    today = date.today()
                    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                solF['s_Idade'] = solF['s_DataNascimento'].apply(lambda x: 'ND' if x=='ND' else
                                                             idade(datetime.strptime(x,'%d/%m/%Y')))
                        
                ped  = ped.merge( solF, on='IdSolicitante', how='left')
                recl = recl.merge(solF, on='IdSolicitante', how='left')
                ped = ped.fillna('ND')
                recl = recl.fillna('ND')        


                ped['Data'] = ped['DataRegistro'].apply(lambda x: 'ND' if x=='ND' else
                                                             datetime.strptime(x,'%d/%m/%Y'))
                ped['Periodo']     = ped['Data'].apply(lambda x: str(x.year)+'-'+str(x.month).zfill(2) if x != 'ND' else 'ND')
                tmp = ped[ped.Data != 'ND']
                inicio = str(tmp['Data'].min())
                final  = str(tmp['Data'].max())
                print(inicio, final)

                recl['Periodo_tmp'] = recl['DataRegistro'].apply(lambda x: datetime.strptime(x,'%d/%m/%Y'))
                recl['Periodo']     = recl['Periodo_tmp'].apply(lambda x: str(x.year)+'-'+str(x.month).zfill(2))
                recl.drop('Periodo_tmp', axis=1, inplace=True)

                geo= pd.read_pickle('../ANDP.Denunciometro/Geo.pkl')
                def ajuste_cidade(x):
                    x = unidecode(str(x).lower().strip())
                    exc = '`- '
                    x = ''.join([c for c in x if not c in exc])
                    return(x)
                ped['CidadeU'] = ped['s_Municipio'].apply(lambda x: ajuste_cidade(x))  
                ped = ped.merge(geo,on='CidadeU', how='left')
                ped.rename({'UF_y':'UF_loc',
                           },axis=1,inplace=True)
                ped.drop('CidadeU', axis=1,inplace=True)
                ped['Cidade'] = ped['Cidade'].fillna('ND')
                ped['lat']    = ped['lat'].fillna(-34.017678)
                ped['lon']    = ped['lon'].fillna(-41.617380)
                with open('../ANDP.Denunciometro/00LastUpdate.txt', 'w', encoding='utf-8') as base:
                    base.write(f"""{running_date}\n{inicio}\n{final}""")
                ped.to_pickle('../ANDP.Denunciometro/00Ped.pkl')
                recl.to_pickle('../ANDP.Denunciometro/00Recl.pkl')
                ped.to_csv('00Ped.csv', index=False)
                recl.to_csv('00Recl.csv', index=False)
            ############################################## END OF UPDATE
        return(True)
    except:
        return(False)
        
last_update = (datetime.today() - datetime.strptime(last, '%d-%m-%Y %Hh%Mm')).days
if last_update > 0:
    if update():
        st.success('Dados atualizados!')
    else:
        st.error('Problemas baixando dados a partir de CGU.gov.br')


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






