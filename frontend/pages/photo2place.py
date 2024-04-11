from io import BytesIO

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from PIL import Image

import main


# Placeholder for your model (Replace this with your actual model)
def predict(bytes):
    # Example dictionary for prediction probabilities
    predictions = requests.post("http://158.160.138.228:8000/api/v1/classify-image", files={"image": bytes},
                                params={"city": open('city', 'r').read()}).json()
    predictions = pd.DataFrame(predictions['predicts'])
    predictions['longitude'] = predictions['coordinates'].apply(lambda x: x['longitude'])
    predictions['latitude'] = predictions['coordinates'].apply(lambda x: x['latitude'])
    predictions['images'] = predictions['xid'].apply(lambda xid: f"https://storage.yandexcloud.net/misis-progrev-gradientov/{xid}.jpg")
    return predictions


from st_pages import Page, show_pages

show_pages(
    [
        Page("main.py", "Главная", "🏠"),
        Page("pages/photo2place.py", "Поиск достопримечательности по фотографии", "🖼️"),
        Page("pages/text2place.py", "Поиск достопримечательности по тексту", icon="🔎"),
        Page("pages/navigation.py", "Построение маршрута", icon="🌎")
    ]
)

st.title('Предсказание достопримечательности по фото')

uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    if st.button('Predict'):
        # Download the image
        img_bytes = BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        predictions = predict(img_bytes)

        st.markdown('### Достопримечательность относится к одной из категорий:')
        cats = predictions.groupby(by='category')['probability'].sum()
        cats = pd.DataFrame(cats).reset_index()
        cats.columns = ['category', 'probability']
        cats['category'] = cats['category'].replace(main.TRANSLATION)
        fig = px.pie(cats, names='category', values='probability',
                     width=400, height=400)
        st.plotly_chart(fig)

        highest = predictions.iloc[predictions['probability'].idxmax()]['name']
        st.markdown(f"### Скорее всего это {highest}, посмотреть все варианты:")

        df_for_table = predictions[['xid', 'images', 'name', 'probability']]
        df_for_table.insert(0, "Select", False)
        table = st.data_editor(
            df_for_table,
            column_config={
                "name": st.column_config.SelectboxColumn(
                    "Предложение",
                    width="medium",
                    required=True,
                    options=predictions['name'].unique()
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

        st.markdown("### Посмотреть на карте")
        fig = px.scatter_mapbox(predictions,
                                lat='latitude',
                                lon='longitude',
                                size='probability',
                                zoom=10,
                                hover_name='name',
                                color='category')
        fig.update_layout(mapbox_style="open-street-map", height=800)
        st.plotly_chart(fig, use_container_width=True, height=800)
