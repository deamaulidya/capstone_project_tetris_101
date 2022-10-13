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
alcohol = pd.read_excel("./database/alcohol.xlsx")
mental = pd.read_csv("./database/mental.csv")
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




st.set_page_config(page_title="Korelasi Tingkat Kematian Bunuh Diri",layout="centered")
st.title("Apakah Tingkat Kematian bunuh diri dipengaruhi oleh banyaknya pengangguran?")
st.write("Penulis: Dea Maulidya")
st.subheader("Tingkat Kematian Bunuh Diri")

st.markdown('<div style="text-align: justify;">Kematian karena bunuh diri merupakan masalah yang sangat rumit. Setiap kasus bunuh diri adalah tragedi. Organisasi Kesehatan Dunia (WHO) dan studi Global Burden of Disease memperkirakan bahwa hampir 800.000 orang meninggal karena bunuh diri setiap tahun artinya ada satu orang yang bunuh diri setiap 40 detik. Menurut studi tersebut pada tahun 2019 bunuh diri berada di peringkat ke-15 dari 33 penyebab kematian lainnya. Namun jika dibandingkan dengan tahun-tahun sebelumnya, nilai tingkat kematian bunuh diri terus menurun.</div>', unsafe_allow_html=True)




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
    margin_autoexpand=False,
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
            The World Bank Data / Suicide Mortality Rate</a>',
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
st.plotly_chart(fig1,use_container_width=True)

st.plotly_chart(fig2,use_container_width=True)


st.subheader("Beberapa Faktor Pengaruh Tingkat Bunuh Diri")

st.markdown('<div style="text-align: justify;">Sebagian besar kasus percobaan bunuh diri terjadi secara impulsif atau mendadak yang berarti hal tersebut tidak yang direncanakan secara menyeluruh. Upaya tersebut dapat terjadi karena suatu faktor maupun kombinasi dari beberapa faktor. Beberapa alasan yang mendorong orang untuk melakukan percobaan bunuh diri seperti depresi, penyalahgunaan NAPZA, masalah ekonomi, takut kehilangan dan lain sebagainya. Berikut merupakan nilai dari beberapa faktor pendorong bunuh diri di dunia.</div>', unsafe_allow_html=True)
    
# with col2:
#     var = st.selectbox(label = "Pilih data", options = ('Tingkat Pengangguran','GDP per Kapita','Jumlah Konsumsi Alkohol per Kapita','Persentase Populasi dengan Gangguan Mental dan Penyalahgunaan NAPZA'))
#     v={'Tingkat Pengangguran':'unemployment','GDP per Kapita':'gdp','Jumlah Konsumsi Alkohol per Kapita':'alcohol','Persentase Populasi dengan Gangguan Mental dan Penyalahgunaan NAPZA':'mental'}
#     fig3 = px.bar(res.dropna().sort_values(by=v[var],ascending=False), x='country', y=v[var],labels={v[var]:var,'country':'Negara'},color=v[var], color_continuous_scale=px.colors.sequential.Bluered)
#     fig3.update(layout_showlegend=False,layout_coloraxis_showscale=False)
#     st.plotly_chart(fig3,use_container_width=True)
var = st.selectbox(label = "Pilih data", options = ('Tingkat Pengangguran','GDP per Kapita','Jumlah Konsumsi Alkohol per Kapita','Persentase Populasi dengan Gangguan Mental dan Penyalahgunaan NAPZA'))
v={'Tingkat Pengangguran':'unemployment','GDP per Kapita':'gdp','Jumlah Konsumsi Alkohol per Kapita':'alcohol','Persentase Populasi dengan Gangguan Mental dan Penyalahgunaan NAPZA':'mental'}
figb = go.Figure(data=go.Choropleth(
    locations = res['code'],
    z = res[v[var]],
    text = res['country'],
    colorscale = 'Greens',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5
))
figb.update(layout_showlegend=False,layout_coloraxis_showscale=False)
figb.update_layout(
    width=1000,
    height=620,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    title={
        'text': var,
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
    )
)
st.plotly_chart(figb,use_container_width=True)


st.subheader("Korelasi dengan Tingkat Kematian Bunuh Diri")


var2 = st.selectbox(label = "Pilih data pembanding", options = ('Tingkat Pengangguran','GDP per Kapita','Jumlah Konsumsi Alkohol per Kapita','Persentase Populasi dengan Gangguan Mental dan Penyalahgunaan NAPZA'))
fig5 = px.scatter(res.dropna(), y='smr', x=v[var2],labels={v[var2]:var2,'smr':'Tingkat Kematian Bunuh Diri'},trendline='ols')
# fig5.update_layout(plot_bgcolor='#FFFFFF')
st.plotly_chart(fig5,use_container_width=True)
colo1,colo2=st.columns(2)
with colo1:
    st.markdown('<div style="text-align: justify;">Hubungan antara tingkat kematian bunuh diri dengan beberapa faktor penyebab bunuh diri dibandingkan dengan menghitung korelasi antara keduanya. Faktor yang dijadikan pembanding antara lain Tingkat Pengangguran, GDP per Kapita, Jumlah Konsumsi Alkohol per Kapita, Persentase Populasi dengan Gangguan Mental dan Penyalahgunaan NAPZA. Apabila nilai korelasi yang diperoleh mendekati 1 atau -1 maka dapat dikatakan hubungan antara keduanya sangatlah kuat.</div>', unsafe_allow_html=True)
with colo2:
    corrMatrix = df.corr()
    fig4=plt.figure()
    fig4.set_figwidth(5)
    fig4.set_figheight(3)
    sns.heatmap(corrMatrix, annot=True)
    st.pyplot(fig4,)

st.subheader("Kesimpulan")
st.markdown('<div style="text-align: justify;">Dari hasil korelasi diperoleh nilai korelasi tingkat kematian bunuh diri dengan tingkat pengangguran disuatu negara adalah 0.24 yang artinya ada hubungan yang berbanding lurus namun tidak terlalu kuat antara keduanya. Maksud dari hubungan yang berbanding lurus adalah apabila ada penurunan jumlah tingkat pengangguran maka tingkat kematian bunuh diri juga akan menurun begitu juga berlaku sebaliknya. Namun dari gambar korelasi terlihat bahwa ada faktor yang memiliki hubungan lebih kuat dengan tingkat kematian bunuh diri, yaitu jumlah konsumsi alkohol perkapita di suatu negara dengan nilai korelasi sebesar 0.31</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: left;"> Sumber Data: https://data.worldbank.org/ dan https://ourworldindata.org/mental-health</div>', unsafe_allow_html=True)
