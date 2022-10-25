#   Imports
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_metrics import metric, metric_row

st.set_page_config(  # Start the visualization in wide mode
    layout="wide",  # It can be "centered" or "wide". In the future also "dashboard", etc.
)

col1, col2, col3 = st.columns(3)  # Splitting display in 3 columns, to use a central columns centralize the logo
with col2:
    st.image(
        "https://i.imgur.com/fAJQjmz.png",
        width=450,
    )

st.title("Data Exploration")  # Putting title in page

c1, c2, c3 = st.columns([1, 6, 1])  # Splitting display in 3 columns, but The middle column has 6x more space than 1

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

    else:  # Shows the user where he can upload the file
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
        💡 Tip! Hold shift, to select more than one row at once!
        """
)

df = pd.DataFrame(shows)

### KPI Boards ###
num_stores = df.source.unique()

max = df.max()  # Max value
indice_max = df.extracted_price.idxmax()  # ID_row that has Max value
min = df.min()  # Min value
indice_min = df.extracted_price.idxmin()  # ID_row that has Min value

c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 4, 1, 5, 1, 5, 1])
with c2:
    wch_colour_box = (0, 102, 185)
    wch_colour_font = (0, 0, 0)
    fontsize = 48
    iconname = "fa fa-building"
    sline = "Quantity Stores "
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    i = len(num_stores)

    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                  {wch_colour_box[1]}, 
                                                  {wch_colour_box[2]}); 
                            color: rgb({wch_colour_font[0]}, 
                                       {wch_colour_font[1]}, 
                                       {wch_colour_font[2]}); 
                            font-size: {fontsize}px; 
                            border-radius: 20px; 
                            padding-left: 30px; 
                            padding-top: 30px; 
                            padding-bottom: 30px; 
                            line-height:50px;'>
                            <i class='{iconname} fa-xs'></i> {i}
                            </style><BR><span style='font-size: 28px; 
                            margin-top: 0;'>{sline} </style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)
with c4:
    wch_colour_box = (0, 102, 0)
    wch_colour_font = (0, 0, 0)
    fontsize = 48
    iconname = "fa fa-arrow-down"
    sline = "Best Price"
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    i = df.iloc[indice_min, 4]

    htmlstr2 = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                  {wch_colour_box[1]}, 
                                                  {wch_colour_box[2]}); 
                            color: rgb({wch_colour_font[0]}, 
                                       {wch_colour_font[1]}, 
                                       {wch_colour_font[2]}); 
                            font-size: {fontsize}px; 
                            border-radius: 20px; 
                            padding-left: 30px; 
                            padding-top: 30px; 
                            padding-bottom: 30px; 
                            line-height:50px;'>
                            <i class='{iconname} fa-xs'></i> {i}
                            </style><BR><span style='font-size: 32px; 
                            margin-top: 0;'>{sline}
                            - {df.iloc[indice_min, 3]}</style></span></p>"""
    st.markdown(lnk + htmlstr2, unsafe_allow_html=True)
with c6:
    wch_colour_box = (153, 0, 0)
    wch_colour_font = (0, 0, 0)
    fontsize = 48
    iconname = "fa fa-arrow-up"
    sline = "Higher Price"
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    i = df.iloc[indice_max, 4]

    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                  {wch_colour_box[1]}, 
                                                  {wch_colour_box[2]}); 
                            color: rgb({wch_colour_font[0]}, 
                                       {wch_colour_font[1]}, 
                                       {wch_colour_font[2]}); 
                            font-size: {fontsize}px; 
                            border-radius: 20px; 
                            padding-left: 30px; 
                            padding-top: 30px; 
                            padding-bottom: 30px; 
                            line-height:50px;'>
                            <i class='{iconname} fa-xs'></i> {i}
                            </style><BR><span style='font-size: 32px; 
                            margin-top: 0;'>{sline} 
                            - {df.iloc[indice_max, 3]}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)

response = AgGrid(
    shows,
    gridOptions=gridOptions,
    theme='material',
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=False,
)

df = pd.DataFrame(response["selected_rows"])

st.info(
    'An error may be shown, if you select columns with Rating = "NaN" and others that have values integers to csv download!',
    icon="ℹ️")
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
