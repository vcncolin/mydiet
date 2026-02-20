import streamlit as st
import pandas as pd
import plotly.express as px

# Load data from CIQUAL table
df = pd.read_csv('data_ciqual_filtered.csv')

# Add a title
st.title('Application Diététique')

# Button to add a new entry in the food consumed table : 
# from https://discuss.streamlit.io/t/button-to-add-new-row-of-inputs/33245/2

#On créé un tableau vide avec les colonnes correspondant aux quantités que l'on veut mesurer
if 'data' not in st.session_state:
    data = pd.DataFrame({'Aliment':[],'Quantité (g)':[],'Énergie (kcal)':[],'Protéines (g)':[],'Glucides (g)':[], 'Lipides (g)':[]})
    st.session_state.data = data

data = st.session_state.data

#Fonction pour créer une nouvelle ligne :
def add_dfForm():
    row = pd.DataFrame({'Aliment':[st.session_state.input_Food],
            'Quantité (g)':[st.session_state.input_Qty],
            'Énergie (kcal)':[df[df['Aliment'] == st.session_state.input_Food]['EnergieUE (kcal/100g)'].values[0]*st.session_state.input_Qty],
            'Protéines (g)':[df[df['Aliment'] == st.session_state.input_Food]['Protéines (g/100g)'].values[0]*st.session_state.input_Qty],
            'Glucides (g)':[df[df['Aliment'] == st.session_state.input_Food]['Glucides (g/100g)'].values[0]*st.session_state.input_Qty],
            'Lipides (g)':[df[df['Aliment'] == st.session_state.input_Food]['Lipides (g/100g)'].values[0]*st.session_state.input_Qty],
            })
    st.session_state.data = pd.concat([st.session_state.data, row])

#Fonction pour reset le session state (et don vider le tableau)
def reset_data():
    st.session_state.data = pd.DataFrame({'Aliment':[],'Quantité (g)':[],'Énergie (kcal)':[],'Protéines (g)':[],'Glucides (g)':[], 'Lipides (g)':[]})


col1, col2 = st.columns([3, 1])
col1.subheader('Ajouter un aliment')
with col1:
    dfForm = st.form(key='dfForm')
    with dfForm:
        dfColumns = st.columns(3, vertical_alignment='center', )
        with dfColumns[0]:
            st.selectbox('Aliment', options = df['Aliment'].unique(), key='input_Food')
        with dfColumns[1]:
            st.slider('Quantité (g)', 0.0, 500.0, 50.0, 25.0, key='input_Qty')
        with dfColumns[2]:
            st.form_submit_button('Ajouter', on_click=add_dfForm, use_container_width=True)
col2.subheader('Remise à 0')
with col2:
    st.button('Reset', type="primary", on_click=reset_data)

st.dataframe(data, hide_index=True)