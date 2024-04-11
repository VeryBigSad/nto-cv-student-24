import base64
import io

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from PIL import Image

import main


def decode_img(image_bytes):
    return Image.open(io.BytesIO(base64.decodebytes(bytes(image_bytes, "utf-8"))))


st.markdown('# Предсказание достопримечательности по текстовому запросу')
prompt = st.text_input('Введите поисковый запрос: ')
if prompt:
    data = requests.post("http://158.160.138.228:8000/api/v1/classify-text", json={"text": prompt},
                         params={"city": open('city', 'r').read()}).json()
    data = pd.DataFrame.from_dict(data)
    data['longitude'] = data['coordinates'].apply(lambda x: x['longitude'])
    data['latitude'] = data['coordinates'].apply(lambda x: x['latitude'])
    data['images'] = data['xid'].apply(lambda xid: f"https://storage.yandexcloud.net/misis-progrev-gradientov/{xid}.jpg")

    data.drop('coordinates', axis=1, inplace=True)

    cats = data.groupby(by='category')['probability'].sum()
    cats = pd.DataFrame(cats).reset_index()
    cats.columns = ['category', 'probability']
    fig = px.pie(cats, names='category', values='probability')
    st.plotly_chart(fig)

    st.write('Возможно Вы искали:')
    df_for_table = data[['xid', 'images', 'name', 'probability']]
    df_for_table.insert(0, "Select", False)
    table = st.data_editor(
        df_for_table,
        column_config={
            "name": st.column_config.SelectboxColumn(
                "Предложение",
                width="medium",
                required=True,
                options=data['name'].unique()
            ),
            "images": st.column_config.ImageColumn(
                "Фотография"
            ),
            "probability": st.column_config.ProgressColumn(
                "Вероятности",
                format="%.3f",
                min_value=0,
                max_value=1,
            ),
            "Select": st.column_config.CheckboxColumn(required=True)
        },
        hide_index=True,
    )

    fig = px.scatter_mapbox(data,
                            lat='latitude',
                            lon='longitude',
                            size='probability',
                            zoom=10,
                            hover_name='name',
                            color='category')
    fig.update_layout(mapbox_style="open-street-map", height=800)
    st.plotly_chart(fig, use_container_width=True, height=800)

    st.write(main.PLACES_TO_VISIT)
    main.PLACES_TO_VISIT.update(set(table[table['Select'] == True]['xid']))
