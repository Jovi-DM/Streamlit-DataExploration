#   Imports
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(  # Start the visualization in wide mode
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
)

col1, col2, col3 = st.columns(3)  # Splitting display in 3 columns, to use a central columns centralize the logo
with col2:
    st.image(
        "https://i.imgur.com/fAJQjmz.png",
        width=450,
    )

st.title("Data Exploration")  # Putting title in page

c1, c2, c3 = st.columns([1, 6, 1])  # Splitting display in 3 columns, but the middle column have 6x more space than 1

with c2:
    uploaded_file = st.file_uploader(  # Button box to select your file csv, that will be imported
        "",
        key="1",
        help="To deactive 'wide mode', access ☰ > Settings > turn off 'wide mode'",
    )

    if uploaded_file is not None:  # Verify if the csv file was uploaded
        file_container = st.expander("Check what is in your .csv")
        shows = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        file_container.write(shows)

    else:  # Shows for the user where he can upload the file
        st.markdown("<h1 style='text-align: center; color: white;'> ↑ Upload csv file ↑ </h1>",
                    unsafe_allow_html=True)

        st.stop()

from st_aggrid import GridUpdateMode, DataReturnMode

gb = GridOptionsBuilder.from_dataframe(shows)
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()
gridOptions = gb.build()

st.success(
    f"""
        💡 Tip! Hold the shift, to select more than one row at once!
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

st.markdown("<h1 style='text-align: center; color: white;'> Selected rows in table showed below ↓ </h1>",
            unsafe_allow_html=True)

st.table(df)

st.markdown("<h1 style='text-align: center; color: white;'> To export filtered data </h1>",
            unsafe_allow_html=True)


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


csv = convert_df(df)  # Convert output for csv, that could be downloaded

c1, c2, c3 = st.columns([2, 1, 1.5])

with c2:
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='details.csv',
        mime='text/csv',
    )
