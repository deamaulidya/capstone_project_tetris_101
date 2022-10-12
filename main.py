from numpy import size
import streamlit as st
import lorem
from numerize import numerize
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px

#preprocess data
smr = pd.read_excel("/Users/ACER/Work/TETRIS/capstone_project/database/suicide.xlsx")
smr_dunia = pd.read_excel("/Users/ACER/Work/TETRIS/capstone_project/database/world_suicide.xlsx")
unemployment = pd.read_excel("/Users/ACER/Work/TETRIS/capstone_project/database/unemployment.xlsx")
gdp = pd.read_excel("/Users/ACER/Work/TETRIS/capstone_project/database/gdp.xlsx")
alcohol = pd.read_excel("/Users/ACER/Work/TETRIS/capstone_project/database/alcohol.xlsx")
mental = pd.read_csv("/Users/ACER/Work/TETRIS/capstone_project/database/mental.csv")
mental.columns=['country','code','year','mental']
mentall=mental[mental['year'] == 2019] 
smr_new=smr[['Country Name','2019']]
smr_new.columns=['country','smr']
unem=unemployment[['Country Name','2019']]
unem.columns=['country','unemployment']
gdp_new=gdp[['Country Name','2019']]
gdp_new.columns=['country','gdp']
alco=alcohol[['Country Name','2018']]
alco.columns=['country','alcohol']
result = pd.merge(smr_new, unem, on="country")
result = pd.merge(result, gdp_new, on="country")
result = pd.merge(result, alco, on="country")
res = pd.merge(result,mentall,on='country',how='left')
res=res.dropna()

df = pd.DataFrame(res,columns=['smr','unemployment','gdp','alcohol','mental'])




st.set_page_config(layout="wide")
st.title("Apakah Tingkat Kematian bunuh diri dipengaruhi oleh banyaknya pengangguran?")
st.subheader("Tingkat Kematian Bunuh Diri")
st.write("Kematian karena bunuh diri merupakan masalah yang sangat rumit. Setiap kasus bunuh diri adalah tragedi. Organisasi Kesehatan Dunia (WHO) dan studi Global Burden of Disease memperkirakan bahwa hampir 800.000 orang meninggal karena bunuh diri setiap tahun artinya ada satu orang yang bunuh diri setiap 40 detik. Menurut studi tersebut pada tahun 2019 bunuh diri berada di peringkat ke-15 dari 33 penyebab kematian lainnya. Namun jika dibandingkat dengan tahun-tahun sebelumnya, nilai tingkat kematian bunuh diri terus mengecil.")



fig1 = go.Figure(data=go.Choropleth(
    locations = smr['Country Code'],
    z = smr['2019'],
    text = smr['Country Name'],
    colorscale = 'Greens',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'SMR',
))
fig1.update_layout(
    width=1000,
    height=620,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    title={
        'text': '<b>Tingkat Kematian Bunuh Diri Tiap Negara</b>',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    title_font_color='#525252',
    title_font_size=26,
    font=dict(
        family='Heebo', 
        size=18, 
        color='#525252'
    ),
    annotations = [dict(
        x=0.5,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://data.worldbank.org/indicator/SH.STA.SUIC.P5">\
            The World Bank Data / Suicide Mortality Rate (per 100000 population)</a>',
        showarrow = False
    )]
)
label_fig2=['Dunia','Indonesia','Low Income','Lower Middle Income','Middle Income','Upper Middle Income','High Income']
fig2=px.line(smr_dunia,x='year',y=smr_dunia.columns[1:8],labels={
                     "year": "Tahun",
                     "value": "Suicide Mortality Rate",
                     "variable":"Negara"
                 },
                title="Tingkat Kematian Bunuh Diri per Tahun")
def custom_legend_name(new_names):
    for i, new_name in enumerate(new_names):
        fig2.data[i].name = new_name
custom_legend_name(label_fig2)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1,use_container_width=True)

with col2:
    st.plotly_chart(fig2,use_container_width=True)


st.subheader("Beberapa faktor pengaruh tingkat bunuh diri")
c1,c2=st.columns(2)
with c1:
    var = st.selectbox(label = "Pilih data", options = ('Tingkat Pengangguran','GDP per Kapita','Jumlah Konsumsi Alkohol per Kapita','Persentase Populasi dengan Gangguan Mental dan Penyalahgunaan Zat'))
    v={'Tingkat Pengangguran':'unemployment','GDP per Kapita':'gdp','Jumlah Konsumsi Alkohol per Kapita':'alcohol','Persentase Populasi dengan Gangguan Mental dan Penyalahgunaan Zat':'mental'}
    fig3 = px.bar(res.dropna().sort_values(by=v[var],ascending=False), x='country', y=v[var],labels={v[var]:var})
    st.plotly_chart(fig3,use_container_width=True)
with c2:
    st.write(lorem.paragraph())



st.subheader("Korelasi dengan Tingkat Kematian Bunuh Diri")

colo1,colo2,colo3=st.columns(3)
with colo1:
    st.write(lorem.paragraph())
with colo2:
    var2 = st.selectbox(label = "Pilih data pembanding", options = ('Tingkat Pengangguran','GDP per Kapita','Jumlah Konsumsi Alkohol per Kapita','Persentase Populasi dengan Gangguan Mental dan Penyalahgunaan Zat'))
    fig5 = px.scatter(res.dropna(), x='smr', y=v[var2],labels={v[var2]:var2,'smr':'Tingkat Kematian Bunuh Diri'},color='smr')
    st.plotly_chart(fig5,use_container_width=True)

with colo3:
    corrMatrix = df.corr()
    fig4=plt.figure()
    fig4.set_figwidth(5)
    fig4.set_figheight(3)
    sns.heatmap(corrMatrix, annot=True)
    st.pyplot(fig4)

st.subheader("Kesimpulan")
st.write(lorem.paragraph())

