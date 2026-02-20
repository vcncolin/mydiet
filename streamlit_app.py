import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Load data from CIQUAL table
df = pd.read_csv('data_ciqual_filtered.csv')

# Add a title
st.title('Application Diététique')

# Button to add a new entry in the food consumed table : 
# from https://discuss.streamlit.io/t/button-to-add-new-row-of-inputs/33245/2

#On créé un tableau vide avec les colonnes correspondant aux quantités que l'on veut mesurer
if 'data' not in st.session_state:
    data = pd.DataFrame({'Jour':[],'Repas':[],'Aliment':[],'Quantité (g)':[],'Énergie (kcal)':[],'Protéines (g)':[],'Glucides (g)':[], 'Lipides (g)':[]})
    st.session_state.data = data

data = st.session_state.data

#Fonction pour créer une nouvelle ligne :
def add_dfForm():
    row = pd.DataFrame({
            'Jour':[st.session_state.input_Jour],
            'Repas':[st.session_state.input_Repas],
            'Aliment':[st.session_state.input_Food],
            'Quantité (g)':[st.session_state.input_Qty],
            'Énergie (kcal)':[df[df['Aliment'] == st.session_state.input_Food]['EnergieUE (kcal/100g)'].values[0]*st.session_state.input_Qty*0.01],
            'Protéines (g)':[df[df['Aliment'] == st.session_state.input_Food]['Protéines (g/100g)'].values[0]*st.session_state.input_Qty*0.01],
            'Glucides (g)':[df[df['Aliment'] == st.session_state.input_Food]['Glucides (g/100g)'].values[0]*st.session_state.input_Qty*0.01],
            'Lipides (g)':[df[df['Aliment'] == st.session_state.input_Food]['Lipides (g/100g)'].values[0]*st.session_state.input_Qty*0.01],
            })
    st.session_state.data = pd.concat([st.session_state.data, row])

#Fonction pour reset le session state (et don vider le tableau)
def reset_data():
    st.session_state.data = pd.DataFrame({'Jour':[],'Repas':[],'Aliment':[],'Quantité (g)':[],'Énergie (kcal)':[],'Protéines (g)':[],'Glucides (g)':[], 'Lipides (g)':[]})


col1, col2 = st.columns([4, 1])
col1.subheader('Ajouter un aliment')
with col1:
    dfForm = st.form(key='dfForm')
    with dfForm:
        row0 = st.columns([2,2,1], vertical_alignment='bottom')
        row1 = st.columns([3,1], vertical_alignment='center')
        with row0[0]:
            st.date_input('Jour', value=datetime.date.today(), key='input_Jour')
        with row0[1]:
            st.selectbox('Repas', options = ['Petit-déjeuner', 'Collation', 'Déjeuner', 'Goûter', 'Dîner'], key='input_Repas')
        with row0[2]:
            st.form_submit_button('Ajouter', on_click=add_dfForm, use_container_width=True)
        with row1[0]:
            st.selectbox('Aliment', options = df['Aliment'].unique(), key='input_Food')
        with row1[1]:
            st.slider('Quantité (g)', 0.0, 500.0, 50.0, 25.0, key='input_Qty')
        
col2.subheader('Remise à 0')
with col2:
    st.button('Reset', type="primary", on_click=reset_data)
    st.number_input('AJR (kcal)', value=2000, step=250, key='input_AJR')

col3, col4 = st.columns([1, 1])

if st.session_state.data.empty:
    st.warning('Aucun aliment ajouté pour le moment. Veuillez remplir le formulaire pour ajouter des aliments consommés.')
else:
    #Graphique camembert répartition macronutriments

    labels = ['Protéines', 'Glucides', 'Lipides']
    values = [st.session_state.data['Protéines (g)'].sum(), st.session_state.data['Glucides (g)'].sum(), st.session_state.data['Lipides (g)'].sum()]

    pie = go.Figure(data=[go.Pie(labels=labels, values=values)])
    col3.subheader('Répartition des macronutriments')
    col3.plotly_chart(pie)     

    #Graphique histogramme pour énergie totale journée

    bar = px.bar(x=st.session_state.data['Jour'], y=st.session_state.data['Énergie (kcal)'], color=st.session_state.data['Repas'], labels={'x':'','y':'Énergie (kcal)','color':' '})
    bar.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=st.session_state.data['Jour'].unique()
        ))
    bar.add_hline(y=st.session_state.input_AJR, line_dash="dash", line_color="red")
    col4.subheader('Énergie totale par repas')
    col4.plotly_chart(bar)

    st.dataframe(data, hide_index=True)
