import streamlit as st
import pandas as pd

###################################
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

col1, col2, col3 = st.columns(3)
with col2:
    st.image(
        "https://i.imgur.com/fAJQjmz.png",
        width=450,
    )

st.title("Data Exploration")

c29, c30, c31 = st.columns([1, 6, 1])

with c30:

    uploaded_file = st.file_uploader(
        "",
        key="1",
        help="Para ativar o modo 'wide', acesse o menu lateral > Settings > turn on 'wide mode'",
    )

    if uploaded_file is not None:
        file_container = st.expander("Verifique o que foi enviado do seu arquivo .csv")
        shows = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        file_container.write(shows)

    else:
        st.markdown("<h1 style='text-align: center; color: white;'> ↑ Realize o upload do seu arquivo .csv ↑ </h1>", unsafe_allow_html=True)

        st.stop()

from st_aggrid import GridUpdateMode, DataReturnMode

gb = GridOptionsBuilder.from_dataframe(shows)
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()
gridOptions = gb.build()

st.success(
    f"""
        💡 Dica! Segure o Shift, enquanto seleciona as linhas para selecionar várias por vez!
        """
)

response = AgGrid(
    shows,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=False,
)

df = pd.DataFrame(response["selected_rows"])

st.markdown("<h1 style='text-align: center; color: white;'> Linhas selecionadas na tabela, apareceram abaixo ↓ </h1>", unsafe_allow_html=True)

st.table(df)

st.markdown("<h1 style='text-align: center; color: white;'> Para exportar os dados filtrados </h1>", unsafe_allow_html=True)

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

c32, c33, c34 = st.columns([2, 1, 1.5])

with c33:
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='details.csv',
        mime='text/csv',
    )