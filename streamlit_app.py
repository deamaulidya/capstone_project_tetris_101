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
smr = pd.read_excel("./database/suicide.xlsx")
smr_dunia = pd.read_excel("./database/world_suicide.xlsx")
unemployment = pd.read_excel("./database/unemployment.xlsx")
gdp = pd.read_excel("./database/gdp.xlsx")
alcohol = pd.read_excel("./database/alcohol1.xlsx",usecols=[1,2,3])
mental = pd.read_csv("./database/mental.csv")
mental.columns=['country','code','year','mental']
mentall=mental[mental['year'] == 2019] 
smr_new=smr[['Country Code','2019']]
smr_new.columns=['code','smr']
unem=unemployment[['Country Code','2019']]
unem.columns=['code','unemployment']
gdp_new=gdp[['Country Code','2019']]
gdp_new.columns=['code','gdp']
alco=alcohol[['code','alcohol']]
result = pd.merge(smr_new, unem, on="code")
result = pd.merge(result, gdp_new, on="code")
result = pd.merge(result, alco, on="code")
res = pd.merge(result,mentall,on='code',how='left')
res=res.dropna()

df = pd.DataFrame(res,columns=['smr','unemployment','gdp','alcohol','mental'])




st.set_page_config(page_title="Korelasi Tingkat Kematian Bunuh Diri",layout="centered")
st.title("Apakah Tingkat Kematian Bunuh Diri Dipengaruhi oleh Tingkat Pengangguran?")
st.write("Oleh: Dea Maulidya")
st.subheader("Tingkat Kematian Bunuh Diri")

st.markdown('<div style="text-align: justify;">Kematian karena bunuh diri merupakan masalah yang sangat rumit. Setiap kasus bunuh diri adalah tragedi. Organisasi Kesehatan Dunia (WHO) dan studi Global Burden of Disease memperkirakan bahwa setiap tahun hampir <b>800.000 orang meninggal karena bunuh diri</b> artinya ada satu orang yang bunuh diri setiap 40 detik. Menurut studi tersebut pada tahun 2019 bunuh diri berada di <b>peringkat ke-15 dari 33</b> penyebab kematian lainnya. Namun jika dibandingkan dengan tahun-tahun sebelumnya, nilai tingkat kematian bunuh diri terus menurun. <b>Tingkat Kematian Bunuh Diri atau Suicide Mortality Rate (SMR)</b> menggambarkan jumlah kematian bunuh diri tiap 100.000 populasi penduduk di suatu negara pada tahun tertentu.</div>', unsafe_allow_html=True)




fig1 = go.Figure(data=go.Choropleth(
    locations = smr['Country Code'],
    z = smr['2019'],
    text = smr['Country Name'],
    colorscale = 'OrRd',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'SMR'
))
fig1.update_layout(
    autosize=True,
    margin_autoexpand=True,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    title={
        'text': '<b>Suicide Mortality Rate Tiap Negara Tahun 2019</b>',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    annotations = [dict(
        x=0.5,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://data.worldbank.org/indicator/SH.STA.SUIC.P5">\
            The World Bank Data / Suicide Mortality Rate</a>',
        showarrow = False
    )]
    
)

label_smr=['Dunia','Indonesia','Low','Lower Middle','Upper Middle','High']
smr_wi=[0,1,2]
smr_income=[0,3,4,5,6,7]
figwi=px.line(smr_dunia,x='year',y=smr_dunia.columns[1:3],labels={
                     "year": "Tahun",
                     "value": "Suicide Mortality Rate",
                     "variable":"Negara"
                 })
figwi.update_layout(
    title={
        'text': "<b>SMR Dunia vs Indonesia</b>",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
figin=px.line(smr_dunia,x='year',y=smr_dunia.columns[3:],labels={
                     "year": "Tahun",
                     "value": "Suicide Mortality Rate",
                     "variable":"Negara"
                 },
                 color_discrete_map={
                 "high": "blue",
                 "low":"red",
                 "uppermiddle":"green",
                 "lowermiddle":"orange"
             })
figin.update_layout(
    title={
        'text': "<b>SMR Berdasarkan Income Level</b>",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
def custom_legend_name(fig,new_names):
    for i, new_name in enumerate(new_names):
        fig.data[i].name = new_name
custom_legend_name(figwi,label_smr[0:2])
custom_legend_name(figin,label_smr[2:])

st.plotly_chart(fig1,use_container_width=True)
#st.markdown('<div style="text-align: justify;">Nilai Tingkat Kematian Bunuh Diri menggambarkan jumlah kematian bunuh diri per 100.000 populasi penduduk suatu negara di tahun tertentu.</div>', unsafe_allow_html=True)
col1,col2=st.columns(2)
with col1:
    st.plotly_chart(figwi,use_container_width=True)
    st.markdown('<div style="text-align: justify;">Tingkat kematian bunuh diri Indonesia <b>sangatlah rendah</b> jika dibandingkan dengan Dunia. Dari tahun 2000 hingga tahun 2014 nilai tersebut selalu mengalami penurunan, namun mulai dari tahun 2014 hingga 2019 tingkat kematian bunuh diri di Indonesia <b>tetap konstan di angka 2.4</b>. Artinya, ada kurang lebih 2 dari 100.000 orang yang meninggal karena bunuh diri pada tahun 2019. </div>', unsafe_allow_html=True)

with col2:
    st.plotly_chart(figin,use_container_width=True)
    st.markdown('<div style="text-align: justify;">Terlihat bahwa negara yang termasuk kategori low income rata-rata memiliki tingkat kematian bunuh diri yang rendah. Sebaliknya, negara yang termasuk high income rata-rata memiliki tingkat kematian yang juga tinggi. Dari grafik dapat diambil kesimpulan bahwa nilai <b>tingkat kematian bunuh diri sesuai (berbanding lurus) dengan kategori level pendapatan suatu negara</b>.</div>', unsafe_allow_html=True)

st.write("")
st.subheader("Beberapa Faktor Pengaruh Tingkat Bunuh Diri")

st.markdown('<div style="text-align: justify;">Sebagian besar kasus percobaan bunuh diri terjadi secara impulsif atau mendadak yang berarti hal tersebut tidak yang direncanakan secara menyeluruh. Upaya tersebut dapat terjadi karena suatu faktor maupun kombinasi dari beberapa faktor. Beberapa alasan yang mendorong orang untuk melakukan percobaan bunuh diri seperti depresi, penyalahgunaan NAPZA, masalah ekonomi, takut kehilangan dan lain sebagainya. Berikut merupakan nilai dari beberapa faktor pendorong bunuh diri di dunia.</div>', unsafe_allow_html=True)

var = st.selectbox(label = "Pilih data", options = ('Tingkat Pengangguran','GDP per Kapita','Jumlah Konsumsi Alkohol per Kapita','Persentase Populasi Penduduk dengan Gangguan Mental'))
v={'Tingkat Pengangguran':'unemployment','GDP per Kapita':'gdp','Jumlah Konsumsi Alkohol per Kapita':'alcohol','Persentase Populasi Penduduk dengan Gangguan Mental':'mental'}
vcolor={'Tingkat Pengangguran':'Reds','GDP per Kapita':'Greens','Jumlah Konsumsi Alkohol per Kapita':'YlOrRd','Persentase Populasi Penduduk dengan Gangguan Mental':'Oranges'}
v2={'Tingkat Pengangguran':'(% dari Jumlah Angkatan Kerja)','GDP per Kapita':'(US$)','Jumlah Konsumsi Alkohol per Kapita':'(Liter)','Persentase Populasi Penduduk dengan Gangguan Mental':''}

figb = go.Figure(data=go.Choropleth(
    locations = res['code'],
    z = res[v[var]],
    text = res['country'],
    colorscale = vcolor[var],
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5
))
figb.update_layout(
    autosize=True,
    margin_autoexpand=True,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    title={
        'text': f"<b>{var} {v2[var]} Tiap Negara Tahun 2019</b>",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    }
    
)
st.plotly_chart(figb,use_container_width=True)


st.subheader("Korelasi dengan Tingkat Kematian Bunuh Diri")


var2 = st.selectbox(label = "Pilih data pembanding", options = ('Tingkat Pengangguran','GDP per Kapita','Jumlah Konsumsi Alkohol per Kapita','Persentase Populasi Penduduk dengan Gangguan Mental'))
fig5 = px.scatter(res.dropna(), y='smr', x=v[var2],labels={v[var2]:var2,'smr':'Suicide Mortality Rate','country':'Negara'},hover_name='country',trendline='ols',color_discrete_sequence=["red"])
# fig5.update_layout(plot_bgcolor='#FFFFFF')
st.plotly_chart(fig5,use_container_width=True)
df1=df
df1.columns=['SMR','Unemployment','GDP','Alcohol','Mental']
colo1,colo2=st.columns(2)
with colo1:
    st.markdown('<div style="text-align: justify;">Hubungan antara tingkat kematian bunuh diri dengan beberapa faktor penyebab bunuh diri dibandingkan dengan menghitung korelasi antara keduanya. Faktor yang dijadikan pembanding antara lain Tingkat Pengangguran, GDP per Kapita, Jumlah Konsumsi Alkohol per Kapita, Persentase Populasi dengan Gangguan Mental. Apabila nilai korelasi yang diperoleh mendekati 1 atau -1 maka dapat dikatakan hubungan antara keduanya sangatlah kuat.</div>', unsafe_allow_html=True)
with colo2:
    corrMatrix = df1.corr()
    fig4=plt.figure()
    fig4.suptitle('Matriks Korelasi', fontsize=16)
    fig4.set_figwidth(5)
    fig4.set_figheight(3)
    sns.heatmap(corrMatrix,cmap="RdBu",center=0,annot=True)
    
    st.pyplot(fig4)

st.subheader("Kesimpulan")
st.markdown('<div style="text-align: justify;">Dari hasil korelasi diperoleh nilai korelasi tingkat kematian bunuh diri dengan tingkat pengangguran disuatu negara adalah <b>0.2</b> yang artinya <b>ada hubungan yang berbanding lurus namun tidak terlalu kuat</b> antara keduanya. Maksud dari hubungan yang berbanding lurus adalah apabila ada penurunan jumlah tingkat pengangguran maka tingkat kematian bunuh diri juga akan menurun begitu juga berlaku sebaliknya. Namun dari gambar korelasi terlihat bahwa ada faktor yang memiliki hubungan lebih kuat dengan tingkat kematian bunuh diri, yaitu jumlah konsumsi alkohol perkapita di suatu negara dengan nilai korelasi sebesar 0.33.</div>', unsafe_allow_html=True)
st.markdown('')
st.markdown('<div style="text-align: left;"> Sumber Data: <a href="https://data.worldbank.org/"> The World Bank</a>, <a href="https://www.who.int/">WHO</a>, dan <a href="https://ourworldindata.org/">Our World in Data</a></div>', unsafe_allow_html=True)
